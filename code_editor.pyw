import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import subprocess
import sys
import os

class PythonCodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Editor")
        self.root.geometry("800x600")

        # Create a text editor area using ScrolledText widget
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier New", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # Create a menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Add File menu to menu bar
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Add Run menu to menu bar
        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(label="Run Code", command=self.run_code)

        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.current_file = file_path

    def save_file(self):
        if self.current_file:
            content = self.text_area.get(1.0, tk.END)
            with open(self.current_file, "w") as file:
                file.write(content)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.current_file = file_path

    def run_code(self):
        # Save code to a temporary file to run
        code = self.text_area.get(1.0, tk.END)

        if self.current_file:
            # Write the current text content to the file
            self.save_file()
            run_file = self.current_file
        else:
            run_file = "temp_code.py"
            with open(run_file, "w") as temp_file:
                temp_file.write(code)

        # Run the Python code and capture the output
        try:
            result = subprocess.run([sys.executable, run_file], capture_output=True, text=True, check=True)
            output = result.stdout
            if result.stderr:
                output += "\nErrors:\n" + result.stderr
        except subprocess.CalledProcessError as e:
            output = f"Error running the script:\n{e.output}"

        # Show the output in a messagebox
        messagebox.showinfo("Code Output", output)

        # Remove the temporary file if it was used
        if run_file == "temp_code.py":
            os.remove(run_file)

if __name__ == "__main__":
    root = tk.Tk()
    editor = PythonCodeEditor(root)
    root.mainloop()
