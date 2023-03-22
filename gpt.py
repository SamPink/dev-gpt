import json
import subprocess
import time
import uuid
import openai
import re
import os
from typing import List, Dict
from datetime import datetime


class Session:
    def __init__(self, project_name: str, output_folder: str = "output"):
        self.project_name = project_name
        self.output_folder = output_folder
        self.path = os.path.join(output_folder, project_name)
        self.messages = []

    def create_output_folder(self):    
        self.path = os.path.join(self.output_folder, self.project_name)
        os.makedirs(self.path, exist_ok=True)

    def save_to_file(self, filename: str = "session.json"):
        data = {
            "project_name": self.project_name,
            "output_folder": self.output_folder,
            "path": self.path,
            "messages": self.messages,
        }
        filepath = os.path.join(self.path, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_from_file(cls, filepath: str):
        with open(filepath, "r") as f:
            data = json.load(f)

        session = cls(data["project_name"], data["output_folder"])
        session.path = data["path"]
        session.messages = data["messages"]
        return session



class GPT4:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.session = Session(project_name=str(uuid.uuid4()))
        self.version = 1
        openai.api_key = self.api_key

    def log_message(self, message: str, role: str = "user"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} [{role.upper()}] {message}"
        print(log_message)
        with open("logs.txt", "a") as log_file:
            log_file.write(log_message + "\n")

    def add_message(self, message: str, role: str = "user"):
        self.session.messages.append({"role": role, "content": message})
        self.log_message(message, role)

    def create_chat_completion(self, messages: List[Dict[str, str]] = None) -> str:
        self.log_message("Waiting for GPT response...", "system")
        start_time = time.time()

        resp = openai.ChatCompletion.create(model=self.model, messages=messages or self.session.messages)

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
        name = self.create_chat_completion([{"role": "user", "content": f"generate a short file name for this project make sure its a valid windows folder name: {response}"}])[:-1]
        self.session.project_name = name
        self.session.create_output_folder()

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
        self.output_filename = os.path.join(self.session.path, f"code_v{self.version}.py")

        response = self.create_chat_completion()
        self.write_message_to_file(self.output_filename, response)
        code = self.extract_code_from_response(response)
        self.install_dependencies(code["bash"])

        self.version += 1

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
                self.write_message_to_file(self.output_filename, self.session.messages[-1]["content"])
            else:
                if output:
                    self.add_message("I ran the code and this is the output:", "system")
                    self.add_message(output, "system")
                break


if __name__ == '__main__':
    import config

    # Create a GPT4 instance
    gpt4 = GPT4(config.OPENAI_API_KEY)

    # Define the system messages
    system_messages = [
        {"text": "act as a senior python developer generate python code in the following format:\n\n"
                  "```bash\n(required dependencies)\n```\n\n"
                  "```python\n(Python code)\n```\n\n", "role": "system"},
        {"text": "always follow these rules exactly or the code will not work, dont output any additional text and always output the full code", "role": "system"}
    ]

    # Initialize an empty list of messages
    messages = []

    # Add the system messages first
    messages.extend(system_messages)
    
    output_saved = False

    # Prompt the user to add more messages until they enter "quit" or "exit"
    while True:
        message_text = input("Enter a new message (or type 'quit' to exit): ")
        if message_text.lower() in ["quit", "exit"]:
            break

        gpt4.add_message(message_text)
        
        if not output_saved:
            gpt4.extract_filename_from_query(str(gpt4.session.messages))
            output_saved = True
        

        # Generate and save response
        gpt4.generate_and_save_response()

        # Run code and add output to messages
        gpt4.run_code_and_add_output_to_messages()

    # Save session
    gpt4.session.save_to_file("session.json")
