#!/usr/bin/env python3
"""
Command-line interface for AI Agent Simulator.
Accepts prompts interactively or via --prompt argument and outputs JSON.
"""

import argparse
import json
import sys
import os

# Add parent directory to path to import ai_agent module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agent.agent import categorize_prompt, generate_response


def process_prompt(prompt, use_openai=False):
    """
    Process a single prompt and return result as dict.
    
    Args:
        prompt: The user's input prompt
        use_openai: Whether to use OpenAI API
        
    Returns:
        dict: Result with prompt, category, response, used_openai fields
    """
    category = categorize_prompt(prompt)
    response, used_openai = generate_response(prompt, category, use_openai)
    
    return {
        'prompt': prompt,
        'category': category,
        'response': response,
        'used_openai': used_openai
    }


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='AI Agent Simulator - Command Line Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --prompt "Summarize the history of AI"
  %(prog)s --prompt "How do I fix this Python error?" --use-openai
  %(prog)s  # Interactive mode
        """
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        help='Prompt to process (if not provided, enters interactive mode)'
    )
    
    parser.add_argument(
        '--use-openai',
        action='store_true',
        help='Use OpenAI API for responses (requires OPENAI_API_KEY environment variable)'
    )
    
    args = parser.parse_args()
    
    # Check if OpenAI is requested but key is not available
    if args.use_openai and not os.environ.get('OPENAI_API_KEY'):
        print("Warning: --use-openai specified but OPENAI_API_KEY not found in environment", 
              file=sys.stderr)
        print("Falling back to template responses", file=sys.stderr)
    
    # Single prompt mode
    if args.prompt:
        result = process_prompt(args.prompt, args.use_openai)
        print(json.dumps(result, indent=2))
        return
    
    # Interactive mode
    print("AI Agent Simulator - Interactive Mode")
    print("=" * 50)
    print("Enter prompts to get categorized responses.")
    print("Type 'quit' or 'exit' to end session.")
    print(f"OpenAI API: {'Enabled' if args.use_openai else 'Disabled'}")
    if args.use_openai and os.environ.get('OPENAI_API_KEY'):
        print("✓ OPENAI_API_KEY found")
    print("=" * 50)
    print()
    
    while True:
        try:
            prompt = input("Enter prompt: ").strip()
            
            if not prompt:
                continue
                
            if prompt.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            result = process_prompt(prompt, args.use_openai)
            print("\nResult:")
            print(json.dumps(result, indent=2))
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
