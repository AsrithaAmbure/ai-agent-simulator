# AI Agent Simulator

A versatile AI agent simulator that accepts user prompts and returns categorized, intelligent responses. Supports multiple interfaces: CLI, GUI (Tkinter), and Web (Flask).

## Features

- **Prompt Categorization**: Automatically categorizes prompts into:
  - **Summarization**: Prompts asking for summaries or brief overviews
  - **Code Help**: Programming questions, debugging, and code-related queries
  - **Grammar Check**: Grammar, spelling, and proofreading requests
  - **General**: All other types of questions and conversations

- **Smart Response Generation**: 
  - Template-based responses for quick results
  - Optional OpenAI API integration for advanced responses
  - Automatic fallback to templates if API is unavailable

- **Multiple Interfaces**:
  - Command-line interface (CLI) with JSON output
  - Desktop GUI using Tkinter
  - Web interface using Flask with REST API

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

The CLI provides both interactive and single-prompt modes with JSON output.

**Interactive Mode:**
```bash
python scripts/agent_cli.py
```

**Interactive Mode with OpenAI:**
```bash
python scripts/agent_cli.py --use-openai
```

**Single Prompt Mode:**
```bash
python scripts/agent_cli.py --prompt "Summarize the history of AI"
```

**Single Prompt with OpenAI:**
```bash
python scripts/agent_cli.py --prompt "How do I reverse a string in Python?" --use-openai
```

**Output Format:**
```json
{
  "prompt": "Your prompt text",
  "category": "code-help",
  "response": "Generated response text",
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
- **Categorize** button: Shows only the category
- **Respond** button: Shows category and generates full response
- **Use OpenAI API** checkbox: Toggle OpenAI integration (requires API key)
- Status indicator showing OpenAI API availability
- Clear button to reset all fields

### Web Interface (Flask)

Start the web server:

```bash
python web/app.py
```

For development with debug mode enabled:

```bash
FLASK_DEBUG=true python web/app.py
```

Then open your browser to: **http://localhost:5000**

**Note**: Debug mode is disabled by default for security. Only enable it during development.

**API Endpoints:**

1. **POST /api/categorize** - Categorize a prompt
   ```bash
   curl -X POST http://localhost:5000/api/categorize \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Summarize this text"}'
   ```

2. **POST /api/respond** - Get full response
   ```bash
   curl -X POST http://localhost:5000/api/respond \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Fix this code error", "use_openai": false}'
   ```

3. **GET /api/status** - Check OpenAI API availability
   ```bash
   curl http://localhost:5000/api/status
   ```

## OpenAI API Integration

To use real OpenAI API responses instead of template-based responses:

### Step 1: Get an API Key
Sign up at [OpenAI](https://platform.openai.com/) and get your API key.

### Step 2: Set Environment Variable

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
$env:OPENAI_API_KEY='your-api-key-here'
```

**Using .env file:**
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-api-key-here
```

### Step 3: Enable in Application
- **CLI**: Use `--use-openai` flag
- **GUI**: Check the "Use OpenAI API" checkbox
- **Web**: Check the "Use OpenAI API" checkbox in the web interface

The application will automatically fall back to template responses if:
- The API key is not set
- The API request fails or times out
- The openai package is not installed

## Categorization Rules

The agent uses keyword-based heuristics to categorize prompts:

- **Summarization**: Keywords like "summarize", "summary", "tl;dr", "brief", "overview"
- **Code Help**: Keywords like "error", "bug", "code", "function", "debug", "how to", programming language names, or presence of code blocks
- **Grammar Check**: Keywords like "grammar", "spell", "proofread", "correct", "punctuation"
- **General**: Default category for all other prompts

## Examples

**Summarization:**
- "Summarize the history of artificial intelligence"
- "Give me a brief overview of machine learning"
- "TL;DR of this article about neural networks"

**Code Help:**
- "How do I write a Python function to reverse a string?"
- "Debug this error: IndexError in my loop"
- "Implement a binary search algorithm"

**Grammar Check:**
- "Check this grammar: She don't like apples"
- "Proofread my essay for spelling mistakes"
- "Correct the punctuation in this sentence"

**General:**
- "What is the capital of France?"
- "Explain quantum computing in simple terms"
- "What are the benefits of exercise?"

## Project Structure

```
ai-agent-simulator/
├── ai_agent/           # Core agent logic module
│   ├── __init__.py
│   └── agent.py        # Categorization and response generation
├── scripts/            # Executable scripts
│   ├── agent_cli.py    # Command-line interface
│   └── agent_gui.py    # Tkinter GUI
├── web/                # Flask web application
│   ├── app.py          # Flask server
│   ├── templates/
│   │   └── index.html  # Web UI
│   └── static/
│       └── style.css   # Styles
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## License

MIT License
