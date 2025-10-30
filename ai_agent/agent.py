"""
Core AI Agent logic for categorization and response generation.
"""

import os
import re


def categorize_prompt(prompt):
    """
    Categorize a prompt based on keyword heuristics.
    
    Args:
        prompt: The user's input prompt string
        
    Returns:
        str: Category name - one of 'summarization', 'code-help', 'grammar-check', 'general'
    """
    prompt_lower = prompt.lower()
    
    # Check for summarization keywords (highest priority for these specific words)
    summarization_keywords = ['summarize', 'summary', 'tl;dr', 'tldr', 'brief', 'overview', 
                             'recap', 'condense', 'key points', 'main points']
    if any(keyword in prompt_lower for keyword in summarization_keywords):
        return 'summarization'
    
    # Check for code-help keywords and code patterns (check before grammar to prioritize technical content)
    code_keywords = ['error', 'bug', 'debug', 'code', 'function', 'programming', 
                    'python', 'java', 'javascript', 'typescript', 'c++', 'c#',
                    'implement', 'algorithm', 'script', 'syntax', 'compile',
                    'exception', 'traceback', 'nameerror', 'typeerror', 'valueerror']
    
    how_to_code = 'how to' in prompt_lower or 'how do i' in prompt_lower
    
    # Check for code block patterns (backticks, indentation)
    has_code_block = '```' in prompt or '`' in prompt
    has_code_keywords = any(keyword in prompt_lower for keyword in code_keywords)
    
    if has_code_block or has_code_keywords or how_to_code:
        return 'code-help'
    
    # Check for grammar check keywords (check after code-help)
    grammar_keywords = ['grammar', 'spell', 'spelling', 'proofread', 'punctuation']
    # More specific grammar patterns
    grammar_phrases = ['check this grammar', 'check grammar', 'fix grammar', 
                      'correct this', 'proofread this', 'check spelling']
    
    has_grammar_keywords = any(keyword in prompt_lower for keyword in grammar_keywords)
    has_grammar_phrases = any(phrase in prompt_lower for phrase in grammar_phrases)
    
    if has_grammar_keywords or has_grammar_phrases:
        return 'grammar-check'
    
    # Default to general category
    return 'general'


def generate_response(prompt, category, use_openai=False):
    """
    Generate a response for the given prompt and category.
    
    Args:
        prompt: The user's input prompt string
        category: The categorized type of prompt
        use_openai: Whether to attempt using OpenAI API
        
    Returns:
        tuple: (response_string, used_openai_bool)
    """
    # Try OpenAI if requested and API key is available
    if use_openai and os.environ.get('OPENAI_API_KEY'):
        try:
            response = _generate_openai_response(prompt, category)
            return response, True
        except Exception as e:
            # Fall back to template response on any error
            print(f"OpenAI API error (falling back to template): {e}")
            pass
    
    # Generate template-based response
    response = _generate_template_response(prompt, category)
    return response, False


def _generate_openai_response(prompt, category):
    """
    Generate a response using OpenAI API.
    
    Args:
        prompt: The user's input prompt
        category: The categorized type
        
    Returns:
        str: Response from OpenAI
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise Exception("openai package not installed")
    
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    
    # Create a system message based on category
    system_messages = {
        'summarization': 'You are a helpful assistant that provides clear and concise summaries.',
        'code-help': 'You are a helpful programming assistant that helps with code, debugging, and technical questions.',
        'grammar-check': 'You are a helpful assistant that checks grammar, spelling, and writing quality.',
        'general': 'You are a helpful and friendly AI assistant.'
    }
    
    system_message = system_messages.get(category, system_messages['general'])
    
    # Call OpenAI API with timeout
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        timeout=10.0
    )
    
    return response.choices[0].message.content.strip()


def _generate_template_response(prompt, category):
    """
    Generate a template-based response without using OpenAI.
    
    Args:
        prompt: The user's input prompt
        category: The categorized type
        
    Returns:
        str: Template-based response
    """
    templates = {
        'summarization': (
            f"I can help you with summarization! For the topic you've mentioned, "
            f"here's a brief overview: This appears to be about {_extract_topic(prompt)}. "
            f"Key points would include the main concepts, important details, and conclusions. "
            f"To provide a more accurate summary, I would need the full text to analyze."
        ),
        'code-help': (
            f"I can help with your coding question! Based on your query, it seems you're working with "
            f"{_extract_topic(prompt)}. Here are some general tips:\n\n"
            f"1. Break down the problem into smaller steps\n"
            f"2. Check for common errors like syntax issues or logic bugs\n"
            f"3. Use debugging tools and print statements\n"
            f"4. Consult official documentation for the specific language/library\n\n"
            f"For specific code help, please provide more details about your issue and any error messages."
        ),
        'grammar-check': (
            f"I can help check your grammar! To properly review your text, please provide the specific "
            f"text you'd like me to check. I'll look for:\n\n"
            f"- Spelling errors\n"
            f"- Grammar mistakes\n"
            f"- Punctuation issues\n"
            f"- Sentence structure improvements\n\n"
            f"Please share the text you'd like me to proofread."
        ),
        'general': (
            f"Thank you for your question about {_extract_topic(prompt)}. I'm here to help! "
            f"This is a general inquiry, and I'll do my best to assist. "
            f"Could you provide more specific details about what you'd like to know? "
            f"I can help with summaries, code questions, grammar checks, and general information."
        )
    }
    
    return templates.get(category, templates['general'])


def _extract_topic(prompt):
    """
    Extract a simple topic from the prompt for use in templates.
    
    Args:
        prompt: The user's input prompt
        
    Returns:
        str: A short topic description
    """
    # Take first few words as topic, clean up
    words = prompt.split()[:5]
    topic = ' '.join(words)
    if len(prompt.split()) > 5:
        topic += '...'
    return topic if topic else 'your query'
