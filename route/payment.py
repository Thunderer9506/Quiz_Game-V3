from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models import db
from sqlalchemy import select
from schemas.user import User
from utils.token_mangement import decode_jwt_token, token_required
from logger_config import logger
import razorpay
import os
from dotenv import load_dotenv

load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

payment_bp = Blueprint(
    'payment', 
    __name__, 
    template_folder='templates', # Specifies the blueprint's template folder
    url_prefix='/payment'           # All routes in this blueprint will start with /payment
)


@payment_bp.route("/payment_page")
@token_required
def payment_page():
    return render_template("payment.html")


@payment_bp.route("/payment", methods=["POST"])
@token_required
def payment():
    try:
        credits_raw = request.form.get("credits")
        if credits_raw is None:
            flash("Invalid credits", "error")
            return redirect(url_for("payment.payment_page"))

        try:
            credits = int(credits_raw)
        except (TypeError, ValueError):
            flash("Invalid credits", "error")
            return redirect(url_for("payment.payment_page"))

        if credits <= 0:
            flash("Invalid credits", "error")
            return redirect(url_for("payment.payment_page"))
        
        # Validate minimum credits
        if credits < 5:
            flash("Minimum 5 credits required", "error")
            return redirect(url_for("payment.payment_page"))
        
        
        # Calculate amounts
        credit_price_raw = os.getenv("CREDITS_PER_PRICE")
        if not credit_price_raw:
            flash("Payment configuration missing. Please try again later.", "error")
            return redirect(url_for("payment.payment_page"))

        credit_price = int(credit_price_raw)
        subtotal = credits * credit_price
        fees = subtotal * 0.02  # 2% payment fees
        gst = (subtotal + fees) * 0.18  # 18% GST
        total_amount = subtotal + fees + gst

        amount_paise = total_amount * 100
        
        data = {
            "amount": int(amount_paise),
            "currency": "INR",
            "payment_capture": 1 # Auto-capture payment
        }

        # Create order via Razorpay API
        order = client.order.create(data=data)
        
        # Store order details in session for verification
        session['pending_order'] = {
            'order_id': order['id'],
            'credits': credits,
            'amount': int(total_amount)
        }
        
        return jsonify({
            "order_id": order['id'],
            "amount": int(amount_paise),
            "currency": "INR",
            "key_id": RAZORPAY_KEY_ID,
            "credits": credits
        })
        
    except Exception as e:
        logger.error(f"Payment error: {e}")
        flash("Payment failed. Please try again.", "error")
        return redirect(url_for("payment.payment_page"))


@payment_bp.route('/verify_payment', methods=['POST'])
@token_required
def verify_payment():
    """
    1. Receive payment_id, order_id, and signature from frontend.
    2. Verify the signature using Razorpay utility.
    3. If valid, update your database (add credits to user).
    """
    data = request.json
    
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_signature = data.get('razorpay_signature')

    # Create the dictionary required for verification
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }

    try:
        # This will raise a SignatureVerificationError if verification fails
        client.utility.verify_payment_signature(params_dict)
        
        # --- SUCCESS ---
        # Get pending order details from session
        pending_order = session.get('pending_order')
        if not pending_order:
            return jsonify({"status": "failure", "message": "Order details not found"}), 400
        
        # Verify order matches
        if pending_order['order_id'] != razorpay_order_id:
            return jsonify({"status": "failure", "message": "Order mismatch"}), 400
        
        user_id = decode_jwt_token(request.cookies.get("user_id"))
        stmt = select(User).where(User.id == user_id)
        user = db.session.execute(stmt).scalar()
        
        if not user:
            return jsonify({"status": "failure", "message": "User not found"}), 404
        
        # Add credits to user account
        credits_to_add = pending_order['credits']
        user.credits += credits_to_add
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to commit credits update: {e}")
            return jsonify({"status": "failure", "message": "Could not update credits"}), 500
        
        # Clear session
        session.pop('pending_order', None)
        
        logger.info(f"Payment verified: Added {credits_to_add} credits to user {user_id}")
        return jsonify({
            "status": "success", 
            "message": f"Payment verified successfully! {credits_to_add} credits added.",
            "credits_added": credits_to_add,
            "total_credits": user.credits
        })

    except razorpay.errors.SignatureVerificationError:
        return jsonify({"status": "failure", "message": "Payment verification failed"}), 400
    except Exception as e:
        logger.error(f"Payment verification error: {e}")
        return jsonify({"status": "failure", "message": "Payment verification failed"}), 500


@payment_bp.route('/webhook', methods=['POST'])
def razorpay_webhook():
    """
    Razorpay webhook handler for payment confirmations
    This provides a backup verification mechanism
    """
    try:
        # Get webhook secret from environment
        webhook_secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")
        if not webhook_secret:
            logger.error("Webhook secret not configured")
            return jsonify({"status": "error", "message": "Webhook not configured"}), 500
        
        # Verify webhook signature
        webhook_signature = request.headers.get('X-Razorpay-Signature')
        if not webhook_signature:
            logger.warning("Webhook received without signature")
            return jsonify({"status": "error", "message": "Missing signature"}), 400
        
        # Generate expected signature
        import hmac
        import hashlib
        
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            request.data,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(webhook_signature, expected_signature):
            logger.warning("Invalid webhook signature")
            return jsonify({"status": "error", "message": "Invalid signature"}), 400
        
        # Parse webhook payload
        payload = request.json
        event = payload.get('event')
        
        if event == 'payment.captured':
            payment_data = payload.get('payload', {}).get('payment', {}).get('entity', {})
            order_id = payment_data.get('order_id')
            
            # Find user by order_id (you'd need to store order_id with user)
            # This is a simplified version - in production, you'd track orders properly
            logger.info(f"Webhook: Payment captured for order {order_id}")
            
        return jsonify({"status": "success"})
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": "Webhook processing failed"}), 500