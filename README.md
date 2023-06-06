# PythonDevAssistant

PythonDevAssistant is your on-demand Python developer that empowers you to create Python applications instantly. Our vision is to make software development seamless and accessible to all. With PythonDevAssistant, everyone can become a developer without needing to master complex programming languages. This script contains a minimal working example of our solution.

## demo app, this full web app with real time crypto proces was created with just a prompt
https://github.com/SamPink/dev-gpt/assets/42603236/9840122b-5e1a-4108-b610-8aac75288efb


![Simple weather app](https://github.com/SamPink/dev-gpt/assets/42603236/2f192127-bcb4-43f4-8770-ee95c69e2b61)


## Introduction

PythonDevAssistant is more than a tool—it's a creative partner. From creating games to setting up complex data analysis tools, PythonDevAssistant has you covered. Whether you're a startup looking to quickly validate your ideas, a researcher in need of custom tools, or a business seeking to automate your workflows, PythonDevAssistant is your solution.

How it Works

The PythonDevAssistant class is the core of this minimal working example. When instantiated, it sets up a chat interface with an OpenAI model, primed to act as a senior Python developer. It accepts prompts in natural language and generates Python code in response. The generated code is designed to be self-contained and easily executable, with no dependencies on local files or external APIs requiring a key.

Using PythonDevAssistant

You can run the PythonDevAssistant as a standalone Python program. Simply create an instance of the class and call the generate_code method with a prompt of your choice. For example:

```python
assistant = PythonDevAssistant()
assistant.generate_code("plot some cool data")
```

The generate_code method attempts to generate a valid Python code snippet in response to the prompt. If the code fails to execute, the method will automatically ask the model for a fix and attempt to execute the fixed code. This process repeats until the code runs successfully or the maximum number of attempts is reached.

Requirements

To run PythonDevAssistant, you will need Python 3.6 or later and the dotenv package installed. The dotenv package is used to load environment variables from a .env file in your project root, which should contain your OpenAI API key.

Goals and Future Work

This minimal working example represents the first step in our journey to revolutionize software development and democratize programming. As we continue to develop PythonDevAssistant, we plan to expand its capabilities and make it even easier to use. We envision a future where anyone, regardless of their coding experience, can rapidly prototype applications, set up data pipelines, create interactive visualizations, and automate routine tasks.

Feedback and Contributions

We welcome feedback and contributions from the community. Please feel free to open an issue or submit a pull request. Together, we can build the future of code generation.

Disclaimer

This is a minimal working example (MWE) and should be used with that in mind. It may have bugs and limitations, and we are constantly working to improve it. Please use this responsibly and provide us with feedback so we can make it better.

Note: This script and its content are intended for educational and research purposes only. The use of the code and/or information present in this script is the sole responsibility of the user. The maintainers of this script are not responsible for any damage, loss, or violation of any kind caused by the use or misuse of the code or information from this script.
