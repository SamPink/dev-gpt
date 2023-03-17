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

    def install_dependencies(self, dependencies: list):
        for dep in dependencies:
            subprocess.run(['pip', 'install', dep])

    def generate_and_save_response(self, output_filename: str):
        response = self.create_chat_completion()
        self.write_message_to_file(output_filename, response)
        code = self.extract_code_from_response(response)
        self.install_dependencies(code["bash"])

    def run_code_and_add_output_to_messages(self, filename: str):
        result = subprocess.run(['python', filename], capture_output=True, text=True)
        output = result.stdout.strip()
        if output:
            self.add_message("I ran the code and this is the output:", "system")
            self.add_message(output, "system")

if __name__ == "__main__":
    gpt4 = GPT4(config.OPENAI_API_KEY)

    # Update the initial system message to request code in the specified format
    gpt4.add_message("Act as a data engineer and provide code in the following format: \n\n```bash\n(required dependencies)\n```\n\n```python\n(Python code)\n```\n\nProvide instructions on how to run the code in the response.", role="system")

    while True:
        user_input = input("Enter your message (type 'exit' to quit): ")

        if user_input.lower() == 'exit':
            break

        gpt4.add_message(user_input)

        output_filename = "output/output.py"
        gpt4.generate_and_save_response(output_filename)
        gpt4.run_code_and_add_output_to_messages(output_filename)

        for message in gpt4.messages[-3:]:
            print(f"{message['role'].capitalize()}: {message['content']}")
        print("\n")

