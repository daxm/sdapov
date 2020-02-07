"""Helper subroutines for use by the __exercise_function subroutines."""
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


def get_device_by_name(api_connection, name=None):
    """Get device info and return response"""
    return api_connection.devices.get_device_list(hostname=name)["response"][0]


def get_site_by_name(api_connection, data_vars, sites=[]):
    """Get site info for listed sites."""
    return api_connection.sites.get_site_by_name(name=name)["response"][0]

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
