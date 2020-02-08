"""Configure DNA Center up through Exercise 2."""
from dnacentersdk import DNACenterAPI
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
from ruamel.yaml import YAML
from pathlib import Path
from __exercise_functions import initial_discovery, provision_devices, set_device_role, assign_devices_to_sites

# Disable annoying HTTP warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main(datafile):
    """Run the program."""
    bordering = "=" * 15
    print("\n\n\n")
    print(bordering)
    print("Starting program")
    print(bordering)

    # Grab the data from the yaml file.
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
    # initial_discovery(api_connection=api, data_vars=my_data)

    # Exercise 2 Steps:
    devices_to_provision = ["cp-border-1.selfserve.lab", "cp-border-2.selfserve.lab", "edge-1.selfserve.lab"]
    assign_devices_to_sites(api_connection=api, data_vars=my_data["devices"], devices=devices_to_provision)
    provision_devices(api_connection=api, data_vars=my_data["devices"], devices=devices_to_provision)
    # set_device_role(api_connection=api, data_vars=my_data["devices"], devices=devices_to_provision)

    print(bordering)
    print("Automation script has completed, exiting.")
    print(bordering)


if __name__ == "__main__":
    main(datafile="userdata.yml")
