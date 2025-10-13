document.getElementById('scrapeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const submitButton = form.querySelector('button[type="submit"]');
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    
    // Show loading state
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Analyzing...';
    
    try {
        const formData = new FormData(form);
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            resultsDiv.classList.remove('d-none');
            // Format and display results
            resultsContent.innerHTML = formatResults(data.data);
        } else {
            throw new Error(data.message || 'Analysis failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        submitButton.disabled = false;
        submitButton.innerHTML = 'Analyze';
    }
});

function formatResults(data) {
    // Format your results here based on the data structure
    // Return HTML string
}