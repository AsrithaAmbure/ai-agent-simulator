"""
Command-Line Interface for AI Agent Simulator
"""

from agent_core import AIAgentSimulator
import sys


def print_banner():
    """Print welcome banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║         AI AGENT SIMULATOR - CLI Interface           ║
    ║                                                       ║
    ║  Type your prompts and get intelligent responses!    ║
    ║  Commands: 'quit' or 'exit' to end session          ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main CLI loop"""
    print_banner()
    
    # Ask if user wants to use OpenAI API
    use_api = input("\nUse OpenAI API? (y/n, requires API key): ").strip().lower() == 'y'
    agent = AIAgentSimulator(use_openai=use_api)
    
    print("\n✓ Agent initialized!")
    print("💡 Try different types of prompts (questions, code help, grammar checks, etc.)\n")
    
    conversation_history = []
    
    while True:
        try:
            # Get user input
            prompt = input("\n🤔 You: ").strip()
            
            # Check for exit commands
            if prompt.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n👋 Thank you for using AI Agent Simulator! Goodbye!\n")
                break
            
            if not prompt:
                print("⚠️  Please enter a prompt.")
                continue
            
            # Process the prompt
            print("\n🤖 AI Agent: Processing...", end='\r')
            result = agent.process_prompt(prompt)
            
            # Display results
            print(f"\n🤖 AI Agent [Category: {result['category'].upper()}]:")
            print(f"{result['response']}")
            print(f"\n📊 [Response Mode: {result['api_used']}]\n")
            
            # Store in history
            conversation_history.append(result)
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")
    
    # Show summary
    if conversation_history:
        print(f"\n📈 Session Summary: Processed {len(conversation_history)} prompts")


if __name__ == "__main__":
    main()