const submitButton = document.querySelector('.submit');

// Listen for the submit button to be clicked
submitButton.addEventListener('click', (event) => {
    // Prevent the form from actually submitting (which refreshes the page)
    event.preventDefault(); 

});