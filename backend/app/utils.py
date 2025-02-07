import logging

# Configure logging
logging.basicConfig(filename="chatbot.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def log_message(user, message, response):
    log_data = f"User: {user} | Message: {message} | Bot: {response}"
    logging.info(log_data)