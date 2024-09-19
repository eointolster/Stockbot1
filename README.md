# Stockbot: AI Chat with Brave Search

Stockbot is an AI-powered chat application that provides stock analysis using Brave Search and Claude AI.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/stockbot.git
   cd stockbot
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   ANTHROPIC_API_KEY=your_claude_api_key_here
   BRAVE_API_KEY=your_brave_search_api_key_here
   ```
   Replace `your_claude_api_key_here` and `your_brave_search_api_key_here` with your actual API keys.

## Running the Application

1. Start the FastAPI server:
   ```
   python run.py
   ```

2. Open a web browser and navigate to `http://localhost:8000` to use the application.

## Usage

1. Enter a stock symbol or name in the "Ask about a stock" field.
2. (Optional) Add any additional comments or questions in the "Additional comments" field.
3. Click "Send" to submit your query.
4. The AI will provide an analysis in the "AI Response" section and a combined analysis considering your comments in the "Combined Analysis" section.

## Project Structure

- `run.py`: Entry point for running the FastAPI server
- `app/`: Main application directory
  - `main.py`: FastAPI application setup
  - `api.py`: API route definitions
  - `models.py`: Pydantic models for request/response handling
  - `utils.py`: Utility functions for AI and search operations
- `static/`: Static files (CSS, JavaScript)
- `templates/`: HTML templates
