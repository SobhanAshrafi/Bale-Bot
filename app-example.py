from lib import App,Updater,Updates_controller,Bot
import logging



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logging.getLogger(__name__)


app = App(token = "Token")




@app.updates_controller.message_handler('/start')
def start_command(context):
    text = 'سلام به ربات *** خوش آمدید'
    app.bot.send_text(chat_id="chat_id", text=text)
    

@app.updates_controller.message_handler('echo.+',use_re_filter=True)
def echo(context):

    app.bot.send_text(chat_id="chat_id",text=context['text'][4:])    







app.run()



