#!/usr/bin/env python3
"""
Tkinter GUI for AI Agent Simulator.
Provides a simple graphical interface for prompt categorization and response generation.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import os

# Add parent directory to path to import ai_agent module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agent.agent import categorize_prompt, generate_response


class AgentGUI:
    """Main GUI application class."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("AI Agent Simulator")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Variables
        self.use_openai_var = tk.BooleanVar(value=False)
        self.current_category = tk.StringVar(value="")
        
        # Create UI elements
        self.create_widgets()
        
        # Check for OpenAI API key
        self.check_openai_status()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Title
        title_label = tk.Label(
            self.root, 
            text="AI Agent Simulator", 
            font=("Arial", 18, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Enter your prompt below and click 'Categorize' or 'Respond'",
            font=("Arial", 10),
            fg="gray"
        )
        instructions.pack()
        
        # Input frame
        input_frame = tk.Frame(self.root, pady=10)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        input_label = tk.Label(input_frame, text="Prompt:", font=("Arial", 11, "bold"))
        input_label.pack(anchor=tk.W)
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame, 
            height=6, 
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Category display
        category_frame = tk.Frame(self.root, pady=5)
        category_frame.pack(fill=tk.X, padx=20)
        
        category_label = tk.Label(category_frame, text="Category:", font=("Arial", 11, "bold"))
        category_label.pack(side=tk.LEFT)
        
        self.category_display = tk.Label(
            category_frame, 
            textvariable=self.current_category,
            font=("Arial", 10),
            fg="blue",
            anchor=tk.W
        )
        self.category_display.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Response frame
        response_frame = tk.Frame(self.root, pady=10)
        response_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        response_label = tk.Label(response_frame, text="Response:", font=("Arial", 11, "bold"))
        response_label.pack(anchor=tk.W)
        
        self.response_text = scrolledtext.ScrolledText(
            response_frame, 
            height=8, 
            wrap=tk.WORD,
            font=("Arial", 10),
            state=tk.DISABLED
        )
        self.response_text.pack(fill=tk.BOTH, expand=True)
        
        # Control frame
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(fill=tk.X, padx=20)
        
        # OpenAI checkbox
        self.openai_checkbox = tk.Checkbutton(
            control_frame,
            text="Use OpenAI",
            variable=self.use_openai_var,
            font=("Arial", 10)
        )
        self.openai_checkbox.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(
            control_frame,
            text="",
            font=("Arial", 9),
            fg="gray"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Buttons frame
        button_frame = tk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT)
        
        categorize_btn = tk.Button(
            button_frame,
            text="Categorize",
            command=self.categorize,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=5
        )
        categorize_btn.pack(side=tk.LEFT, padx=5)
        
        respond_btn = tk.Button(
            button_frame,
            text="Respond",
            command=self.respond,
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            padx=15,
            pady=5
        )
        respond_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_all,
            font=("Arial", 10),
            padx=15,
            pady=5
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def check_openai_status(self):
        """Check if OpenAI API key is available."""
        if os.environ.get('OPENAI_API_KEY'):
            self.status_label.config(text="✓ OpenAI API Key detected", fg="green")
        else:
            self.status_label.config(text="✗ No OpenAI API Key (using templates)", fg="orange")
    
    def get_prompt(self):
        """Get prompt from input text widget."""
        return self.input_text.get("1.0", tk.END).strip()
    
    def categorize(self):
        """Categorize the current prompt."""
        prompt = self.get_prompt()
        
        if not prompt:
            messagebox.showwarning("No Input", "Please enter a prompt first.")
            return
        
        try:
            category = categorize_prompt(prompt)
            self.current_category.set(category)
            self.status_label.config(text=f"Categorized as: {category}", fg="blue")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to categorize: {str(e)}")
    
    def respond(self):
        """Generate a response for the current prompt."""
        prompt = self.get_prompt()
        
        if not prompt:
            messagebox.showwarning("No Input", "Please enter a prompt first.")
            return
        
        try:
            # Categorize first if not already done
            if not self.current_category.get():
                category = categorize_prompt(prompt)
                self.current_category.set(category)
            else:
                category = self.current_category.get()
            
            # Generate response
            use_openai = self.use_openai_var.get()
            response, used_openai = generate_response(prompt, category, use_openai)
            
            # Display response
            self.response_text.config(state=tk.NORMAL)
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert("1.0", response)
            self.response_text.config(state=tk.DISABLED)
            
            # Update status
            if used_openai:
                self.status_label.config(text="✓ Response from OpenAI", fg="green")
            else:
                self.status_label.config(text="Response from template", fg="blue")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate response: {str(e)}")
    
    def clear_all(self):
        """Clear all text fields."""
        self.input_text.delete("1.0", tk.END)
        self.current_category.set("")
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete("1.0", tk.END)
        self.response_text.config(state=tk.DISABLED)
        self.status_label.config(text="Cleared", fg="gray")


def main():
    """Main entry point for GUI."""
    root = tk.Tk()
    app = AgentGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
