# ChatCLI

Quick and dirty OpenAI chat interface for the CLI.

## Idea

Each new CLI process is it's own new conversation. A conversation is just all
the turns (messages) in that conversation. User can use %-commands, e.g.
`%conversation new` to issue special commands that are not send to the API
directly but interpreted by the CLI itself.

The history is basically just all `user` messages in the current conversation,
followed by older conversations, interleaved by %-commands. Stored in a separate
table.

Following, the tables and their columns.

### Conversation

- id
- created_at
- system_message, a conversation can have multiple system messages and at any
  position, this is just the default for new conversations, if user does not
  specify or alter them
- max_tokens, default 1000
- model, defaults to `gpt-4` or so
- temperature, default 0.8
- choices_n (n in the API call, default 1)

What about choices here in the response?

### Message

- id
- created_at
- role, one of user, system, assistant
- name (nullable)
- content
- conversation_id, FK

### History

- id
- value, this is just what the user typed in and includes %-commands. It kind of
  duplicates the content field but also includes the %-commands
- created_at
- conversation_id, FK

## Steps

1. Install dependencies

   ```raw
   $ python -m venv .venv
   $ source .venv/bin/activate
   (.venv) pip install -U pip
   (.venv) pip install -r requirements.txt
   ```

2. Specify your OpenAI [API key](https://platform.openai.com/account/api-keys)

   Set `OPENAI_API_KEY` in your environment or use direnv(1) to set it in
   `.envrc` (see `.envrc.example`).

3. Run the script

   ```raw
   (.venv) python -m chatcli.main
   >>> Please write a simple for-loop in Common Lisp
   Here is an example of a simple for-loop in Common Lisp:

   (loop for i from 1 to 10
       do (print i))

   This loop will iterate through the numbers 1 to 10, printing each number to the console.
   >>>
   ```

## Links

- [OpenAI API docs](https://beta.openai.com/docs/api-reference/introduction)
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook)
- [Prompt Toolkit docs](https://python-prompt-toolkit.readthedocs.io/en/stable/pages/asking_for_input.html)
- [SQLite docs](https://www.sqlite.org/docs.html)
- [SQLAlchemy docs](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html)
- [Alembic migration docs](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
