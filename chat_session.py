import json
import copy
from telegram.ext import Updater, MessageHandler, Filters

class ChatSession:
    
    __latestTime = 0
    __messageList = []
    config_dict = {}
    
    def __init__(self, contactTime, message):
        # first message
        self.__messageList = copy.deepcopy([])
        self.__latestTime = contactTime
        self.__messageList.append(
            {"role": "user", "content": message}
        )
        # load config
        with open("config.json") as f:
            self.config_dict = json.load(f)
            
    def __repr__(self):
        return str(self.messageList) + '\n'
    
    @property
    def messageList(self):
        return self.__messageList
    
    def update(self, contactTime, message, source):
        # check time
        if (source == "user") and (contactTime - self.__latestTime > self.config_dict["wait_time"]) :
            # refresh message list
            self.__messageList.clear()
        self.__latestTime = contactTime
        self.__messageList.append(
            {"role": source, "content": message}
        )
        
    def clear_context(self, clear_time):
        self.__latestTime = clear_time
        self.__messageList.clear()
        
def handle_message(update, context):
    message_text = update.message.text
    chat_id = update.message.chat_id
    contact_time = update.message.date.timestamp()
    
    # check if chat session exists
    if chat_id in context.chat_data:
        # update existing session
        session = context.chat_data[chat_id]
        session.update(contact_time, message_text, "user")
    else:
        # create new session
        session = ChatSession(contact_time, message_text)
        context.chat_data[chat_id] = session
        
    # do something with the user's message here
    # for example, send a response back
    response_text = "Thanks for your message: " + message_text
    context.bot.send_message(chat_id, response_text)
    
def main():
    # load config
    with open("config.json") as f:
        config_dict = json.load(f)
        
    # create an updater and dispatcher for handling messages
    updater = Updater(token=config_dict["bot_token"], use_context=True)
    dispatcher = updater.dispatcher
    
    # add a message handler to the dispatcher
    message_handler = MessageHandler(Filters.text & ~Filters.command, handle_message)
    dispatcher.add_handler(message_handler)
    
    # start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
