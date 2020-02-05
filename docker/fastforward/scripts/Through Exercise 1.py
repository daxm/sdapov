
"""Configure DNA Center up through Exercise 1."""

from dnacentersdk import DNACenterAPI
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
from ruamel.yaml import YAML
from pathlib import Path
from __subroutines import get_cli_user_id, get_snmp_v2_communities, check_task_error_state, testing_stuff
from time import sleep, perf_counter

# Disable annoying HTTP warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Globals
MAX_WAIT_SEC = 300


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
    initial_discovery(api=api, data_vars=my_data)
    # testing_stuff(api=api, data_vars=my_data)


def initial_discovery(api, data_vars):
    """
    Perform initial discovery to get cp-border-1, cp-border-2, and edge-1 into DNA Center.
    """
    print("Exercise 1: Add Devices to DNA Center")

    # Gather IDs for credentials list
    data_vars["initial_discovery"]["globalCredentialIdList"] = []
    print("\tCollecting info for CLI credentials.")
    data_vars["initial_discovery"]["globalCredentialIdList"].append(
        get_cli_user_id(api=api, credentials=data_vars["credentials"]["cli"]))
    print("\tCollecting info for SNMP RO/RW.")
    snmp_info = get_snmp_v2_communities(api=api)
    for item in snmp_info:
        data_vars["initial_discovery"]["globalCredentialIdList"].append(item["id"])

    discovery_info = data_vars["initial_discovery"]

    # Start the Discovery
    print("\tBuild and start 'Initial Discovery'.")
    result = api.network_discovery.start_discovery(
        discoveryType=discovery_info["discoveryType"],
        preferredMgmtIPMethod=discovery_info["preferredMgmtIPMethod"],
        ipAddressList=discovery_info["ipAddressList"],
        protocolOrder=discovery_info["protocolOrder"],
        globalCredentialIdList=discovery_info["globalCredentialIdList"],
        timeout=discovery_info["timeout"],
        retry=discovery_info["retry"],
        name=discovery_info["name"],
        netconfPort=str(discovery_info["netconfPort"]),
    )
    check_task_error_state(api=api, task_id=result["response"]["taskId"])

    # Wait for discovery to complete
    print("\tWait for 'Initial Discovery' to finish.")
    devices_discovered = []
    number_of_devices_to_find = len(discovery_info["device_names"])
    starttime = perf_counter()
    time_delta = 0
    while (len(devices_discovered) <= number_of_devices_to_find) or (MAX_WAIT_SEC > time_delta):
        result = api.devices.get_device_list()
        for device in result["response"]:
            if device["hostname"] in discovery_info["device_names"] and device["hostname"] not in devices_discovered:
                print(f"\t\t{device['hostname']} has been added to inventory.")
                devices_discovered.append(device["hostname"])
        sleep(5)
        time_delta = perf_counter() - starttime
        if time_delta > MAX_WAIT_SEC:
            print("\t\tMax wait time met.  Quiting waiting for devices to finish being discovered.")


if __name__ == "__main__":
    main(datafile="userdata.yml")
