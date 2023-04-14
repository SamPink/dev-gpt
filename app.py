import devgpt.prompts.config as config
import devgpt.prompts.tasks as tasks
from devgpt import GPT4

# Create a GPT4 instance
gpt4 = GPT4(config.OPENAI_API_KEY)

task = """
make a grpah showing the most popular cars in the world, uuse a piblic api to get the data
"""
gpt4.start_project(task)

# Prompt the user to add more messages until they enter "quit" or "exit"
while True:
    message_text = input("Enter a new message (or type 'quit' to exit): ")
    if message_text.lower() in ["quit", "exit"]:
        break

    gpt4.add_message(message_text)

    # Generate and save response
    gpt4.generate_and_save_response()

    # Run code and add output to messages
    gpt4.run_code_and_add_output_to_messages()