#!/bin/bash
curl -i -X POST -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","method":"host.get","params":{"output":"extend","filter":{"host":"fqdn"}},"auth":"changeme","id":1}' http://fqdn/zabbix/api_jsonrpc.php
