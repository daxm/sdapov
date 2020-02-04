"""Subroutines related to Network Discovery API; to be used in main programs."""


def get_snmp_properties(api):
    response = api.network_discovery.get_global_credentials(credential_sub_type="SNMPV2_READ_COMMUNITY")
    return response


def get_cli_user_id(api, credentials):
    response = api.network_discovery.get_global_credentials(credential_sub_type="CLI")
    for item in response["response"]:
        if item["username"] == credentials["username"]:
            return item["id"]
    return 0


def testing_stuff(api, data_vars):
    """Playground to mess with testing API calls."""
    pass
