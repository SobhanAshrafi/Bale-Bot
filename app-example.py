from lib import App
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.getLogger(__name__)


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

