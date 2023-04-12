import config
import tasks
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

tell me about the last nft trade
"""

gpt4.add_message(task_eth.replace("INFURA", config.INFURA), role="user")

# Generate and save response
gpt4.generate_and_save_response()
