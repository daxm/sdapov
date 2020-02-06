"""Subroutines related to Network Discovery API; to be used in main programs."""
from dnacentersdk import DNACenterAPI, api
from time import sleep, perf_counter


def testing_stuff(api_connection, data_vars):
    """Playground to mess with testing API calls."""
    if api_connection:
        pass
    if data_vars:
        pass

    # asdf = api_connection.sites.get_site(name='SJ-13-2')
    # print(asdf)


def get_execution_info(api_connection, result={}):
    """Use the JSON response (aka the result) to dig deeper into the execution status."""
    query = {"timeDuration": 0}
    while query["timeDuration"] == 0:
        query = api_connection.custom_caller.call_api('GET', result["executionStatusUrl"])
    if query["status"] == 'FAILURE':
        print(f"API call failed with error:\n\t{query['bapiError']}")
        exit(1)
    elif query["status"] == 'SUCCESS':
        print(f"API call was a success!")


def assign_devices_to_sites(api_connection, data_vars, devices=[]):
    """Assign the list of devices to their hierarchy location."""
    # Loop through devices and provision them.
    for device in devices:
        # Collect this Device's ID from DNA Center.
        the_device = get_device_by_name(api_connection=api_connection, name=device)
        # Get info from userdata.yml file regarding this particular device.
        for yaml_device in data_vars:
            if yaml_device["name"] == device:
                # Get ID of hierarchy location for this device.
                print(f"Assigning {device} to site {yaml_device['location_name']}")
                result = api_connection.sites.assign_device_to_site(
                    device=[the_device],
                    site_id=api_connection.sites.get_site(name=yaml_device["location_name"])["response"][0]["id"])
                # result contains the "execution ID" and stuff so we can see how this POST is working.
                get_execution_info(api_connection=api_connection, result=result)


def get_device_by_name(api_connection, name=None):
    """Get device info and return response"""
    devices = api_connection.devices.get_device_list()["response"]
    for device in devices:
        if device["hostname"] == name:
            return device
    return 0


def set_device_role(api_connection, data_vars, devices=[]):
    """Configure the list of devices to their chosen device role."""
    # Loop through our list of devices to set roles.
    for device in devices:
        # Collect this Device's ID from DNA Center.
        device_id = get_device_by_name(api_connection=api_connection, name=device)["id"]
        # Loop through YAML configured devices to find THIS device.
        for yaml_device in data_vars:
            if yaml_device["name"] == device:
                # Set this device's role.
                print(f"Setting {device}'s role to {yaml_device['role']}")
                api_connection.devices.update_device_role(id=device_id, role=yaml_device["role"])


def provision_devices(api_connection, data_vars, devices=[]):
    """Provision the list of devices and assign to their hierarchy location."""
    # Loop through devices and provision them.
    for device in devices:
        # Collect this Device's ID from DNA Center.
        device_id = get_device_by_name(api_connection=api_connection, name=device)["id"]
        # Get info from userdata.yml file regarding this particular device.
        for yaml_device in data_vars:
            if yaml_device["name"] == device:
                # Get ID of hierarchy location for this device.
                location_id = api_connection.sites.get_site(name=yaml_device["location_name"])["response"][0]["id"]


                pass


def get_site(api_connection, data_vars, sites=[]):
    """Get site info for listed sites."""
    pass


def initial_discovery(api_connection, data_vars):
    """Perform initial discovery to get cp-border-1, cp-border-2, and edge-1 into DNA Center."""
    discovery_wait_timeout = 300
    print("Exercise 1: Add Devices to DNA Center")

    # Gather IDs for credentials list
    data_vars["initial_discovery"]["globalCredentialIdList"] = []
    print("\tCollecting info for CLI credentials.")
    data_vars["initial_discovery"]["globalCredentialIdList"].append(
        get_cli_user_id(api_connection=api_connection, credentials=data_vars["credentials"]["cli"]))
    print("\tCollecting info for SNMP RO/RW.")
    snmp_info = get_snmp_v2_communities(api_connection=api_connection)
    for item in snmp_info:
        data_vars["initial_discovery"]["globalCredentialIdList"].append(item["id"])

    # Start the Discovery
    print("\tBuild and start 'Initial Discovery'.")
    discovery_info = data_vars["initial_discovery"]
    result = api_connection.network_discovery.start_discovery(
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
    check_task_error_state(api_connection=api_connection, task_id=result["response"]["taskId"])

    # Wait for discovery to complete
    print("\tWait for 'Initial Discovery' to finish.")
    devices_discovered = []
    starttime = perf_counter()
    are_we_there_yet = False
    while not are_we_there_yet:
        result = api_connection.devices.get_device_list()
        for device in result["response"]:
            if device["hostname"] in discovery_info["device_names"] and device["hostname"] not in devices_discovered:
                print(f"\t{device['hostname']} has been added to inventory.")
                devices_discovered.append(device["hostname"])
        if (perf_counter() - starttime) > discovery_wait_timeout:
            print("\tMax wait time met.  Quiting waiting for devices to finish being discovered.")
            are_we_there_yet = True
        elif len(devices_discovered) >= len(discovery_info["device_names"]):
            print("\tAll devices discovered.")
            are_we_there_yet = True
        else:
            sleep(5)


def check_task_error_state(api_connection, task_id=None):
    """Check whether given task_id has errored."""
    if task_id:
        result = api_connection.task.get_task_by_id(task_id=task_id)
        if result["response"]["isError"]:
            print(f"An error has occurred with this task: {result}")
        else:
            print(f"Submitted task shows no errors.")
    return


def get_snmp_v2_communities(api_connection):
    """Collect SNMP v2 info."""
    community_ids = []

    # RO communitites
    result = api_connection.network_discovery.get_global_credentials(credential_sub_type="SNMPV2_READ_COMMUNITY")
    for item in result["response"]:
        community_ids.append(item)

    # RW communitites
    result = api_connection.network_discovery.get_global_credentials(credential_sub_type="SNMPV2_WRITE_COMMUNITY")
    for item in result["response"]:
        community_ids.append(item)
    return community_ids


def get_cli_user_id(api_connection, credentials):
    """Collect ID first user with CLI as sub-type."""
    result = api_connection.network_discovery.get_global_credentials(credential_sub_type="CLI")
    for item in result["response"]:
        if item["username"] == credentials["username"]:
            return item["id"]
    return 0


if __name__ == "__main__":
    # This won't work but will allow command completion.
    api = DNACenterAPI
