const quizData = {
    "Html": [
        {
            "question": "What does the <label> tag do?",
            "options": [
                "It styles form inputs",
                "It provides accessibility for input elements",
                "It submits the form",
                "It resets form values"
            ],
            "answer": "It provides accessibility for input elements"
        },
        {
            "question": "Which tag is used to create a hyperlink?",
            "options": ["<link>", "<a>", "<href>", "<url>"],
            "answer": "<a>"
        },
        {
            "question": "What is the correct way to embed an image in HTML?",
            "options": [
                "<img src='image.jpg'>",
                "<image src='image.jpg'>",
                "<img href='image.jpg'>",
                "<pic src='image.jpg'>"
            ],
            "answer": "<img src='image.jpg'>"
        },
        {
            "question": "Which HTML tag is used for a line break?",
            "options": ["<break>", "<br>", "<lb>", "<hr>"],
            "answer": "<br>"
        },
        {
            "question": "What does the <meta> tag provide?",
            "options": [
                "Page styling",
                "Metadata about the HTML document",
                "Interactive content",
                "Structural layout"
            ],
            "answer": "Metadata about the HTML document"
        },
        {
            "question": "Which tag is used to define a table row?",
            "options": ["<tr>", "<td>", "<th>", "<row>"],
            "answer": "<tr>"
        },
        {
            "question": "What is the default type of a button element?",
            "options": ["submit", "button", "reset", "input"],
            "answer": "submit"
        },
        {
            "question": "Which HTML tag is used to define a list item?",
            "options": ["<li>", "<ul>", "<ol>", "<item>"],
            "answer": "<li>"
        },
        {
            "question": "Which tag is used for inserting a horizontal line?",
            "options": ["<line>", "<hr>", "<hl>", "<break>"],
            "answer": "<hr>"
        },
        {
            "question": "Which attribute is used to define inline styles?",
            "options": ["class", "style", "id", "css"],
            "answer": "style"
        }
    ],
    "Css": [
        {
            "question": "What does 'display: flex' do?",
            "options": [
                "Makes the element hidden",
                "Aligns elements vertically by default",
                "Turns a container into a flexible box layout",
                "Applies animations to child elements"
            ],
            "answer": "Turns a container into a flexible box layout"
        },
        {
            "question": "Which property is used to change text color?",
            "options": ["background-color", "text-color", "font-color", "color"],
            "answer": "color"
        },
        {
            "question": "What does 'z-index' control?",
            "options": [
                "The transparency of elements",
                "The stacking order of elements",
                "The margin of an element",
                "The animation speed"
            ],
            "answer": "The stacking order of elements"
        },
        {
            "question": "What is the default position value in CSS?",
            "options": ["relative", "absolute", "static", "fixed"],
            "answer": "static"
        },
        {
            "question": "Which unit is relative to the root element?",
            "options": ["em", "rem", "%", "vh"],
            "answer": "rem"
        },
        {
            "question": "Which CSS property controls spacing between lines of text?",
            "options": ["letter-spacing", "line-height", "word-spacing", "text-indent"],
            "answer": "line-height"
        },
        {
            "question": "How do you apply a class selector in CSS?",
            "options": [".classname", "#classname", "*classname", "/classname"],
            "answer": ".classname"
        },
        {
            "question": "Which property makes an element float to the right?",
            "options": ["position: right", "align: right", "float: right", "move: right"],
            "answer": "float: right"
        },
        {
            "question": "Which property is used to round the corners of an element?",
            "options": ["corner-radius", "border-style", "border-radius", "radius"],
            "answer": "border-radius"
        },
        {
            "question": "What does 'overflow: hidden' do?",
            "options": [
                "Hides text only",
                "Hides overflowed content",
                "Enables auto scroll",
                "Resizes the container"
            ],
            "answer": "Hides overflowed content"
        }
    ],
    "Js": [
        {
            "question": "What does 'event.preventDefault()' do?",
            "options": [
                "Stops the page from refreshing on form submit",
                "Prevents user input",
                "Prevents syntax errors",
                "Stops all JS execution"
            ],
            "answer": "Stops the page from refreshing on form submit"
        },
        {
            "question": "Which method is used to parse a JSON string?",
            "options": ["JSON.parse()", "JSON.stringify()", "parseInt()", "toString()"],
            "answer": "JSON.parse()"
        },
        {
            "question": "What is a closure?",
            "options": [
                "A function that runs once",
                "A function that remembers variables from its outer scope",
                "A function inside a loop",
                "A global function"
            ],
            "answer": "A function that remembers variables from its outer scope"
        },
        {
            "question": "What is the default behavior of 'fetch'?",
            "options": [
                "Synchronous request",
                "Returns a Promise",
                "Returns XML",
                "Reloads the page"
            ],
            "answer": "Returns a Promise"
        },
        {
            "question": "Which keyword declares a block-scoped variable?",
            "options": ["var", "let", "const", "both let and const"],
            "answer": "both let and const"
        },
        {
            "question": "Which of these is a primitive data type?",
            "options": ["Array", "Object", "Function", "String"],
            "answer": "String"
        },
        {
            "question": "What is the output of typeof null?",
            "options": ["'null'", "'object'", "'undefined'", "'boolean'"],
            "answer": "'object'"
        },
        {
            "question": "What does 'this' refer to in a regular function?",
            "options": ["The current object", "Window/global object", "null", "The previous function"],
            "answer": "Window/global object"
        },
        {
            "question": "How do you write an arrow function?",
            "options": [
                "() -> {}",
                "() => {}",
                "function() => {}",
                "=> function()"
            ],
            "answer": "() => {}"
        },
        {
            "question": "What does '===' check in JS?",
            "options": [
                "Value only",
                "Type only",
                "Both value and type",
                "Neither value nor type"
            ],
            "answer": "Both value and type"
        }
    ],
    "Accessibility": [
        {
            "question": "What does the 'aria-label' attribute do?",
            "options": [
                "Adds a tooltip",
                "Styles an element",
                "Provides label text for screen readers",
                "Hides the element"
            ],
            "answer": "Provides label text for screen readers"
        },
        {
            "question": "Which HTML element defines the main content of a document?",
            "options": ["<main>", "<section>", "<div>", "<body>"],
            "answer": "<main>"
        },
        {
            "question": "What is the purpose of the 'alt' attribute in images?",
            "options": [
                "Changes image size",
                "Adds a caption",
                "Provides alternative text for screen readers",
                "Embeds video"
            ],
            "answer": "Provides alternative text for screen readers"
        },
        {
            "question": "Which tag should be used for navigation links?",
            "options": ["<nav>", "<aside>", "<header>", "<section>"],
            "answer": "<nav>"
        },
        {
            "question": "What is 'semantic HTML'?",
            "options": [
                "HTML used for styling",
                "HTML with no structure",
                "HTML that describes meaning and structure",
                "HTML for mobile devices"
            ],
            "answer": "HTML that describes meaning and structure"
        },
        {
            "question": "Which element is best for grouping a set of related form controls?",
            "options": ["<div>", "<section>", "<fieldset>", "<form>"],
            "answer": "<fieldset>"
        },
        {
            "question": "Which role attribute is used for a dialog box?",
            "options": ["alert", "popup", "dialog", "tooltip"],
            "answer": "dialog"
        },
        {
            "question": "What is the correct role for a navigation bar?",
            "options": ["navigation", "menu", "toolbar", "nav"],
            "answer": "navigation"
        },
        {
            "question": "How can you make a button accessible?",
            "options": [
                "Use <div> with onclick",
                "Use <a> with href",
                "Use <button> with clear text",
                "Use CSS for styling only"
            ],
            "answer": "Use <button> with clear text"
        },
        {
            "question": "Which element is used to group headings, text, and images?",
            "options": ["<section>", "<header>", "<article>", "<main>"],
            "answer": "<article>"
        }
    ]
}