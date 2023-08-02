from lib import App,Updater,Updates_controller,Bot
import logging



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logging.getLogger(__name__)


app = App(token = "811876770:Qnwb52SDgE14QdiWDUKziKm4kvjPmBMcjsofyuNo")




@app.updates_controller.message_handler('/start')
def start_command(context):
    text = 'سلام به ربات \یام ناشناس خوش آمدید'
    app.bot.send_text(chat_id=658937530, text=text)
    

@app.updates_controller.message_handler('echo.+',use_re_filter=True)
def echo(context):

    app.bot.send_text(chat_id=658937530,text=context['text'][4:])    







app.run()


