from requests import request
import re
import asyncio
import logging
import time



logging.getLogger('urllib3').propagate = False



class Bot():
    

    def __init__(self, token : str, base_url = 'https://tapi.bale.ai/') -> None:
        
        self.logger = logging.getLogger(__name__ + '.Bot')
        self._token = token
        self.base_url = base_url
        self.url = base_url + token

        self.getme()


    def safe_req(self, fun_name='safe_req', **kwargs):

        s = 0
        
        try_time = 5

        while (s != 200):

            
            try:
                res = request(**kwargs)
                s = res.status_code
            except:
                self.logger.error('Connection error! check your connection.')


            
            

            if s != 200:
                self.logger.error(f'http status_code error : {s} at function {fun_name}')
                try_time -= 1
            
            if try_time == 1:
                time.sleep(2)
                try_time = 4
        return res




    def getme(self):


        url = self.url + '/getme'

        res = self.safe_req(fun_name='getme', method='GET', url = url)
        
        if res.json()['ok'] == False:
            raise ValueError('the bot token is wrong')
            

        return res.json()



    def get_updates(self, offset = 0, limit = 0):
        url = self.url + '/getupdates'
        res = self.safe_req( fun_name='get_updates', method='GET', url = url, params={'offset':offset, 'limit':limit})
        
        return res.json()['result'] 



    def send_text(self, chat_id=658937530, text='hello guguli'):

        url = self.url + '/sendMessage'
        data = {'chat_id':chat_id, 'text':text}
        res = self.safe_req(fun_name='send_text', method='POST', url=url, data=data)




class Updates_controller(): #Dispatcher
    
    def __init__(self) -> None:
        
        self.logger = logging.getLogger(__name__ + '.Updates_controller')
        self._StrFilters_funcs = {}
        self._ReFilters_funcs = {}
        


    def msg_filter_checker(self,text):
        
        if text in list(self._StrFilters_funcs.keys()):

            call_back_func = self._StrFilters_funcs[text]
            return call_back_func

        else:

            for regEx in list( self._ReFilters_funcs.keys() ):
                result = re.compile(regEx)
                if result.match(text):
                    call_back_func = self._ReFilters_funcs[regEx]
                    return call_back_func

        return False



    async def _run(self,updates_queue):
        
        self.logger.debug('Updates_controller start running!')

        speed = 10

        while True:

            if updates_queue.qsize() == 0:
                await asyncio.sleep(0)
                continue
            
            if updates_queue.qsize() < speed :
                for i in range(updates_queue.qsize()):
                    
                    update = updates_queue.get_nowait()

                    text = update['message']['text']

                    result = self.msg_filter_checker(text=text)

                    if result:

                        try:
                            context = {'text':text, 'update':update}
                            result(context)
                        except:
                            result()


                    else:
                        continue

                await asyncio.sleep(0)
                continue



            for i in range( updates_queue.qsize()//speed ):
                for j in range(speed):
                    update = updates_queue.get_nowait()
                    text = update['message']['text']

                    result = self.msg_filter_checker(text=text)

                    if result:
                        
                        try:
                            context = {'text':text, 'update':update}
                            result(context)
                        except:
                            result()

                    else:
                        continue 

                await asyncio.sleep(0)






    def add_handler(self, filter, callback_func, use_re_filter = False):
        
        if use_re_filter == False:
            
            if filter in list(self._StrFilters_funcs.keys()):
                raise ValueError('filter is already defined!')
            else:
                self._StrFilters_funcs[filter] = callback_func

            
        else:

            if filter in list(self._ReFilters_funcs.keys()):
                raise ValueError('filter is already defined!')
            else:
                self._ReFilters_funcs[filter] = callback_func
            



    # to use with dcorators
    def message_handler(self, filter : str, use_re_filter = False):

        
        def decorator(callback_func):

            self.add_handler(filter,callback_func, use_re_filter)
            
            return callback_func


        return decorator







class Updater():

    def __init__(self,bot) -> None:
        
        self.logger = logging.getLogger(__name__ + '.Updater')
        self.bot = bot
        self.updates_queue = asyncio.Queue(maxsize=-1)
        self.offset = 244
        self.poll_interval = 1

    # the core of getting updates.
    async def _run(self):

        self.logger.debug('updater start running!')

        while True:
            updates = self.bot.get_updates(offset=self.offset)
            print(updates)

            if len(updates) == 0:
                await asyncio.sleep(self.poll_interval)
                continue

            #To Do :  divide puting updates in queue into some updates with lower than 50 len (so we will have some await if len>50)
            for update in updates:

                self.updates_queue.put_nowait(update)
                self.offset += 1

            await asyncio.sleep(self.poll_interval)          

            


    #To Do  : to run updater directly not by App.
    # def start(self,loop=asyncio.get_event_loop()):

    #     updating_task = self._run()
    #     loop.create_task(updating_task)
        



class App():

    def __init__(self, token : str, base_url = 'https://tapi.bale.ai/') -> None:
        
        self.logger = logging.getLogger(__name__ + '.App')
        self.bot = Bot(token=token,base_url=base_url)
        self.updater = Updater(bot=self.bot)
        self.updates_controller = Updates_controller()
        self.loop = asyncio.get_event_loop()
        
    


    def run(self):
        
        self.logger.debug('app start running!')
        
        #add task 1
        updating_task = self.updater._run()
        
        self.loop.create_task(updating_task)


        #add task 2
        updates_controlling_task = self.updates_controller._run(self.updater.updates_queue)

        self.loop.create_task(updates_controlling_task)


        self.loop.run_forever()





# to do 1: sometimes requests in bot funcs give error so app stops. convert this funcs to async func
# to do 2: web hook?  offset
# to do 3: add logger for app
# to do 4: add error exception for app (by an error app or part of it should not crash!)
# to do 5: add database to save users.
# to do 6: دسته بندی \یام ها وقتی آ\\دیت ها رو میگیریم٫ مثلا یک صف مخصوص تکست ها باشه یک صف مخصوص عکس ها اینجوری دیگه مشکلی برای فیلتر ها برای انواع مختلف \یش نمیاد
