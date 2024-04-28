# data_manager.py
# Manages data storage, retrieval, and preprocessing on the server side for the Distributed Inference System across Tesla Fleet

import os
import json
from .config import Config
from .utilities import setup_logging, log_system_activity, encrypt_data, decrypt_data

class DataManager:
    def __init__(self):
        """
        Initializes the DataManager class.
        """
        setup_logging()
        self.data_storage_path = Config.TEMP_DATA_STORAGE_PATH
        self.ensure_data_storage_path_exists()

    def ensure_data_storage_path_exists(self):
        """
        Ensures that the temporary data storage path exists.
        """
        if not os.path.exists(self.data_storage_path):
            os.makedirs(self.data_storage_path)
            log_system_activity(f"Created data storage directory at {self.data_storage_path}", "DEBUG")

    def store_data(self, data, file_name):
        """
        Stores data in a file within the temporary data storage path.
        :param data: Data to store.
        :param file_name: Name of the file to store the data in.
        """
        file_path = os.path.join(self.data_storage_path, file_name)
        with open(file_path, 'w') as file:
            json.dump(data, file)
        log_system_activity(f"Data stored in {file_path}", "INFO")

    def retrieve_data(self, file_name):
        """
        Retrieves data from a file within the temporary data storage path.
        :param file_name: Name of the file to retrieve the data from.
        :return: Data retrieved from the file.
        """
        file_path = os.path.join(self.data_storage_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
            log_system_activity(f"Data retrieved from {file_path}", "INFO")
            return data
        else:
            log_system_activity(f"File not found: {file_path}", "ERROR")
            return None

    def preprocess_data(self, data):
        """
        Preprocesses data if required by the configuration.
        :param data: Data to preprocess.
        :return: Preprocessed data.
        """
        if Config.DATA_PREPROCESSING_REQUIRED:
            # Example preprocessing: encrypt data
            preprocessed_data = encrypt_data(data)
            log_system_activity("Data preprocessing completed", "DEBUG")
            return preprocessed_data
        return data

    def cleanup_data_storage(self):
        """
        Cleans up the temporary data storage by removing all files.
        """
        for file_name in os.listdir(self.data_storage_path):
            file_path = os.path.join(self.data_storage_path, file_name)
            os.remove(file_path)
            log_system_activity(f"Removed file {file_path}", "DEBUG")

# Example usage
if __name__ == "__main__":
    dm = DataManager()
    sample_data = {"key": "value"}
    dm.store_data(sample_data, "sample.json")
    retrieved_data = dm.retrieve_data("sample.json")
    preprocessed_data = dm.preprocess_data(retrieved_data)
    dm.cleanup_data_storage()
