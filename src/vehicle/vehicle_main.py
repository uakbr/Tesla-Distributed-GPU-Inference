# vehicle_main.py
# Main script running on each Tesla vehicle for the Distributed Inference System

import threading
import time
from .communication import send_data, receive_instructions
from .inference_engine import process_inference_task
from .data_cache import cache_data, retrieve_cached_data
from src.common.utilities import setup_logging, log_system_activity, encrypt_data, decrypt_data
from src.common.config import Config

def main():
    setup_logging()
    log_system_activity("Vehicle node starting up.", "INFO")

    # Main loop
    while True:
        try:
            # Check for new instructions from the server
            instructions = receive_instructions()
            if instructions:
                log_system_activity(f"Received instructions: {instructions}", "DEBUG")
                handle_instructions(instructions)
            else:
                log_system_activity("No new instructions received. Checking cached tasks.", "DEBUG")
                handle_cached_tasks()

            # Monitor system health
            monitor_system_health()

            # Sleep for a configured interval before next check
            time.sleep(Config.CHECK_INTERVAL)
        except Exception as e:
            log_system_activity(f"Error in main loop: {str(e)}", "ERROR")
            if Config.AUTO_RECOVERY_ENABLED:
                recover_from_error(e)

def handle_instructions(instructions):
    """
    Handle instructions received from the central server.
    :param instructions: Dict containing task details and commands.
    """
    if 'task' in instructions:
        task_data = decrypt_data(instructions['task'])
        cache_data(task_data['id'], task_data)
        log_system_activity(f"Task {task_data['id']} cached for processing.", "INFO")

        # Start a new thread to handle the task processing
        task_thread = threading.Thread(target=process_task, args=(task_data,))
        task_thread.start()

def handle_cached_tasks():
    """
    Process tasks that are cached locally if no new instructions are received.
    """
    cached_tasks = retrieve_cached_data()
    for task_id, task_data in cached_tasks.items():
        log_system_activity(f"Processing cached task {task_id}.", "INFO")
        process_task(task_data)

def process_task(task_data):
    """
    Process a single inference task using the vehicle's GPU.
    :param task_data: Data necessary for the inference task.
    """
    result = process_inference_task(task_data)
    send_data(encrypt_data(result))
    log_system_activity(f"Task {task_data['id']} processed and result sent.", "INFO")

def monitor_system_health():
    """
    Monitor and log the health of the vehicle's system components.
    """
    # Example health checks (to be expanded based on actual system requirements)
    log_system_activity("System health check completed.", "DEBUG")

def recover_from_error(error):
    """
    Attempt to recover from an error automatically.
    :param error: The error to recover from.
    """
    log_system_activity(f"Attempting to recover from error: {str(error)}", "WARNING")
    # Recovery logic here

if __name__ == "__main__":
    main()
