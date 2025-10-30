#!/usr/bin/env python3
"""
Tkinter GUI for AI Agent Simulator
Provides a simple desktop interface for categorizing prompts and generating responses
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agent.agent import categorize_prompt, generate_response


class AgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Agent Simulator")
        self.root.geometry("700x600")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="AI Agent Simulator", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Prompt input section
        prompt_frame = ttk.LabelFrame(main_frame, text="Enter Your Prompt", padding="10")
        prompt_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        prompt_frame.columnconfigure(0, weight=1)
        
        self.prompt_text = scrolledtext.ScrolledText(prompt_frame, height=5, wrap=tk.WORD)
        self.prompt_text.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Button and options frame
        button_frame = ttk.Frame(prompt_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # OpenAI checkbox
        self.use_openai_var = tk.BooleanVar(value=False)
        openai_check = ttk.Checkbutton(button_frame, text="Use OpenAI API", 
                                       variable=self.use_openai_var,
                                       command=self.update_openai_status)
        openai_check.grid(row=0, column=0, padx=(0, 10))
        
        # OpenAI status label
        self.openai_status_label = ttk.Label(button_frame, text="", foreground="gray")
        self.openai_status_label.grid(row=0, column=1, padx=(0, 10))
        self.update_openai_status()
        
        # Buttons
        categorize_btn = ttk.Button(button_frame, text="Categorize", 
                                    command=self.categorize_only)
        categorize_btn.grid(row=0, column=2, padx=5)
        
        respond_btn = ttk.Button(button_frame, text="Respond", 
                                command=self.generate_full_response)
        respond_btn.grid(row=0, column=3, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear", 
                              command=self.clear_all)
        clear_btn.grid(row=0, column=4, padx=5)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
        # Category display
        category_frame = ttk.Frame(results_frame)
        category_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(category_frame, text="Category:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.category_label = ttk.Label(category_frame, text="", foreground="blue")
        self.category_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Response display
        ttk.Label(results_frame, text="Response:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        
        self.response_text = scrolledtext.ScrolledText(results_frame, height=12, wrap=tk.WORD, 
                                                       state=tk.DISABLED)
        self.response_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_bar = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E))
    
    def update_openai_status(self):
        """Update the OpenAI status label based on API key availability."""
        if os.environ.get('OPENAI_API_KEY'):
            self.openai_status_label.config(text="✓ API Key Set", foreground="green")
        else:
            self.openai_status_label.config(text="✗ API Key Not Set", foreground="red")
            if self.use_openai_var.get():
                self.use_openai_var.set(False)
    
    def get_prompt(self):
        """Get the current prompt from the text widget."""
        return self.prompt_text.get("1.0", tk.END).strip()
    
    def categorize_only(self):
        """Categorize the prompt without generating a response."""
        prompt = self.get_prompt()
        
        if not prompt:
            messagebox.showwarning("No Input", "Please enter a prompt first.")
            return
        
        try:
            category = categorize_prompt(prompt)
            self.category_label.config(text=category.upper())
            self.status_bar.config(text=f"Categorized as: {category}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_bar.config(text="Error during categorization")
    
    def generate_full_response(self):
        """Categorize and generate a full response."""
        prompt = self.get_prompt()
        
        if not prompt:
            messagebox.showwarning("No Input", "Please enter a prompt first.")
            return
        
        try:
            use_openai = self.use_openai_var.get()
            
            # Categorize
            category = categorize_prompt(prompt)
            self.category_label.config(text=category.upper())
            
            # Generate response
            self.status_bar.config(text="Generating response...")
            self.root.update()
            
            response, used_openai = generate_response(prompt, category, use_openai)
            
            # Display response
            self.response_text.config(state=tk.NORMAL)
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert("1.0", response)
            self.response_text.config(state=tk.DISABLED)
            
            # Update status
            api_status = "OpenAI API" if used_openai else "Template"
            self.status_bar.config(text=f"Response generated using {api_status} | Category: {category}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_bar.config(text="Error during response generation")
    
    def clear_all(self):
        """Clear all input and output fields."""
        self.prompt_text.delete("1.0", tk.END)
        self.category_label.config(text="")
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete("1.0", tk.END)
        self.response_text.config(state=tk.DISABLED)
        self.status_bar.config(text="Ready")


def main():
    """Main entry point for GUI."""
    root = tk.Tk()
    app = AgentGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
