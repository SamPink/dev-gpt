import json
import subprocess
import time
import uuid
import openai
import re
import os
from typing import List, Dict
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
            
    def get_project_list(self):
        return [
            project
            for project in os.listdir(self.output_folder)
            if os.path.isdir(os.path.join(self.output_folder, project))
        ]

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
        
        

