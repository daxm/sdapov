
"""Configure DNA Center up through Exercise 1."""

from dnacentersdk import DNACenterAPI
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
from ruamel.yaml import YAML
from pathlib import Path
from __subroutines import get_cli_user_id, get_snmp_v2_communities, wait_for_task_to_complete

# Disable annoying HTTP warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main(datafile):
    """Grab the data from the yaml file."""
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

    # testing_stuff(api, data_vars)
    # Exercise 1 Steps:
    initial_discover(api=api, data_vars=my_data)


def initial_discover(api, data_vars):
    """
    Perform initial discovery to get cp-border-1, cp-border-2, and edge-1 into DNA Center.
    """
    # Gather IDs for credentials list
    data_vars["initial_discovery"]["globalCredentialIdList"] = []
    data_vars["initial_discovery"]["globalCredentialIdList"].append(
        get_cli_user_id(api=api, credentials=data_vars["credentials"]["cli"]))
    snmp_info = get_snmp_v2_communities(api=api)
    for item in snmp_info:
        data_vars["initial_discovery"]["globalCredentialIdList"].append(item["id"])

    discovery_info = data_vars["initial_discovery"]

    # Start the Discovery
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

    print(result["response"])
    # Wait for discovery to complete
    wait_for_task_to_complete(task_id=result["response"]["taskId"])


if __name__ == "__main__":
    main(datafile="userdata.yml")
