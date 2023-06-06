TWITTER_APP = """
        create a twiter clone using fastapi and sqlite
        remember it needs to run from main
        so import uvicorn and run it from main
        """

ETH_PRICE = """
        predict the price of the eth next week, 
        generate a detailed dash app with your research and calculations
        """

MAKE_BLOCKCHAIN = """
create a simple blockchain using python
        include standard blockchain features 
        create a fastapi app that can interact with the blockchain
        remember it needs to run from main so import uvicorn and run it from main
"""

SYSTEM_MESSAGE= """
Task:
Act as a senior python dev and provide code.

rules:
the code should be in a single file that can be run from main.
try write pythonic code.
remember to think step by step to solve the problem.

output format: 
```bash
pip install dependencies
```
```python
imports 
def main():
    code
if __name__ == "__main__":
main()
```
        
Follow all of these rules exactly or the code will not run!
"""