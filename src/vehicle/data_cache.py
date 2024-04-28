# data_cache.py
# Manages local caching of data needed for quick access during computation in Tesla vehicles.

import os
import pickle
from .config import Config
from .utilities import log_system_activity, encrypt_data, decrypt_data

class DataCache:
    def __init__(self):
        self.cache_path = Config.TEMP_DATA_STORAGE_PATH
        self.ensure_cache_directory_exists()

    def ensure_cache_directory_exists(self):
        """
        Ensures that the cache directory exists on the filesystem.
        """
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
            log_system_activity(f"Cache directory created at {self.cache_path}", level="DEBUG")

    def store_data(self, key, data):
        """
        Stores data in the local cache with encryption.
        :param key: The key under which the data is stored.
        :param data: The data to store.
        """
        file_path = os.path.join(self.cache_path, f"{key}.cache")
        encrypted_data = encrypt_data(pickle.dumps(data))
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
        log_system_activity(f"Data stored in cache under key {key}", level="DEBUG")

    def retrieve_data(self, key):
        """
        Retrieves data from the local cache using the specified key.
        :param key: The key for the data to retrieve.
        :return: The decrypted data if available, otherwise None.
        """
        file_path = os.path.join(self.cache_path, f"{key}.cache")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
                data = pickle.loads(decrypt_data(encrypted_data))
                log_system_activity(f"Data retrieved from cache for key {key}", level="DEBUG")
                return data
        log_system_activity(f"No data found in cache for key {key}", level="WARNING")
        return None

    def clear_cache(self):
        """
        Clears all data stored in the cache.
        """
        for filename in os.listdir(self.cache_path):
            file_path = os.path.join(self.cache_path, filename)
            os.remove(file_path)
            log_system_activity(f"Removed cached file {filename}", level="DEBUG")
        log_system_activity("Cache cleared", level="INFO")

# Example usage:
if __name__ == "__main__":
    cache = DataCache()
    cache.store_data('example_key', {'data': 'This is a test'})
    retrieved_data = cache.retrieve_data('example_key')
    print(retrieved_data)
    cache.clear_cache()
