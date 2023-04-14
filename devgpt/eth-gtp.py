import devgpt.prompts.config as config
import devgpt.prompts.tasks as tasks
from devgpt import GPT4

# Create a GPT4 instance
gpt4 = GPT4(config.OPENAI_API_KEY)

gpt4.add_message(tasks.system_message, role="system")

gpt4.session.project_name = "eth-gtp"
gpt4.session.create_output_folder()

task_eth = """
your goal is to make as much eth as possible,

INFURA

start by creating a wallet,

example curl --url https://mainnet.infura.io/v3/f4149201e122477882ce3ec91ed8a37b \
-X POST \
-H "Content-Type: application/json" \
-d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

now connect to the blockchain

"""

output_saved = False

gpt4.add_message(task_eth.replace("INFURA", config.INFURA), role="user")

# Prompt the user to add more messages until they enter "quit" or "exit"
while True:
    message_text = input("Enter a new message (or type 'quit' to exit): ")
    if message_text.lower() in ["quit", "exit"]:
        break

    gpt4.add_message(message_text)

    if not output_saved:
        gpt4.extract_filename_from_query(str(gpt4.session.messages[-1]))
        output_saved = True

    # Generate and save response
    gpt4.generate_and_save_response()

    # Run code and add output to messages
    gpt4.run_code_and_add_output_to_messages()

# Save session
gpt4.session.save_to_file("session.json")
