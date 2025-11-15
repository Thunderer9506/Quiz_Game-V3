// Select all the 'choice' buttons on the quiz page
const choiceButtons = document.querySelectorAll('.quiz-options-area .choice');

// This variable will hold the currently selected button
let selectedAnswer = null;

// Loop through each choice button and add a click event listener
choiceButtons.forEach(button => {
    button.addEventListener('click', () => {
        // 1. Remove 'active' class from the previously selected answer
        if (selectedAnswer) {
            selectedAnswer.classList.remove('active');
        }

        // 2. Add 'active' class to the button that was just clicked
        button.classList.add('active');

        // 3. Update our variable to store the new active button
        selectedAnswer = button;
        
        // Optional: You can log the answer to the console to test
        // .mcq is the <p> tag, .textContent gets the text
        console.log("Selected:", selectedAnswer.querySelector('.mcq').textContent);
    });
});