# result_aggregator.py
# Collects and processes results from the vehicles in the Distributed Inference System across Tesla Fleet

import json
from .config import Config
from .utilities import setup_logging, log_system_activity, decrypt_data

class ResultAggregator:
    def __init__(self):
        """
        Initializes the ResultAggregator class.
        """
        setup_logging()
        self.results = []

    def aggregate_results(self, encrypted_results):
        """
        Aggregates results from multiple vehicle nodes, decrypts them, and processes them for final output.
        :param encrypted_results: List of encrypted result strings from vehicle nodes.
        """
        log_system_activity("Starting aggregation of results.", "INFO")
        decrypted_results = [decrypt_data(result) for result in encrypted_results]
        self.results.extend(decrypted_results)
        log_system_activity(f"Aggregated {len(decrypted_results)} results.", "INFO")

    def process_final_results(self):
        """
        Processes the aggregated results to produce the final output.
        """
        log_system_activity("Processing final results.", "INFO")
        # Example processing: Summing up results
        final_result = sum(self.results)
        log_system_activity(f"Final result computed: {final_result}", "INFO")
        return final_result

    def store_results(self, result):
        """
        Stores the final result in a persistent storage.
        :param result: The final result to store.
        """
        log_system_activity("Storing final result.", "INFO")
        # Placeholder for storing the result, e.g., in a database or a file
        with open('final_result.json', 'w') as f:
            json.dump({'final_result': result}, f)
        log_system_activity("Final result stored successfully.", "INFO")

# Example usage
if __name__ == "__main__":
    aggregator = ResultAggregator()
    # Simulate receiving encrypted results
    encrypted_results = ["gAAAAABf2xyz...==", "gAAAAABf2abc...=="]
    aggregator.aggregate_results(encrypted_results)
    final_result = aggregator.process_final_results()
    aggregator.store_results(final_result)
