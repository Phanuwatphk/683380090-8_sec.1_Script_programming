# main.py
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __package__:
    from .src.config_parser import ConfigParser
    from .src.communication_agent import CommunicationAgent
    from .src.utils import setup_logging, ensure_directory_exists
else:
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    from src.config_parser import ConfigParser
    from src.communication_agent import CommunicationAgent
    from src.utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)

def main():
    base_dir = BASE_DIR
    config_file_path = os.path.join(base_dir, 'configs', 'comm_pipeline_config.json')

    try:
        ensure_directory_exists(os.path.join(base_dir, 'data', 'reports'))
        ensure_directory_exists(os.path.join(base_dir, 'data', 'incoming_attachments'))
        ensure_directory_exists(os.path.join(base_dir, 'reports'))

        logger.info(f"Loading configuration from: {config_file_path}")
        config_parser = ConfigParser(config_file_path)
        config = config_parser.load_config()

        logger.info("Initializing Communication Agent...")
        agent = CommunicationAgent(config, base_dir)

        logger.info("Running Communication Agent workflow...")
        agent.run()
        logger.info("Communication automation process completed.")

    except ValueError as e:
        logger.critical(f"Configuration error: {e}")
        logger.info(f"Set email credentials in '{os.path.join(base_dir, '.env')}' using '.env.example', and check '{config_file_path}'.")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
