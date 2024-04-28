# scheduler.py
# Task scheduler for managing workload distribution among the Tesla Fleet vehicles in the Distributed Inference System

import heapq
import random
from threading import Lock
from .utilities import log_system_activity
from .config import Config

class TaskScheduler:
    def __init__(self):
        self.lock = Lock()
        self.tasks_queue = []
        self.node_status = {}  # Stores the status of each node (vehicle)

    def schedule_task(self, task):
        """
        Schedules a task based on the current load and the specified scheduling strategy.
        :param task: A dictionary containing task details.
        """
        with self.lock:
            if Config.TASK_ALLOCATION_STRATEGY == "dynamic":
                self._dynamic_schedule(task)
            else:
                self._static_schedule(task)

    def _dynamic_schedule(self, task):
        """
        Dynamically schedules tasks based on node performance and current load.
        :param task: Task to be scheduled.
        """
        # Select the node with the least load
        if not self.node_status:
            log_system_activity("No nodes available for scheduling", "ERROR")
            return

        least_loaded_node = min(self.node_status, key=lambda k: self.node_status[k]['load'])
        self._assign_task_to_node(task, least_loaded_node)

    def _static_schedule(self, task):
        """
        Statically schedules tasks in a round-robin fashion.
        :param task: Task to be scheduled.
        """
        nodes = list(self.node_status.keys())
        if not nodes:
            log_system_activity("No nodes available for scheduling", "ERROR")
            return

        node = random.choice(nodes)
        self._assign_task_to_node(task, node)

    def _assign_task_to_node(self, task, node):
        """
        Assigns a task to a specified node.
        :param task: Task to be assigned.
        :param node: Node to which the task is assigned.
        """
        if node in self.node_status:
            self.node_status[node]['tasks'].append(task)
            self.node_status[node]['load'] += task['load']
            log_system_activity(f"Task {task['id']} assigned to node {node}", "INFO")
        else:
            log_system_activity(f"Node {node} not found in node status", "ERROR")

    def update_node_status(self, node_id, status):
        """
        Updates the status of a node.
        :param node_id: ID of the node.
        :param status: Status information containing load and other metrics.
        """
        with self.lock:
            self.node_status[node_id] = status
            log_system_activity(f"Updated status for node {node_id}", "INFO")

    def remove_node(self, node_id):
        """
        Removes a node from the scheduler.
        :param node_id: ID of the node to be removed.
        """
        with self.lock:
            if node_id in self.node_status:
                del self.node_status[node_id]
                log_system_activity(f"Node {node_id} removed from scheduler", "INFO")
            else:
                log_system_activity(f"Node {node_id} not found in scheduler", "ERROR")

# Example usage:
# scheduler = TaskScheduler()
# scheduler.update_node_status('node1', {'load': 10, 'tasks': []})
# scheduler.schedule_task({'id': 'task1', 'load': 5})
