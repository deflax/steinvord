#!/usr/bin/python3.2
#
# Zabbix API Python usage example
# Christoph Haas <email@christoph-haas.de>
#

username=''
password='1'
hostgroup=''
item_name='system.cpu.load[,avg1]'
zabbix_url=''

import zabbix_api
import sys

# Connect to Zabbix server
z=zabbix_api.ZabbixAPI(server=zabbix_url)
z.login(user=username, password=password)

# Get hosts in the hostgroup
hostgroup = z.hostgroup.get(
    {
    'filter': { 'name':hostgroup },
    'sortfield': 'name',
    'sortorder': 'ASC',
    'limit':2,
    'select_hosts':'extend'
    })

print(hostgroup[0])
print("\n")
for host in hostgroup[0]['name']:
    hostname = host['host']
    print("Host:", hostname)
    print("Host-ID:", host['hostid'])

    item = z.item.get({
        'output':'extend',
        'hostids':host['hostid'],
        'filter':{'key_':item_name}})
    if item:
        print(item[0]['lastvalue'])
        print("Item-ID:", item[0]['itemid'])

        # Get history
        lastvalue = z.history.get({
            'history': item[0]['value_type'],
            'itemids': item[0]['itemid'],
            'output': 'extend',
            # Sort by timestamp from new to old
            'sortfield':'clock',
            'sortorder':'DESC',
            # Get only the first (=newest) entry
            'limit': 1,
            })

        # CAVEAT! The history.get function must be told which type the
        # values are (float, text, etc.). The item.value_type contains
        # the number that needs to be passed to history.get.
        if lastvalue:
            lastvalue = lastvalue[0]['value']

        print("Last value:", lastvalue)

    else:
        print("No item....")

    print("---------------------------")


