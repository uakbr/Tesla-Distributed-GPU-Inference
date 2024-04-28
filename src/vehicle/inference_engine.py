# inference_engine.py
# Module to execute inference tasks using the vehicle’s GPU in the Distributed Inference System across Tesla Fleet

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from .communication import send_results_to_server
from .data_cache import get_cached_data
from .utilities import log_system_activity, setup_logging
from .config import Config

setup_logging()

class InferenceEngine:
    def __init__(self):
        """
        Initializes the Inference Engine with the necessary model and configurations.
        """
        self.model = self.load_model()
        log_system_activity("Inference Engine initialized.", "INFO")

    def load_model(self):
        """
        Loads the machine learning model from the specified path.
        :return: Loaded TensorFlow model.
        """
        try:
            model = load_model(Config.MODEL_PATH)
            log_system_activity("Model loaded successfully.", "INFO")
            return model
        except Exception as e:
            log_system_activity(f"Failed to load model: {str(e)}", "ERROR")
            return None

    def perform_inference(self, data):
        """
        Performs inference on the provided data using the loaded model.
        :param data: Data on which inference is to be performed.
        :return: Inference results.
        """
        if self.model is None:
            log_system_activity("Model is not loaded, cannot perform inference.", "ERROR")
            return None

        try:
            preprocessed_data = self.preprocess_data(data)
            predictions = self.model.predict(preprocessed_data)
            log_system_activity("Inference performed successfully.", "INFO")
            return predictions
        except Exception as e:
            log_system_activity(f"Error during inference: {str(e)}", "ERROR")
            return None

    def preprocess_data(self, data):
        """
        Preprocesses the data before feeding it into the model.
        :param data: Raw data to preprocess.
        :return: Preprocessed data.
        """
        # Example preprocessing: normalize data
        return data / 255.0

    def handle_inference_task(self):
        """
        Handles an inference task by fetching data, performing inference, and sending results back.
        """
        data = get_cached_data()
        if data is not None:
            results = self.perform_inference(data)
            if results is not None:
                send_results_to_server(results)
                log_system_activity("Results sent to server.", "INFO")
            else:
                log_system_activity("Failed to perform inference or send results.", "ERROR")
        else:
            log_system_activity("No data available for inference.", "ERROR")

if __name__ == "__main__":
    inference_engine = InferenceEngine()
    inference_engine.handle_inference_task()
