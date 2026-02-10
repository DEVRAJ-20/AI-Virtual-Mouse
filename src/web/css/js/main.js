// =======================
// Python ↔ JS bridge
// =======================

// Function to display messages from Python (AI assistant)
function addAppMsg(msg) {
    const element = document.getElementById("messages");
    element.innerHTML += '<div class="message to ready ltor">' + msg + '</div>';
    element.scrollTop = element.scrollHeight - element.clientHeight - 15;
    const index = element.childElementCount - 1;
    setTimeout(changeClass.bind(null, element, index, "message to"), 500);
}

// Function to display user messages
function addUserMsg(msg) {
    const element = document.getElementById("messages");
    element.innerHTML += '<div class="message from ready rtol">' + msg + '</div>';
    element.scrollTop = element.scrollHeight - element.clientHeight - 15;
    const index = element.childElementCount - 1;
    setTimeout(changeClass.bind(null, element, index, "message from"), 500);
}

// Helper function to change class after animation
function changeClass(element, index, newClass) {
    console.log(newClass + ' ' + index);
    element.children[index].className = newClass;
}

// Expose these functions so Python can call them
eel.expose(addAppMsg);
eel.expose(addUserMsg);


// =======================
// User input handling
// =======================

// Send message when user clicks button
document.getElementById("userInputButton").addEventListener("click", getUserInput, false);

// Send message when user presses Enter key (keyCode 13)
document.getElementById("userInput").addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        getUserInput();
    }
});

// Function to send user input to Python
function getUserInput() {
    const element = document.getElementById("userInput");
    const msg = element.value.trim();
    if (msg.length !== 0) {
        element.value = "";
        eel.getUserInput(msg);  // Sends message to Python
    }
}
