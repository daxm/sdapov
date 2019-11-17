"""
Program SDA Security PoV's FMC and FTD for this PoV.
"""
import fmcapi


def main():
    """
    The FTD device already has 100.127.100.15 on its management interface and the command 'configure network manager
    100.64.0.155 cisco123' has already been manually typed on the FTD's CLI.
    """
    with fmcapi.FMC(host='100.64.0.166', username='apiadmin', password='C1sco12345', autodeploy=True) as fmc1:
        # Create Security Zones
        sz1 = fmcapi.SecurityZones(fmc=fmc1)
        sz1.name = 'Restricted'
        sz1.post()

        sz2 = fmcapi.SecurityZones(fmc=fmc1)
        sz2.name = 'Outside'
        sz2.post()

        # Create Objects
        border1 = fmcapi.NetworkAddresses(fmc=fmc1, name='Border-1', value='100.126.1.13')
        border1.post()

        finance = fmcapi.NetworkAddresses(fmc=fmc1, name='finance.selfserve.lab', value='100.64.0.134')
        finance.post()

        pci = fmcapi.NetworkAddresses(fmc=fmc1, name='pci.selfserve.lab', value='100.64.0.133')
        pci.post()

        ftd_border1_net = fmcapi.Networks(fmc=fmc1, name='FTD-Border1-net', value='100.126.1.12/30')
        ftd_border1_net.post()

        restricted_vn_net = fmcapi.Networks(fmc=fmc1, name='Restricted-VN-net', value='100.110.0.0/16')
        restricted_vn_net.post()

        # Create ACPs
        acp1 = fmcapi.AccessPolicies(fmc=fmc1,
                                     name='Restricted-VN-Initial-Policy',
                                     defaultAction='NETWORK_DISCOVERY',
                                     )
        acp1.post()

        acp2 = fmcapi.AccessPolicies(fmc=fmc1,
                                     name='Restricted-VN-RTC-Policy',
                                     defaultAction='NETWORK_DISCOVERY',
                                     )
        acp2.post()

        # Create ACP Rules for the ACPs
        initial_rule1 = fmcapi.AccessRules(fmc=fmc1, acp_name=acp1.name, name='Permit-ANY')
        initial_rule1.logBegin = True
        initial_rule1.logEnd = True
        initial_rule1.action = 'ALLOW'
        initial_rule1.post()

        rapid_threat_rule1 = fmcapi.AccessRules(fmc=fmc1, acp_name=acp2.name, name='PCIUsers-to-sources')
        rapid_threat_rule1.source_network(action='add', name=restricted_vn_net.name)
        rapid_threat_rule1.destination_port(action='add', name='HTTP')
        # rapid_threat_rule1.isesgt(name='PCI_user')
        rapid_threat_rule1.logBegin = True
        rapid_threat_rule1.logEnd = True
        rapid_threat_rule1.intrusion_policy(action='add', name='Restricted-VN-IPS-Policy')
        rapid_threat_rule1.action = 'ALLOW'
        rapid_threat_rule1.enabled = True
        rapid_threat_rule1.post()

        rapid_threat_rule2 = fmcapi.AccessRules(fmc=fmc1, acp_name=acp2.name, name='FinanceUsers2PCIResource')
        rapid_threat_rule2.source_network(action='add', name=restricted_vn_net.name)
        rapid_threat_rule2.destination_network(action='add', name=finance.name)
        rapid_threat_rule2.destination_port(action='add', name='HTTP')
        # rapid_threat_rule2.isesgt(name='PCI_user')
        # rapid_threat_rule2.isesgt(name='finance_user')
        rapid_threat_rule2.logBegin = True
        rapid_threat_rule2.logEnd = True
        rapid_threat_rule2.intrusion_policy(action='add', name='Restricted-VN-IPS-Policy')
        rapid_threat_rule2.action = 'ALLOW'
        rapid_threat_rule2.enabled = True
        rapid_threat_rule2.post()

        rapid_threat_rule3 = fmcapi.AccessRules(fmc=fmc1, acp_name=acp2.name, name='DenyUnauthenticatedUsers')
        rapid_threat_rule3.source_network(action='add', name=restricted_vn_net.name)
        rapid_threat_rule3.destination_network(action='add', name=finance.name)
        rapid_threat_rule3.destination_network(action='add', name=pci.name)
        rapid_threat_rule3.destination_port(action='add', name='HTTP')
        rapid_threat_rule3.logBegin = True
        rapid_threat_rule3.action = 'BLOCK'
        rapid_threat_rule3.enabled = True
        rapid_threat_rule3.post()

        rapid_threat_rule4 = fmcapi.AccessRules(fmc=fmc1, acp_name=acp2.name, name='Permit-ANY')
        rapid_threat_rule4.source_network(action='add', name='ipv4-any')
        rapid_threat_rule4.destination_network(action='add', name='ipv4-any')
        rapid_threat_rule4.action = 'ALLOW'
        rapid_threat_rule4.enabled = True
        rapid_threat_rule4.post()

        # Add FTD device to FMC
        ftd1 = fmcapi.DeviceRecords(fmc=fmc1)
        ftd1.hostName = '100.127.100.15'
        ftd1.regKey = 'C1sco12345'
        ftd1.acp(name='Restricted-VN-Initial-Policy')
        ftd1.name = 'FTD'
        ftd1.licensing(action='add', name='MALWARE')
        ftd1.licensing(action='add', name='VPN')
        ftd1.licensing(action='add', name='BASE')
        ftd1.licensing(action='add', name='THREAT')
        ftd1.licensing(action='add', name='URL')
        # Push to FMC to start device registration.
        ftd1.post(post_wait_time=300)

        # Once registration is complete configure the interfaces of ftd.
        int101 = fmcapi.PhysicalInterfaces(fmc=fmc1, device_name=ftd1.name)
        int101.get(name='GigabitEthernet0/0')
        int101.enabled = True
        int101.ifname = 'FTD-to-Fusion'
        int101.sz(name=sz2.name)
        int101.static(ipv4addr='100.127.101.254', ipv4mask=24)
        int101.put()

        int3004 = fmcapi.PhysicalInterfaces(fmc=fmc1, device_name=ftd1.name)
        int3004.get(name='GigabitEthernet0/1')
        int3004.enabled = True
        int3004.ifname = 'FTD-to-Border1'
        int3004.sz(name=sz1.name)
        int3004.static(ipv4addr='100.126.1.14', ipv4mask=30)
        int3004.put()


if __name__ == "__main__":
    main()
