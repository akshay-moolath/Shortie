async function shorter() 
{
    const inputBox = document.getElementById('long-url');
    const inputText = inputBox.value;
    const OutputBox = document.getElementById('short-url');        
    
    const response = await fetch('/shorten', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body:JSON.stringify({ url: inputText })
        });

        OutputBox.value = await response.text()
        
                                    
}