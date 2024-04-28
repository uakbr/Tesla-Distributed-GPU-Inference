# config.py
# Configuration settings for the Distributed Inference System across Tesla Fleet

class Config:
    # General settings
    SYSTEM_NAME = "Tesla Fleet Distributed Inference System"
    DEBUG_MODE = False

    # Network settings
    SERVER_URL = "https://central.server.com"
    VPN_TUNNEL_ENDPOINT = "https://vpn.server.com"
    VEHICLE_TO_VEHICLE_COMMUNICATION_ENABLED = True
    VEHICLE_TO_INFRASTRUCTURE_COMMUNICATION_ENABLED = True

    # Security settings
    ENCRYPTION_KEY = "your-encryption-key-here"
    AUTHENTICATION_TOKEN = "secure-auth-token"

    # Performance settings
    MAX_GPU_UTILIZATION_PERCENT = 85  # Maximum GPU utilization before throttling
    NETWORK_BANDWIDTH_LIMIT = 1000  # in Mbps

    # Fault tolerance and error handling
    AUTO_RECOVERY_ENABLED = True
    DATA_REPLICATION_FACTOR = 3  # Number of copies of critical data

    # Scheduler settings
    TASK_ALLOCATION_STRATEGY = "dynamic"  # Options: 'static', 'dynamic'
    LOAD_BALANCING_ALGORITHM = "predictive"  # Options: 'round-robin', 'predictive'

    # Data management
    DATA_PREPROCESSING_REQUIRED = True
    TEMP_DATA_STORAGE_PATH = "/tmp/tesla_fleet_data"

    # Logging and monitoring
    LOGGING_LEVEL = "INFO"  # Options: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    MONITOR_GPU_USAGE = True
    MONITOR_NETWORK_TRAFFIC = True

    # Update and deployment settings
    AUTO_UPDATE_CHECK_ENABLED = True
    UPDATE_CHECK_URL = "https://update.server.com/check"
    UPDATE_FREQUENCY_HOURS = 24  # Check for updates every 24 hours

    # Define any additional configuration parameters that might be needed for the project

# End of config.py
