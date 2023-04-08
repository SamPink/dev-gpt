# dev-gpt

## How to use
Currently the best way to use dev-gpt is through the Jupyter notebook called dev-gpt

This command-line interface (CLI) app uses OpenAI's GPT-4 to automatically write Python code based on a given prompt. It allows users to interact with GPT-4, request code snippets, save the code to files, and run the generated code. The app also extracts and installs required dependencies and handles potential code execution errors.

## Features

- Interact with GPT-4 through a command-line interface
- Automatically generate Python code based on user input
- Extract and install required dependencies
- Save generated code to a file
- Run generated code and display the output
- Error handling for code execution
- Save the session information in JSON format

## Requirements

- Python 3.6+
- `openai` library (install via `pip install openai`)
- An OpenAI API key (obtain from [OpenAI](https://beta.openai.com/signup/))

## Installation

1. Clone this repository: `git clone https://github.com/SamPink/gpt-4-python-code-generator.git`
2. Change into the cloned directory: `cd gpt-4-python-code-generator`
3. Install the required libraries: `pip install -r requirements.txt`
4. Set up an environment variable for the OpenAI API key: `export OPENAI_API_KEY=your_api_key_here`

## Usage

1. Run the CLI app: `python cli.py --api_key your_api_key`
2. Enter a message to provide a prompt for GPT-4. For example:

```
Enter a new message (or type 'quit' to exit): Write a Python function to find the factorial of a given number.
```

3. GPT-4 generates a response with the code snippet and provides instructions on how to run the code. The response will be in the following format:

```
```bash
(required dependencies)
```

```python
(Python code)
```

Provide instructions on how to run the code in the response.
```

4. The app saves generated code to a file and runs the code. Any output is displayed in the CLI.

5. If there are any errors in the code, the app asks for help to fix the errors and generates a new response.

6. To exit the CLI, type `quit` or `exit`.

7. The session information is saved in a JSON file named `session.json`.

## Example

```
$ python cli.py --api_key your_api_key
Enter a new message (or type 'quit' to exit): Write a Python function to find the factorial of a given number.

GPT-4 Response:
```bash
```

```python
def factorial(n: int) -> int:
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
```

To run the code, call the `factorial` function with an integer argument, like `factorial(5)`.

$ python cli.py --api_key your_api_key
Enter a new message (or type 'quit' to exit): Run the factorial function with the input 5.
I ran the code and this is the output:
Factorial of 5 is: 120
```
