"""Configure ny-ftd-1 via fmcapi."""

import fmcapi


def main():
    """Configure ny-ftd-1 via fmcapi."""
    with fmcapi.FMC(
        host="10.100.64.120",
        username="apiadmin",
        password="C1sco12345",
        autodeploy=True,
    ) as fmc:

        # Create ACP.
        acp = fmcapi.AccessPolicies(fmc=fmc, name="Initial_Policy")
        acp.defaultAction = "BLOCK"
        acp.post()

        # Create Security Zones
        sz_inside = fmcapi.SecurityZones(fmc=fmc, name="inside", interfaceMode="ROUTED")
        sz_inside.post()
        sz_outside = fmcapi.SecurityZones(
            fmc=fmc, name="outside", interfaceMode="ROUTED"
        )
        sz_outside.post()

        # Create Network Objects
        example_org_network = fmcapi.Networks(
            fmc=fmc, name="Example_Org_LANs", value="10.0.0.0/8"
        )
        example_org_network.post()
        fusion_gw = fmcapi.Hosts(fmc=fmc, name="Fusion_GW", value="10.100.255.81")
        fusion_gw.post()

        # Create Access Control Policy Rules
        init_rule = fmcapi.AccessRules(
            fmc=fmc, name="Permit Example Org LANs", action="ALLOW", enabled=True
        )
        init_rule.acp(name=acp.name)
        init_rule.source_network(action="add", name=example_org_network.name)
        init_rule.source_zone(action="add", name=sz_inside.name)
        init_rule.destination_zone(action="add", name=sz_outside.name)
        init_rule.post()

        # Build NAT Policy
        nat = fmcapi.FTDNatPolicies(fmc=fmc, name="Example Org NAT Policy")
        nat.post()

        # Build NAT Policy Rules.
        autonat = fmcapi.AutoNatRules(fmc=fmc)
        autonat.natType = "DYNAMIC"
        autonat.interfaceInTranslatedNetwork = True
        autonat.original_network(example_org_network.name)
        autonat.source_intf(name=sz_inside.name)
        autonat.destination_intf(name=sz_outside.name)
        autonat.nat_policy(name=nat.name)
        autonat.post()

        # Register ny-ftd-1 to FMC
        ftd = fmcapi.DeviceRecords(fmc=fmc)
        ftd.hostName = "10.100.255.82"
        ftd.regKey = "C1sco12345"
        ftd.acp(name=acp.name)
        ftd.name = "ny-ftd-1"
        ftd.licensing(action="add", name="BASE")
        ftd.licensing(action="add", name="MALWARE")
        ftd.licensing(action="add", name="VPN")
        ftd.licensing(action="add", name="THREAT")
        ftd.licensing(action="add", name="URLFilter")
        ftd.post(post_wait_time=300)

        # Configure ny-ftd-1 interfaces
        g0 = fmcapi.PhysicalInterfaces(fmc=fmc, device_name=ftd.name)
        g0.get(name="GigabitEthernet0/0")
        g0.enabled = True
        g0.ifname = "IN"
        g0.static(ipv4addr="10.100.255.83", ipv4mask=29)
        g0.sz(name=sz_inside.name)
        g0.put()
        g1 = fmcapi.PhysicalInterfaces(fmc=fmc, device_name=ftd.name)
        g1.get(name="GigabitEthernet0/1")
        g1.enabled = True
        g1.ifname = "OUT"
        g1.dhcp(enableDefault=True, routeMetric=1)
        g1.sz(name=sz_outside.name)
        g1.put()

        # Build Routes
        lan_route = fmcapi.IPv4StaticRoutes(fmc=fmc, name="ExampleOrgLANs")
        lan_route.device(device_name=ftd.name)
        lan_route.networks(action="add", networks=[example_org_network.name])
        lan_route.gw(name=fusion_gw.name)
        lan_route.interfaceName = g0.ifname
        lan_route.metricValue = 1
        lan_route.post()

        # Associate NAT Policy with ny-ftd-1
        devices = [{"name": ftd.name, "type": "device"}]
        assign_nat = fmcapi.PolicyAssignments(fmc=fmc)
        assign_nat.ftd_natpolicy(name=nat.name, devices=devices)
        assign_nat.post()


if __name__ == "__main__":
    main()
