"""
Flask web application for AI Agent Simulator.
Provides web UI and JSON API endpoints.
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path to import ai_agent module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agent.agent import categorize_prompt, generate_response


app = Flask(__name__)


@app.route('/')
def index():
    """Serve the main web UI."""
    has_api_key = bool(os.environ.get('OPENAI_API_KEY'))
    return render_template('index.html', has_api_key=has_api_key)


@app.route('/api/categorize', methods=['POST'])
def api_categorize():
    """
    API endpoint to categorize a prompt.
    
    Request JSON:
        {
            "prompt": "user prompt text"
        }
    
    Response JSON:
        {
            "prompt": "user prompt text",
            "category": "category-name"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt field'}), 400
        
        prompt = data['prompt']
        
        if not prompt.strip():
            return jsonify({'error': 'Prompt cannot be empty'}), 400
        
        category = categorize_prompt(prompt)
        
        return jsonify({
            'prompt': prompt,
            'category': category
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/respond', methods=['POST'])
def api_respond():
    """
    API endpoint to generate a response.
    
    Request JSON:
        {
            "prompt": "user prompt text",
            "category": "category-name" (optional, will categorize if not provided),
            "use_openai": true/false (optional, default false)
        }
    
    Response JSON:
        {
            "prompt": "user prompt text",
            "category": "category-name",
            "response": "generated response",
            "used_openai": true/false
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt field'}), 400
        
        prompt = data['prompt']
        
        if not prompt.strip():
            return jsonify({'error': 'Prompt cannot be empty'}), 400
        
        # Get or determine category
        if 'category' in data and data['category']:
            category = data['category']
        else:
            category = categorize_prompt(prompt)
        
        # Get use_openai flag
        use_openai = data.get('use_openai', False)
        
        # Generate response
        response, used_openai = generate_response(prompt, category, use_openai)
        
        return jsonify({
            'prompt': prompt,
            'category': category,
            'response': response,
            'used_openai': used_openai
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def api_status():
    """
    API endpoint to check API key status.
    
    Response JSON:
        {
            "has_openai_key": true/false
        }
    """
    return jsonify({
        'has_openai_key': bool(os.environ.get('OPENAI_API_KEY'))
    })


if __name__ == '__main__':
    print("=" * 60)
    print("AI Agent Simulator - Web Interface")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    
    if os.environ.get('OPENAI_API_KEY'):
        print("✓ OpenAI API Key detected")
    else:
        print("✗ No OpenAI API Key (using template responses)")
    
    print("=" * 60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
