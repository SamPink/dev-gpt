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
        self.folder_name = None
        output_filename = None

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
        name = self.create_chat_completion([{"role": "user", "content": f"genrrate a short file name for this project make sure its a valide windows foldername: {response}"}])[:-1]
        self.folder_name = name
        
        return name
    

    def write_message_to_file(self, filename: str, message: str):
        code = self.extract_code_from_response(message)
        if code:
            with open(filename, "w") as f:
                f.write("\n".join(code["python"]))

    def install_dependencies(self, dependencies: List[str]):
        for dep in dependencies:
            os.system(dep)

    def generate_and_save_response(self):
        query_folder = f"{self.output_folder}/{self.folder_name}"

        os.makedirs(query_folder, exist_ok=True)

        self.output_filename = f"{query_folder}/code.py"
        
        response = self.create_chat_completion()
        self.write_message_to_file(self.output_filename, response)
        code = self.extract_code_from_response(response)
        self.install_dependencies(code["bash"])
        
        

    def run_code_and_add_output_to_messages(self):
        while True:
            result = subprocess.run(
                ["python", self.output_filename], capture_output=True, text=True
            )
            output = result.stdout.strip()
            error = result.stderr.strip()

            if error:
                self.add_message(
                    "The following error occurred while running the code:", "system"
                )
                self.add_message(error, "system")
                self.add_message("Please help me fix the error in the code.")


                self.generate_and_save_response()
                self.write_message_to_file(self.output_filename, self.messages[-1]["content"])
            else:
                if output:
                    self.add_message("I ran the code and this is the output:", "system")
                    self.add_message(output, "system")
                break
        
if __name__ == '__main__':
    import config
    gpt4 = GPT4(config.OPENAI_API_KEY)
    gpt4.add_message(
        "act as a senior python developer:\n\n"
        "```bash\n(required dependencies)\n```\n\n"
        "```python\n(Python code)\n```\n\n",
        role="system",
    )

    gpt4.add_message(
        "always follow these rules exactly or the code will not work, dont output any aditional text and always output the full code",
        role="system",
    )

    gpt4.add_message("create an application that tracks all flights in real time using a public api and plot them of a globe", role="user")

    gpt4.folder_name = gpt4.extract_filename_from_query(str(gpt4.messages))
                


    gpt4.generate_and_save_response()
    gpt4.run_code_and_add_output_to_messages()


