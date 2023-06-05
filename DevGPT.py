import os
import re
import subprocess
from typing import Dict, List
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


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
        self.chat = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0, model='gpt-4')
        self.messages = [
            SystemMessage(content=self.system_message),
        ]

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

    def add_message_to_chat(self, message, role="human"):
        if role == "human":
            self.messages.append(HumanMessage(content=message))
        elif role == "system":
            self.messages.append(SystemMessage(content=message))

    def install_dependencies(self, dependencies: List[str]):
        for dep in dependencies:
            os.system(dep)

    def generate_code(self, prompt: str, max_attempts=5):
        attempt = 0
        self.add_message_to_chat(prompt)

        while attempt < max_attempts:
            attempt += 1

            resp = self.chat(self.messages)
            code = self.extract_code_from_response(resp.content)
            self.install_dependencies(code["bash"])

            # Write the code to a temporary Python file
            with open("temp.py", "w") as f:
                f.write(code["python"][0])

            try:
                # Execute the Python file and capture the output
                result = subprocess.run(
                    ["python", "temp.py"], capture_output=True, text=True, check=True
                )
                return result.stdout

            except subprocess.CalledProcessError as e:
                error_message = f"I got this error when running the code can you help me fix it. remember to always output the full code and listen to the system message: {e.stderr}"
                self.add_message_to_chat(error_message)
                if attempt == max_attempts:
                    raise ValueError(
                        "Max attempts reached. Unable to generate valid code."
                    )


if __name__ == "__main__":
    assistant = PythonDevAssistant()
    print(assistant.generate_code("create a siple pygame"))