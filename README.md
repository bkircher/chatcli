# ChatCLI

Quick and dirty OpenAI chat interface for the CLI.

## Steps

1. Install dependencies

    ```raw
    $ python -m venv .venv
    $ source .venv/bin/activate
    (.venv) pip install -U pip
    (.venv) pip install -r requirements.txt
    ```

2. Specify your OpenAI [API key](https://platform.openai.com/account/api-keys)

    Set `OPENAI_API_KEY` in your environment or use direnv(1) to set it in `.envrc` (see `.envrc.example`).

3. Run the script

    ```raw
    (.venv) openai/chatcli % python -m chatcli.main
    >>> Please write a simple for-loop in Common Lisp
    Here is an example of a simple for-loop in Common Lisp:

    (loop for i from 1 to 10
        do (print i))

    This loop will iterate through the numbers 1 to 10, printing each number to the console.
    >>>
    ```
