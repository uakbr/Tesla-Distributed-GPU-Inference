# utilities.py
# Common utility functions for the Distributed Inference System across Tesla Fleet

import logging
import json
from datetime import datetime
from .config import Config

def setup_logging():
    """
    Sets up the logging configuration for the system.
    """
    logging.basicConfig(level=getattr(logging, Config.LOGGING_LEVEL),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

def log_system_activity(message, level="INFO"):
    """
    Logs system activities based on the specified level.
    :param message: Message to log.
    :param level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    logger = logging.getLogger(Config.SYSTEM_NAME)
    log_function = getattr(logger, level.lower(), logger.info)
    log_function(message)

def encrypt_data(data):
    """
    Encrypts data using the specified encryption key.
    :param data: Data to encrypt.
    :return: Encrypted data.
    """
    from cryptography.fernet import Fernet
    cipher_suite = Fernet(Config.ENCRYPTION_KEY)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    """
    Decrypts data using the specified encryption key.
    :param encrypted_data: Data to decrypt.
    :return: Decrypted data.
    """
    from cryptography.fernet import Fernet
    cipher_suite = Fernet(Config.ENCRYPTION_KEY)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

def authenticate_request(token):
    """
    Authenticates a request using the system's authentication token.
    :param token: Token to authenticate.
    :return: Boolean indicating if the authentication is successful.
    """
    return token == Config.AUTHENTICATION_TOKEN

def format_timestamp(timestamp):
    """
    Formats a timestamp into a human-readable string.
    :param timestamp: Timestamp to format.
    :return: Formatted timestamp string.
    """
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def load_json_file(file_path):
    """
    Loads a JSON file and returns its content.
    :param file_path: Path to the JSON file.
    :return: Content of the JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json_file(data, file_path):
    """
    Saves data to a JSON file.
    :param data: Data to save.
    :param file_path: Path to the JSON file where data will be saved.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# End of utilities.py
