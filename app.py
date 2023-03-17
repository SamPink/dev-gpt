import subprocess
import time
import openai
import config
import re
import os
import json
from typing import List, Dict, Union
import tkinter as tk
from tkinter import ttk
from datetime import datetime


class GPT4:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.messages = []
        openai.api_key = self.api_key
        self.output_folder = "output"

        # Create output folder if it doesn't exist
        os.makedirs(self.output_folder, exist_ok=True)

    def log_message(self, message: str, role: str = "user"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} [{role.upper()}] {message}"
        print(log_message)
        with open("logs.txt", "a") as log_file:
            log_file.write(log_message + "\n")

    def add_message(self, message: str, role: str = "user"):
        self.messages.append({"role": role, "content": message})
        self.log_message(message, role)

    def create_chat_completion(self, messages: List[Dict[str, str]] = None) -> str:
        self.log_message("Waiting for GPT response...", "system")
        start_time = time.time()

        resp = openai.ChatCompletion.create(model=self.model, messages=messages or self.messages)

        response = resp["choices"][0]["message"]["content"]
        self.add_message(response, "assistant")

        end_time = time.time()
        elapsed_time = end_time - start_time
        self.log_message(f"GPT response received in {elapsed_time:.2f} seconds", "system")

        return response

    def extract_code_from_response(self, response: str) -> Dict[str, List[str]]:
        code_blocks = re.findall(r"```(?:python|bash)?\s*[\s\S]*?```", response)

        extracted_code = {"python": [], "bash": []}

        for code_block in code_blocks:
            code_type, code = re.match(
                r"```(python|bash)?\s*([\s\S]*?)```", code_block
            ).groups()
            code_type = code_type or "python"
            extracted_code[code_type].append(code.strip())

        return extracted_code

    def extract_filename_from_query(self, response: str) -> str:
        return self.create_chat_completion([{"role": "user", "content": f"genrrate file name for this project make sure its a valide windows foldername: {response}"}])[:-1]

    
    def write_message_to_file(self, filename: str, message: str):
        code = self.extract_code_from_response(message)
        if code:
            with open(filename, "w") as f:
                f.write("\n".join(code["python"]))

    def install_dependencies(self, dependencies: List[str]):
        for dep in dependencies:
            os.system(dep)

    def generate_and_save_response(self, output_filename: str):
        response = self.create_chat_completion()
        self.write_message_to_file(output_filename, response)
        code = self.extract_code_from_response(response)
        self.install_dependencies(code["bash"])

    def run_code_and_add_output_to_messages(self, filename: str):
        while True:
            result = subprocess.run(
                ["python", filename], capture_output=True, text=True
            )
            output = result.stdout.strip()
            error = result.stderr.strip()

            if error:
                self.add_message(
                    "The following error occurred while running the code:", "system"
                )
                self.add_message(error, "system")
                self.add_message("Please help me fix the error in the code.")

                output_filename = f"{self.output_folder}/{len(self.messages)}.py"
                self.generate_and_save_response(output_filename)
                self.write_message_to_file(filename, self.messages[-1]["content"])
            else:
                if output:
                    self.add_message("I ran the code and this is the output:", "system")
                    self.add_message(output, "system")
                break


class GPT4UI:
    def __init__(self, gpt4_instance):
        self.gpt4 = gpt4_instance
        self.root = tk.Tk()
        self.root.title("GPT-4 Assistant")
        self.create_widgets()

    def create_widgets(self):
        mainframe = ttk.Frame(self.root, padding="5")
        mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        query_label = ttk.Label(mainframe, text="Choose a query:")
        query_label.grid(column=0, row=0, sticky=tk.W)

        self.query_var = tk.StringVar()
        query_options = [
            "create a python doodle jump game using pygame",
            "Custom"
        ]
        query_dropdown = ttk.OptionMenu(
            mainframe, self.query_var, query_options[0], *query_options
        )
        query_dropdown.grid(column=0, row=1, sticky=(tk.W, tk.E))

        self.query_entry = ttk.Entry(mainframe, width=80)
        self.query_entry.grid(column=0, row=2, sticky=(tk.W, tk.E))

        submit_button = ttk.Button(
            mainframe, text="Submit", command=self.submit_query
        )
        submit_button.grid(column=1, row=2, sticky=tk.W)

        self.message_display = tk.Text(
            mainframe, wrap=tk.WORD, width=80, height=20
        )
        self.message_display.grid(column=0, row=3, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.update_message_display()

    def submit_query(self):
        selected_query = self.query_var.get()
        if selected_query == "Custom":
            user_query = self.query_entry.get()
        else:
            user_query = selected_query

        self.query_entry.delete(0, tk.END)
        self.gpt4.add_message(user_query)
        
        folder_name = self.gpt4.extract_filename_from_query(user_query)
        
        query_folder = f"{self.gpt4.output_folder}/{folder_name}"
        
        os.makedirs(query_folder, exist_ok=True)

        output_filename = f"{query_folder}/code.py"
        self.gpt4.generate_and_save_response(output_filename)
        self.gpt4.run_code_and_add_output_to_messages(output_filename)
        self.update_message_display()

    def update_message_display(self):
        self.message_display.delete(1.0, tk.END)
        for message in self.gpt4.messages:
            self.message_display.insert(
                tk.END, f"{message['role'].capitalize()}: {message['content']}\n"
            )
        self.message_display.see(tk.END)  # Scroll to the bottom

    def run(self):
        self.root.mainloop()
        

if __name__ == "__main__":
    gpt4 = GPT4(config.OPENAI_API_KEY)
    gpt4.add_message(
        "Please provide a code snippet in the following format:\n\n"
        "```bash\n(required dependencies)\n```\n\n"
        "```python\n(Python code)\n```\n\n"
        "And also suggest a filename in the following format:\n"
        "file name: ([\\w\\-]+)",
        role="system",
    )
    
    gpt4.add_message(
        "always follow these rules exactly or the code will not work dont output any aditional text",
        role="system",
    )
    

    gpt4_ui = GPT4UI(gpt4)
    gpt4_ui.run()