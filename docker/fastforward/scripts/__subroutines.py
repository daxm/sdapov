"""Subroutines related to Network Discovery API; to be used in main programs."""


def get_snmp_properties(api):
    community_ids = []

    # RO communitites
    response = api.network_discovery.get_global_credentials(credential_sub_type="SNMPV2_READ_COMMUNITY")
    for item in response["response"]:
        community_ids.append(item)

    # RW communitites
    response = api.network_discovery.get_global_credentials(credential_sub_type="SNMPV2_WRITE_COMMUNITY")
    for item in response["response"]:
        community_ids.append(item)
    return community_ids


def get_cli_user_id(api, credentials):
    response = api.network_discovery.get_global_credentials(credential_sub_type="CLI")
    for item in response["response"]:
        if item["username"] == credentials["username"]:
            return item["id"]
    return 0


def testing_stuff(api, data_vars):
    """Playground to mess with testing API calls."""
    pass
