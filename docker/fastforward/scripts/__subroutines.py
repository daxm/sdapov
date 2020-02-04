"""Subroutines related to Network Discovery API; to be used in main programs."""
import time
from dnacentersdk import DNACenterAPI


def check_task_error_state(api, task_id=None):
    if task_id:
        result = api.task.get_task_by_id(task_id=task_id)
        if result["response"]["isError"]:
            print(f"An error has occurred with this task: {result}")
        else:
            print(f"Submitted task shows no errors.")
    return


def get_snmp_v2_communities(api):
    community_ids = []

    # RO communitites
    result = api.network_discovery.get_global_credentials(credential_sub_type="SNMPV2_READ_COMMUNITY")
    for item in result["response"]:
        community_ids.append(item)

    # RW communitites
    result = api.network_discovery.get_global_credentials(credential_sub_type="SNMPV2_WRITE_COMMUNITY")
    for item in result["response"]:
        community_ids.append(item)
    return community_ids


def get_cli_user_id(api, credentials):
    result = api.network_discovery.get_global_credentials(credential_sub_type="CLI")
    for item in result["response"]:
        if item["username"] == credentials["username"]:
            return item["id"]
    return 0


def testing_stuff(api, data_vars):
    """Playground to mess with testing API calls."""
    # Get tasks
    print(api.task.get_tasks())
    pass


if __name__ == "__main__":
    # This won't work but will allow command completion.
    api = DNACenterAPI
