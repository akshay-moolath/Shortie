async function urlshortner(event) {
    event.preventDefault();
    const inputBox = document.getElementById('long-url');      
    const inputText = inputBox.value;
    const resultField = document.getElementById("short-url");
    resultField.value = "Shortening...";


    const response = await fetch('/shorten', {
            method: 'POST',
            headers: { 'Content-Type':'text/plain'},
            body: inputText
        });
    const shortUrl = await response.text();
    
}
document.getElementById('short-url').addEventListener('submit', urlshortner);

function copyShortUrl() {
            let shortUrlInput = document.getElementById("shortUrl");
            shortUrlInput.select();
            document.execCommand("copy");
            alert("Copied: " + shortUrlInput.value);
        }
