# !/user/bin/env python3

# This parses through all yamls and puts them into a dataclass so that other modules can import and use the config
# within them

from dataclasses import dataclass

import yaml

from rev_console_logger import ConsoleAccess


# Main yaml dataclass
@dataclass
class YAMLData:
    # Config of the serial port
    PORT: int = 0
    SPEED: int = 0

    # Wait time in seconds between attempted connection attempts if serial is not present
    S_WAIT: int = 60

    def __post_init__(self):
        # Set up serial from yaml config file
        with open(r'serial_config.yaml') as file:
            documents = yaml.full_load(file)

            # Get serial config
            self.PORT = documents['port']
            self.SPEED = documents['speed']
            self.S_WAIT = documents['serial_reconnect']


# Instantiates the yaml dataclass so that other modules can import it and use the latest yaml data
YAMLAccess = YAMLData()

if __name__ == "__main__":
    # Perform a test by parsing all yaml files and printing their data
    ConsoleAccess.console_print_enable = True
    ConsoleAccess.console_printer(YAMLAccess)
