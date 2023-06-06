import re
import subprocess
from venv import create
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class PythonDevAssistant:
    def __init__(self):
        self.venv_dir = "./temp"
        self.create_venv()
        self.chat = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0, model='gpt-4')
        self.messages = [SystemMessage(content=self.get_system_message())]

    def get_system_message(self):
        return """
            Act as a senior python dev and provide code 
            try write as few lines of code as possible while writing pythonic code 
            output the following format: 
            ```bash
            (required dependencies)
            ```
            ```python
            imports 
            def main():
                code
            if __name__ == "__main__":
                main()
            ```
            the code should be in a single file that can be run from main.
            NEVER try to import any local files, 
            NEVER try to use any external APIs that require a key. Only use publicly available data.
            Follow all of these rules exactly or the code will not run.
        """

    def create_venv(self):
        create(self.venv_dir, with_pip=True)

    def extract_code(self, response: str):
        return {t: re.findall(fr"```{t}\s*([\s\S]*?)```", response) for t in ["python", "bash"]}

    def add_msg(self, message, role="human"):
        self.messages.append(HumanMessage(content=message) if role == "human" else SystemMessage(content=message))

    def install_deps(self, dependencies):
        for dep in dependencies:
            subprocess.check_call([f"{self.venv_dir}/bin/python", "-m"] + dep.split())

    def run_script(self, script_path):
        return subprocess.run([f"{self.venv_dir}/bin/python", script_path], capture_output=True, text=True, check=True)

    def generate_code(self, prompt: str, attempts=5):
        self.add_msg(prompt)
        for _ in range(attempts):
            code = self.extract_code(self.chat(self.messages).content)
            self.install_deps(code["bash"])

            with open("temp.py", "w") as f:
                f.write(code["python"][0])

            try:
                return self.run_script("temp.py").stdout
            except subprocess.CalledProcessError:
                self.add_msg(f"I got an error when running the code. Can you help me fix it?")

        raise ValueError("Max attempts reached. Unable to generate valid code.")



if __name__ == "__main__":
    assistant = PythonDevAssistant()
    print(assistant.generate_code("""
        get the price of eth for the last 2 years, 
        then use that to predict the price for the next week. show the predicted price on the same graph
        show all your findings
    """))
