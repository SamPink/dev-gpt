import os
import re
import traceback
import subprocess

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage


class PythonDevAssistant:
    def __init__(self):
        load_dotenv()
        self.system_message = """
        Act as a senior python dev and provide code in the following format: 

        ```bash
        (required dependencies)
        ```

        ```python
        (Python code)
        ```

        the code should be in a single file that can be run from main.
        never try to import any local files, or external apis that require a key.
        the code should run without any aditional configuration.
        follow all of these rules exactly or the code will not run.
        """
        self.chat = ChatOpenAI(temperature=0)
        self.messages = [
            SystemMessage(content=self.system_message),
        ]

    def extract_code_from_response(self, response: str):
        code_blocks = re.findall(r"```(?:python|bash)?\s*[\s\S]*?```", response)
        return next(
            (
                re.match(r"```(python|bash)?\s*([\s\S]*?)```", code_block).groups()[1]
                for code_block in code_blocks
                if "python" in code_block
            ),
            "",
        )

    def add_message_to_chat(self, message, role="human"):
        if role == "human":
            self.messages.append(HumanMessage(content=message))
        elif role == "system":
            self.messages.append(SystemMessage(content=message))

    def generate_code(self, prompt: str, max_attempts=5):
        attempt = 0
        self.add_message_to_chat(prompt)

        while attempt < max_attempts:
            attempt += 1

            resp = self.chat(self.messages)
            code = self.extract_code_from_response(resp.content)

            # Write the code to a temporary Python file
            with open("temp.py", "w") as f:
                f.write(code)

            try:
                # Execute the Python file and capture the output
                result = subprocess.run(
                    ["python", "temp.py"], capture_output=True, text=True, check=True
                )
                print(result.stdout)  # Print the output of the executed code

                self.add_message_to_chat(
                    f"the result of running the code is: {result.stdout}"
                )
                break  # If the code executes successfully, break the loop
            except subprocess.CalledProcessError as e:
                error_message = f"I got this error when running the code can you help me fix it. remember to always output the full code and listen to the system message: {e.stderr}"

                self.add_message_to_chat(error_message)
                if attempt == max_attempts:
                    print("Max attempts reached. Unable to generate valid code.")


if __name__ == "__main__":
    assistant = PythonDevAssistant()
    assistant.generate_code("get the last house sold in england and print the price")
