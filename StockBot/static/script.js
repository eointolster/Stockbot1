document.addEventListener('DOMContentLoaded', () => {
    const userInputForm = document.getElementById('user-input-form');
    const userQuestion = document.getElementById('user-question');
    const userComments = document.getElementById('user-comments');
    const aiSummary = document.getElementById('ai-summary');
    const aiAnalysis = document.getElementById('ai-analysis');
    const combinedSummary = document.getElementById('combined-summary');
    const combinedAnalysis = document.getElementById('combined-analysis');
    const loadingSpinner = document.getElementById('loading-spinner');

    userInputForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = userQuestion.value.trim();
        const comments = userComments.value.trim();
        
        if (question) {
            // Show immediate feedback
            aiSummary.textContent = "Processing your request...";
            aiAnalysis.textContent = "";
            combinedSummary.textContent = "";
            combinedAnalysis.textContent = "";
            
            // Show loading spinner
            loadingSpinner.classList.remove('hidden');
            
            await sendMessage(question, comments);
            
            // Hide loading spinner
            loadingSpinner.classList.add('hidden');
        }
    });

    async function sendMessage(question, comments) {
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: question,
                    user_comments: comments
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            displayResponse(data);

            // Reset form
            userQuestion.value = '';
            userComments.value = '';

        } catch (error) {
            console.error('Error:', error);
            displayError(error);
        }
    }

    function displayResponse(data) {
        aiSummary.innerHTML = formatContent(data.ai_response.summary);
        aiAnalysis.innerHTML = formatContent(data.ai_response.detailed_analysis);
        
        // Display AI's opinion
        const aiOpinionElement = document.createElement('div');
        aiOpinionElement.innerHTML = `AI Opinion: ${data.ai_response.ai_opinion === 'THUMBS_UP' ? '👍' : '👎'}`;
        aiAnalysis.appendChild(aiOpinionElement);

        // Display Combined Analysis
        combinedSummary.innerHTML = formatContent(data.combined_analysis.summary);
        combinedAnalysis.innerHTML = formatContent(data.combined_analysis.detailed_analysis);
    }

    function displayError(error) {
        aiSummary.textContent = 'An error occurred while processing your request.';
        aiAnalysis.textContent = `Error details: ${error.message}`;
        combinedSummary.textContent = '';
        combinedAnalysis.textContent = '';
    }

    function formatContent(content) {
        // Apply formatting based on content
        if (content.includes('increase') || content.includes('up')) {
            return `<span style="color: green;">${content}</span>`;
        } else if (content.includes('decrease') || content.includes('down')) {
            return `<span style="color: red;">${content}</span>`;
        }
        return content;
    }
});