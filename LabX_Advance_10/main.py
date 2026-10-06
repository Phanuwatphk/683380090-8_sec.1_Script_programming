# main.py
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __package__:
    from .src.utils import setup_logging
    from .src.config_parser import ConfigParser
    from .src.spreadsheet_agent import SpreadsheetAgent
else:
    # Find the local src package relative to this file when run as a script.
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    from src.utils import setup_logging
    from src.config_parser import ConfigParser
    from src.spreadsheet_agent import SpreadsheetAgent

logger = setup_logging(__name__)

def main():
    base_dir = BASE_DIR
    config_file_path = os.path.join(base_dir, 'configs', 'example_spreadsheet_config.json')
    try:
        os.makedirs(os.path.join(base_dir, 'data'), exist_ok=True)
        logger.info(f"Loading configuration from: {config_file_path}")
        config_parser = ConfigParser(config_file_path)
        config = config_parser.load_config()
        for key in ('input_file', 'output_file'):
            config[key] = os.path.join(base_dir, config[key])
        
        input_file_path = config.get("input_file")
        if not os.path.exists(input_file_path):
            logger.critical(f"❌ Input file not found: '{input_file_path}'")
            return
        
        logger.info("Initializing Spreadsheet Agent...")
        agent = SpreadsheetAgent(config)
        logger.info("Running Spreadsheet Agent...")
        agent.run()
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
