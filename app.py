from gpt import GPT4
from ui import GPT4UI

import config

if __name__ == "__main__":
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
    

    gpt4_ui = GPT4UI(gpt4)
    gpt4_ui.run()