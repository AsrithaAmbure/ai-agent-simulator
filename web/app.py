"""
Flask Web Application for AI Agent Simulator
Provides a web interface and JSON API for categorizing prompts and generating responses
"""
from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agent.agent import categorize_prompt, generate_response

app = Flask(__name__)


@app.route('/')
def index():
    """Render the main web interface."""
    return render_template('index.html')


@app.route('/api/categorize', methods=['POST'])
def api_categorize():
    """
    API endpoint to categorize a prompt.
    
    Expects JSON: {"prompt": "user prompt"}
    Returns JSON: {"prompt": "...", "category": "..."}
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' field"}), 400
        
        prompt = data['prompt']
        category = categorize_prompt(prompt)
        
        return jsonify({
            "prompt": prompt,
            "category": category
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/respond', methods=['POST'])
def api_respond():
    """
    API endpoint to generate a full response.
    
    Expects JSON: {"prompt": "user prompt", "use_openai": true/false}
    Returns JSON: {"prompt": "...", "category": "...", "response": "...", "used_openai": true/false}
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' field"}), 400
        
        prompt = data['prompt']
        use_openai = data.get('use_openai', False)
        
        category = categorize_prompt(prompt)
        response, used_openai = generate_response(prompt, category, use_openai)
        
        return jsonify({
            "prompt": prompt,
            "category": category,
            "response": response,
            "used_openai": used_openai
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/status', methods=['GET'])
def api_status():
    """
    API endpoint to check OpenAI API availability.
    
    Returns JSON: {"openai_available": true/false}
    """
    openai_available = bool(os.environ.get('OPENAI_API_KEY'))
    return jsonify({"openai_available": openai_available})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
