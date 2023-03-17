import openai
import config
import re
import subprocess

class GPT4:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.messages = []
        openai.api_key = self.api_key

    def add_message(self, message: str, role: str = "user"):
        self.messages.append({"role": role, "content": message})

    def create_chat_completion(self):
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
        )
        response = resp['choices'][0]['message']['content']
        self.add_message(response, "assistant")
        return response

    def extract_code_from_response(self, response: str):
        code_pattern = re.compile(r'```(?:python)?\s*(.*?)```', re.DOTALL)
        match = code_pattern.search(response)
        if match:
            return match.group(1)
        return None

    def write_message_to_file(self, filename: str, message: str):
        code = self.extract_code_from_response(message)
        if code:
            with open(filename, "w") as f:
                f.write(code)

    def generate_and_save_response(self, output_filename: str):
        response = self.create_chat_completion()
        self.write_message_to_file(output_filename, response)

    def run_code_and_add_output_to_messages(self, filename: str):
        result = subprocess.run(['python', filename], capture_output=True, text=True)
        output = result.stdout.strip()
        if output:
              #add a message saying I run the code and this is the output
            self.add_message("I ran the code and this is the output:", "system")
            self.add_message(output, "system")

if __name__ == "__main__":
    gpt4 = GPT4(config.OPENAI_API_KEY)
    
    # Ask GPT-4 to act as a data engineer
    gpt4.add_message("Act as a data engineer.", role="system")
    
    # Ask GPT-4 to write Python code
    gpt4.add_message("Write a Python script to read a rest api and print its contents.")
    gpt4.add_message("get the price of eth in usd")
    
    #create a folder called output and add a file called output.py
    output_filename = "output/output.py"
    gpt4.generate_and_save_response(output_filename)
    gpt4.run_code_and_add_output_to_messages(output_filename)
