from src.model.core.engine_chat import process_message

def process_message_controller(self, message):
    bot_message = process_message(self, message)
    return bot_message