import tkinter as tk
from tkinter import messagebox

class App:
    def __init__(self, master):
        self.master = master
        master.title("AI Agent Simulator")

        self.label = tk.Label(master, text="Welcome to the AI Agent Simulator!")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.button = tk.Button(master, text="Run Simulation", command=self.run_simulation)
        self.button.pack()

    def run_simulation(self):
        input_text = self.entry.get()
        messagebox.showinfo("Simulation Result", f"Running simulation with input: {input_text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()