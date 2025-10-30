# AI Agent Simulator

A versatile AI agent simulator that accepts user prompts and returns categorized, intelligent responses. Supports multiple interfaces: CLI, GUI (Tkinter), and Web (Flask).

## Features

- **Prompt Categorization**: Automatically categorizes prompts into:
  - **Summarization**: Detects requests for summaries (keywords: summarize, tl;dr, brief, overview, etc.)
  - **Code Help**: Identifies programming questions and code issues (keywords: error, bug, how to, code, function, etc.)
  - **Grammar Check**: Recognizes grammar and spelling requests (keywords: grammar, spell, proofread, correct, etc.)
  - **General**: Default category for general questions and conversation

- **Smart Response Generation**: 
  - Template-based responses for offline/fallback mode
  - Optional OpenAI API integration (GPT-3.5-turbo) when API key is available
  - Automatic fallback to templates if API fails or is unavailable

- **Multiple Interfaces**:
  - Command-line interface (CLI) with JSON output
  - Desktop GUI using Tkinter
  - Web interface using Flask

## Installation

```bash
# Clone the repository
git clone https://github.com/AsrithaAmbure/ai-agent-simulator.git
cd ai-agent-simulator

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command-Line Interface (CLI)

The CLI provides both single-prompt and interactive modes with JSON output.

**Single prompt mode:**
```bash
python scripts/agent_cli.py --prompt "Summarize the history of AI"
```

**With OpenAI API:**
```bash
python scripts/agent_cli.py --prompt "How do I fix this Python error?" --use-openai
```

**Interactive mode:**
```bash
python scripts/agent_cli.py
# Or with OpenAI enabled:
python scripts/agent_cli.py --use-openai
```

**Output format:**
```json
{
  "prompt": "Your prompt here",
  "category": "code-help",
  "response": "Generated response...",
  "used_openai": false
}
```

### GUI Interface (Tkinter)

Launch the desktop GUI application:

```bash
python scripts/agent_gui.py
```

**Features:**
- Text input area for entering prompts
- **Categorize** button to categorize the prompt
- **Respond** button to generate a full response
- **Use OpenAI** checkbox to enable/disable OpenAI API
- **Clear** button to reset all fields
- Status indicator showing OpenAI API key availability
- Category display with color-coded badges
- Response display area

### Web Interface (Flask)

Start the web server:

```bash
python web/app.py
```

Then open your browser to: **http://localhost:5000**

**API Endpoints:**

1. **POST /api/categorize** - Categorize a prompt
   ```json
   Request: {"prompt": "Your prompt"}
   Response: {"prompt": "Your prompt", "category": "code-help"}
   ```

2. **POST /api/respond** - Generate a response
   ```json
   Request: {
     "prompt": "Your prompt",
     "category": "code-help",  // optional
     "use_openai": true        // optional, default false
   }
   Response: {
     "prompt": "Your prompt",
     "category": "code-help",
     "response": "Generated response...",
     "used_openai": false
   }
   ```

3. **GET /api/status** - Check OpenAI API key availability
   ```json
   Response: {"has_openai_key": true}
   ```

## OpenAI API Integration

To use OpenAI API for enhanced responses:

1. **Set your API key as an environment variable:**

   **Linux/Mac:**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

   **Windows (Command Prompt):**
   ```cmd
   set OPENAI_API_KEY=your-api-key-here
   ```

   **Windows (PowerShell):**
   ```powershell
   $env:OPENAI_API_KEY="your-api-key-here"
   ```

2. **The agent will automatically detect and use the API when:**
   - The environment variable is set
   - The `use_openai` flag is enabled in CLI/GUI/Web
   - The `openai` package is installed

3. **Fallback behavior:**
   - If API call fails or times out, falls back to template responses
   - If API key is not set, uses template responses
   - Timeout set to 10 seconds for API calls

## Examples

Here are some example prompts to try:

### Summarization
- "Summarize the history of artificial intelligence"
- "Give me a brief overview of machine learning"
- "TL;DR: What is quantum computing?"

### Code Help
- "How do I write a Python function to reverse a string?"
- "I'm getting this error: TypeError: unsupported operand type(s)"
- "How to implement a binary search algorithm?"
- "Debug this code: ```python\ndef add(a,b) return a+b\n```"

### Grammar Check
- "Check this grammar: She don't like apples"
- "Proofread this sentence: Their going to the store"
- "Fix spelling: I recieved the package"

### General
- "What is the capital of France?"
- "Explain photosynthesis"
- "Tell me about the solar system"

## Project Structure

```
ai-agent-simulator/
├── ai_agent/              # Core agent module
│   ├── __init__.py
│   └── agent.py          # Categorization and response logic
├── scripts/              # Executable scripts
│   ├── agent_cli.py      # Command-line interface
│   └── agent_gui.py      # Tkinter GUI
├── web/                  # Flask web application
│   ├── app.py           # Flask app and API endpoints
│   ├── templates/
│   │   └── index.html   # Web UI
│   └── static/
│       └── style.css    # Styling
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Requirements

- Python 3.7+
- Flask 3.0.0
- openai 1.3.0 (for OpenAI API integration)
- python-dotenv 1.0.0
- tkinter (usually comes with Python)

## License

MIT License
