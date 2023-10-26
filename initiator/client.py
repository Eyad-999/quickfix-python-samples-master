"""FIX GATEWAY"""
import sys
import argparse
import quickfix
from application import Application
from your_custom_module import ResendRequestHandler  # Import your custom ResendRequestHandler class

def main(config_file):
    """Main"""
    try:
        # Initialize QuickFIX components
        quickfix_settings = quickfix.SessionSettings(config_file)
        quickfix_application = Application()
        store_factory = quickfix.FileStoreFactory(quickfix_settings)
        log_factory = quickfix.FileLogFactory(quickfix_settings)
        initiator = quickfix.SocketInitiator(quickfix_application, store_factory, quickfix_settings, log_factory)

        initiator.start()
        # Your QuickFIX application runs here
        initiator.stop()

    except quickfix.ConfigError as e:
        print(f"QuickFIX configuration error: {e}")
    except quickfix.RuntimeError as e:
        print(f"QuickFIX runtime error: {e}")
        initiator.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FIX Client')
    parser.add_argument('file_name', type=str, help='Name of configuration file')
    args = parser.parse_args()
    main(args.file_name)
