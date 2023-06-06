import re, subprocess
from venv import create
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from prompts import SYSTEM_MESSAGE

class PythonDevAssistant:
    def __init__(self):
        load_dotenv()
        self.venv_dir= "./temp"
        self.chat, self.messages =  self.initialize_chat(), [SystemMessage(content=SYSTEM_MESSAGE)]

    def initialize_chat(self):
        self.create_venv()
        return ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0, model="gpt-4")

    def create_venv(self):
        create(self.venv_dir, with_pip=True)

    def add_msg(self, message, role="human"):
        self.messages.append(HumanMessage(content=message) if role == "human" else SystemMessage(content=message))

    def extract_code(self, response: str):
        return {t: re.findall(rf"```{t}\s*([\s\S]*?)```", response) for t in ["python", "bash"]}

    def install_deps(self, dependencies):
        for dep in dependencies: subprocess.check_call([f"{self.venv_dir}/bin/python", "-m"] + dep.split())

    def run_script(self, script_path):
        return subprocess.run([f"{self.venv_dir}/bin/python", script_path], capture_output=True, text=True, check=True)

    def generate_code(self, prompt: str, attempts=5):
        self.add_msg(prompt)
        for _ in range(attempts):
            code = self.extract_code(self.chat(self.messages).content)
            self.install_deps(code["bash"])
            self.add_msg(f"this is the code generated: {code['python'][0]}")
            with open("temp.py", "w") as f: f.write(code["python"][0])
            try:
                output = self.run_script("temp.py").stdout
                print(output)
                improvement = input("How can I improve the code? enter the code or type 'no' to finish:")
                if improvement == "no": return output
                self.add_msg(improvement)

            except subprocess.CalledProcessError as e:
                self.add_msg(f"I got an error when running the code. Can you help me fix it? {e}")
        raise ValueError("Max attempts reached. Unable to generate valid code.")
    
if __name__ == "__main__":
    assistant = PythonDevAssistant()
    print(assistant.generate_code(input("Enter a prompt: ")))
