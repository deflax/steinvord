#!/bin/bash
curl -i -X POST -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","method":"item.get","params":{"output":"extend","filter":{"hostid":"10125"}},"auth":"changeme","id":2}' http://fqdn/zabbix/api_jsonrpc.php
