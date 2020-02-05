
"""Configure DNA Center up through Exercise 1."""

from dnacentersdk import DNACenterAPI
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
from ruamel.yaml import YAML
from pathlib import Path
from __subroutines import initial_discovery

# Disable annoying HTTP warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main(datafile):
    """Grab the data from the yaml file."""
    print("\n\n\n")
    print("="*15)
    print("Starting program")
    print("="*15)
    yaml = YAML(typ="safe")
    path = Path(datafile)
    with open(path, "r") as stream:
        try:
            my_data = yaml.load(stream)
            logging.info(f"Loading {path} file.")
        except OSError:
            logging.error(f"An error has occurred trying to open {path}.")
            exit(1)

    # Establish connection to DNA Center
    api = DNACenterAPI(**my_data["dnac"])

    # Exercise 1 Steps:
    initial_discovery(api_connection=api, data_vars=my_data)
    # testing_stuff(api=api, data_vars=my_data)


if __name__ == "__main__":
    main(datafile="userdata.yml")
