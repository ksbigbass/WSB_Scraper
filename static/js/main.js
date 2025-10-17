function addValue() {
    const inputValue = document.getElementById('inputValue').value;
    if (inputValue) {
        const displayBox = document.getElementById('display-box');
        const newLine = document.createElement('p');
        newLine.textContent = inputValue;
        displayBox.appendChild(newLine);
        document.getElementById('inputValue').value = ''; // Clear input field
    }
}