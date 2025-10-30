#!/usr/bin/env python3
"""
Command-line interface for AI Agent Simulator
Accepts prompts and returns categorized responses in JSON format
"""
import argparse
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agent.agent import categorize_prompt, generate_response


def process_prompt(prompt: str, use_openai: bool = False) -> dict:
    """
    Process a single prompt and return result as dictionary.
    
    Args:
        prompt: User input prompt
        use_openai: Whether to use OpenAI API
        
    Returns:
        Dictionary with prompt, category, response, and used_openai fields
    """
    category = categorize_prompt(prompt)
    response, used_openai = generate_response(prompt, category, use_openai)
    
    return {
        "prompt": prompt,
        "category": category,
        "response": response,
        "used_openai": used_openai
    }


def interactive_mode(use_openai: bool = False):
    """Run in interactive mode, accepting prompts until user exits."""
    print("AI Agent Simulator - CLI Interface")
    print("=" * 50)
    print("Enter prompts to get categorized responses.")
    print("Type 'quit' or 'exit' to end the session.")
    print("=" * 50)
    
    if use_openai:
        if os.environ.get('OPENAI_API_KEY'):
            print("OpenAI API: ENABLED")
        else:
            print("OpenAI API: DISABLED (OPENAI_API_KEY not set)")
            use_openai = False
    else:
        print("OpenAI API: DISABLED")
    
    print()
    
    while True:
        try:
            prompt = input("Enter prompt: ").strip()
            
            if not prompt:
                continue
                
            if prompt.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            result = process_prompt(prompt, use_openai)
            print(json.dumps(result, indent=2))
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="AI Agent Simulator - Categorize prompts and generate responses"
    )
    parser.add_argument(
        '--prompt',
        type=str,
        help='Prompt to process (if not provided, runs in interactive mode)'
    )
    parser.add_argument(
        '--use-openai',
        action='store_true',
        help='Use OpenAI API for responses (requires OPENAI_API_KEY environment variable)'
    )
    
    args = parser.parse_args()
    
    if args.prompt:
        # Single prompt mode
        result = process_prompt(args.prompt, args.use_openai)
        print(json.dumps(result, indent=2))
    else:
        # Interactive mode
        interactive_mode(args.use_openai)


if __name__ == "__main__":
    main()
