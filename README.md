# Bale Bot Library (Python)

This is a **simple and startup library** for creating bots in **Bale Messenger**.  
The goal of this project is to **learn and experiment** with topics such as:

- Writing Python modules
- Using the `requests` library
- Working with `asyncio`
- Getting and managing updates
- Filtering messages
- Using decorators for cleaner handler registration

It’s not meant to be a fully-featured or production-ready framework, but rather a **first step into the world of building Python libraries**.

---

## Features

- Lightweight, no external dependencies except `requests`.
- `Bot` class for sending messages and fetching updates.
- `Updater` for polling updates asynchronously.
- `Updates_controller` for message filtering and dispatching.
- `App` wrapper for easy setup and running.
- Simple support for **string filters** and **regex filters**.

---

## Installation

Clone this repository and install dependencies:

```bash
git clone https://github.com/SobhanAshrafi/Bale-Bot.git
cd Bale-Bot
```

---

## Quick Example

`app-example.py` shows a basic usage:

```python
from lib import App

# Initialize your bot with the provided token
app = App(token="YOUR_BOT_TOKEN_HERE")

# Register a simple /start command
@app.updates_controller.message_handler('/start')
def start_command(context):
    text = 'سلام به ربات خوش آمدید'
    app.bot.send_text(chat_id=context['update']['message']['chat']['id'], text=text)

# Echo command using regex filter
@app.updates_controller.message_handler('echo.+', use_re_filter=True)
def echo(context):
    app.bot.send_text(
        chat_id=context['update']['message']['chat']['id'],
        text=context['text'][4:]
    )

# Run the bot
app.run()
```

---

## Project Structure

```
├── lib.py            # Core library: Bot, Updater, Updates_controller, App
├── app-example.py    # Example usage
```

---

## To Do (learning goals)

- [ ] Convert requests to async (`aiohttp`).
- [ ] Add webhook support.
- [ ] Add better error handling and logging.
- [ ] Support more update types (photos, files, etc.).
- [ ] Experiment with database integration for users.

---

## License

Open-source under the MIT License.

---

👉 This library is **mainly for learning purposes** and as a **startup project** to get familiar with writing modules, working with APIs, and using async in Python.  
