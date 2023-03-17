import subprocess
import time
import openai
import config
import re
import os
import json
from typing import List, Dict, Union


class GPT4:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.messages = []
        openai.api_key = self.api_key
        self.output_folder = "output"

        # Create output folder if it doesn't exist
        os.makedirs(self.output_folder, exist_ok=True)

    def add_message(self, message: str, role: str = "user"):
        self.messages.append({"role": role, "content": message})

    def create_chat_completion(self) -> str:
        print("Waiting for GPT response...")
        start_time = time.time()

        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
        )

        response = resp['choices'][0]['message']['content']
        self.add_message(response, "assistant")

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"GPT response received in {elapsed_time:.2f} seconds")

        return response

    def extract_code_from_response(self, response: str) -> Dict[str, List[str]]:
        code_blocks = re.findall(r'```(?:python|bash)?\s*[\s\S]*?```', response)

        extracted_code = {
            "python": [],
            "bash": []
        }

        for code_block in code_blocks:
            code_type, code = re.match(r'```(python|bash)?\s*([\s\S]*?)```', code_block).groups()
            code_type = code_type or "python"
            extracted_code[code_type].append(code.strip())

        return extracted_code

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
            result = subprocess.run(['python', filename], capture_output=True, text=True)
            output = result.stdout.strip()
            error = result.stderr.strip()

            if error:
                self.add_message("The following error occurred while running the code:", "system")
                self.add_message(error, "system")
                self.add_message("Please help me fix the error in the code.")

                output_filename = f"{self.output_folder}/{len(self.messages)}.py"
                self.generate_and_save_response(output_filename)
                self.write_message_to_file(filename, self.messages[-1]['content'])
            else:
                if output:
                    self.add_message("I ran the code and this is the output:", "system")
                    self.add_message(output, "system")
                break


if __name__ == "__main__":
    gpt4 = GPT4(config.OPENAI_API_KEY)

    # Update the initial system message to request code in the specified format
    gpt4.add_message("Act as a data engineer and provide code in the following format: \n\n```bash\n(required dependencies)\n```\n\n```python\n(Python code)\n```\n\n just output the required format, nothing else.", role="system")

    gpt4.add_message('write a python script to get the current eth price in £.')

    output_filename = "output/first.py"
    gpt4.generate_and_save_response(output_filename)
    gpt4.run_code_and_add_output_to_messages(output_filename)

    gpt4.add_message('now update the script to get 30 days of historical data for eth in £')

    output_filename = "output/second.py"
    gpt4.generate_and_save_response(output_filename)
    gpt4.run_code_and_add_output_to_messages(output_filename)

    gpt4.add_message('now update the script to use sqlalchemy to write the data to a local sqllite database, get the data for the top 5 cryptos')

    output_filename = "output/third.py"
    gpt4.generate_and_save_response(output_filename)
    gpt4.run_code_and_add_output_to_messages(output_filename)

    gpt4.add_message('now update the script to use the data in the database to create a dashboard using streamlit')

    output_filename = "output/fourth.py"
    gpt4.generate_and_save_response(output_filename)
    gpt4.run_code_and_add_output_to_messages(output_filename)

    print(gpt4.messages)

