import logging

# Configure logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler("mainApp.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)