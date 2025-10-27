# AI Agent Simulator

A versatile AI agent simulator that accepts user prompts and returns categorized, intelligent responses. Supports multiple interfaces: CLI, GUI (Tkinter), and Web (Flask).

## Features

- **Prompt Categorization**: Automatically categorizes prompts into:
  - Summarization
  - Code Help
  - Grammar Check
  - Question Answering
  - Creative Writing
  - Translation
  - General Conversation

- **Smart Response Generation**: Uses pattern matching, NLP, and optional OpenAI API integration

- **Multiple Interfaces**:
  - Command-line interface (CLI)
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

### Command-Line Interface
```bash
python cli_interface.py
```

### GUI Interface (Tkinter)
```bash
python gui_interface.py
```

### Web Interface
```bash
python web_app.py
# Open browser to http://localhost:5000
```

## Optional: OpenAI API Integration

To use real OpenAI API responses:
1. Set your API key as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key-here'
```
2. The agent will automatically use the API when available

## Testing

```bash
python -m pytest tests/
```

## Examples

- "Summarize the history of artificial intelligence"
- "How do I write a Python function to reverse a string?"
- "Check this grammar: She don't like apples"
- "What is the capital of France?"
- "Write a short poem about coding"

## License

MIT License
