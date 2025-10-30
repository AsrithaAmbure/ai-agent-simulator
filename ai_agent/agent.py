"""
Core AI Agent Module
Provides prompt categorization and response generation with optional OpenAI integration
"""
import os
import re
from typing import Tuple


def categorize_prompt(prompt: str) -> str:
    """
    Categorize a prompt using keyword-based heuristics.
    
    Args:
        prompt: User input prompt
        
    Returns:
        Category string: summarization, code-help, grammar-check, or general
    """
    prompt_lower = prompt.lower()
    
    # Summarization keywords (check first for specificity)
    summarization_keywords = ['summarize', 'summary', 'tl;dr', 'tldr', 'brief', 'overview', 
                              'condense', 'in short', 'recap', 'key points']
    if any(keyword in prompt_lower for keyword in summarization_keywords):
        return 'summarization'
    
    # Grammar-check keywords (check before code-help to avoid false positives with "error")
    grammar_keywords = ['grammar', 'spell', 'spelling', 'proofread', 'correct this',
                        'punctuation', 'fix grammar', 'grammatical', 'check grammar',
                        'check spelling']
    if any(keyword in prompt_lower for keyword in grammar_keywords):
        return 'grammar-check'
    
    # Code-help keywords and patterns
    code_keywords = ['error', 'bug', 'code', 'function', 'debug', 'how to', 'implement',
                     'syntax', 'programming', 'python', 'javascript', 'java', 'c++',
                     'algorithm', 'script', 'compile', 'exception']
    # Check for code blocks (markdown style ``` or indented)
    has_code_block = '```' in prompt or '\n    ' in prompt or '\n\t' in prompt
    
    if has_code_block or any(keyword in prompt_lower for keyword in code_keywords):
        return 'code-help'
    
    # Default to general
    return 'general'


def generate_response(prompt: str, category: str, use_openai: bool = False) -> Tuple[str, bool]:
    """
    Generate a response for the given prompt and category.
    
    Args:
        prompt: User input prompt
        category: Categorized type of prompt
        use_openai: Whether to attempt using OpenAI API
        
    Returns:
        Tuple of (response string, whether OpenAI was actually used)
    """
    used_openai = False
    
    # Try OpenAI if requested and API key is available
    if use_openai and os.environ.get('OPENAI_API_KEY'):
        try:
            response = _generate_openai_response(prompt, category)
            if response:
                return response, True
        except Exception as e:
            # Fall back to template responses on error
            print(f"OpenAI API error (falling back to templates): {e}")
    
    # Template-based responses
    response = _generate_template_response(prompt, category)
    return response, used_openai


def _generate_openai_response(prompt: str, category: str) -> str:
    """
    Generate response using OpenAI API.
    
    Args:
        prompt: User input prompt
        category: Categorized type of prompt
        
    Returns:
        Response string from OpenAI or None on failure
    """
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=os.environ.get('OPENAI_API_KEY'),
            timeout=10.0  # 10 second timeout
        )
        
        # Create system message based on category
        system_messages = {
            'summarization': 'You are a helpful assistant that provides concise summaries.',
            'code-help': 'You are a helpful programming assistant that helps debug code and answer technical questions.',
            'grammar-check': 'You are a helpful grammar and spelling checker that corrects text.',
            'general': 'You are a helpful assistant.'
        }
        
        system_message = system_messages.get(category, system_messages['general'])
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except ImportError:
        print("OpenAI package not installed")
        return None
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None


def _generate_template_response(prompt: str, category: str) -> str:
    """
    Generate a template-based response.
    
    Args:
        prompt: User input prompt
        category: Categorized type of prompt
        
    Returns:
        Template response string
    """
    templates = {
        'summarization': (
            f"I would summarize your request as follows:\n\n"
            f"Your prompt asks about: {prompt[:100]}...\n\n"
            f"Key points to consider:\n"
            f"- Main topic identified\n"
            f"- Context analyzed\n"
            f"- Summary approach determined\n\n"
            f"(Note: This is a simulated response. For real summarization, set OPENAI_API_KEY environment variable.)"
        ),
        'code-help': (
            f"Based on your code-related query:\n\n"
            f"Issue detected: {_extract_main_issue(prompt)}\n\n"
            f"Suggested approach:\n"
            f"1. Review the error message or requirements\n"
            f"2. Check syntax and logic\n"
            f"3. Test with simple inputs\n"
            f"4. Debug step by step\n\n"
            f"(Note: This is a simulated response. For detailed code help, set OPENAI_API_KEY environment variable.)"
        ),
        'grammar-check': (
            f"Grammar analysis of your text:\n\n"
            f"Original text reviewed: {prompt[:200]}\n\n"
            f"Suggestions:\n"
            f"- Check subject-verb agreement\n"
            f"- Review punctuation usage\n"
            f"- Verify spelling of key terms\n\n"
            f"(Note: This is a simulated response. For real grammar checking, set OPENAI_API_KEY environment variable.)"
        ),
        'general': (
            f"I understand you're asking: {prompt[:100]}...\n\n"
            f"This is a general inquiry. I'm here to help! "
            f"For more detailed and accurate responses, you can set the OPENAI_API_KEY environment variable.\n\n"
            f"Is there anything specific you'd like to know more about?"
        )
    }
    
    return templates.get(category, templates['general'])


def _extract_main_issue(prompt: str) -> str:
    """Extract the main issue from a code-help prompt."""
    # Simple heuristic: return first sentence or first 100 chars
    sentences = prompt.split('.')
    if sentences:
        issue = sentences[0].strip()
        return issue[:100] if len(issue) > 100 else issue
    return prompt[:100]
