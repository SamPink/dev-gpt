# dev-gpt

## About
*Currently the best way to use dev-gpt is through the Jupyter notebook called dev-gpt*

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

1. Clone this repository: `git clone https://github.com/SamPink/dev-gpt.git
2. Change into the cloned directory: `cd gpt-4-python-code-generator`
3. Install the required libraries: `pip install -r requirements.txt`
4. Set up an environment variable for the OpenAI API key: `export OPENAI_API_KEY=your_api_key_here`

## Usage

To use the `dev-gpt` CLI application, follow the steps outlined below:

1. Begin by launching the CLI app using the command `python cli.py --api_key your_api_key`.

2. You will be asked to enter a message. This message serves as a prompt for GPT-4. An example input could be: 

    ```
    Enter a new message (or type 'quit' to exit): Write a Python function to find the factorial of a given number.
    ```

3. GPT-4 will respond by generating a code snippet. Additionally, it will provide instructions on how to execute the generated code. This information will be presented in the following format:

    ```
    (required dependencies)
    (Python code)
    ```

    Guidance on how to execute the code will follow.

4. The application will save the generated code to a file and run it. Any output from the execution will be displayed in the CLI.

5. In the event of any errors in the code, the app will provide assistance in rectifying them and generate a fresh response.

6. To end the CLI session, simply type `quit` or `exit`.

7. All session data will be saved in a JSON file named `session.json`.

## Example

This is a sample interaction with the CLI application:

```
$ python cli.py --api_key your_api_key
Enter a new message (or type 'quit' to exit): "Write a Python function to find the factorial of a given number."
```
```python
#GPT-4 Response:

def factorial(n: int) -> int:
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
```

Then to run the code, you could call the `factorial` function with an integer argument, like `factorial(5)`.

```
$ python cli.py --api_key your_api_key
Enter a new message (or type 'quit' to exit): "Run the factorial function with the input 5."
```
```bash
#GPT-4 Response:

I ran the code and this is the output:
Factorial of 5 is: 120
```
