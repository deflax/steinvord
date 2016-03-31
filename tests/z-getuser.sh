#!/bin/bash
curl -i -X POST -H 'Content-Type:application/json' -d'{"jsonrpc": "2.0","method":"user.login","params":{"user":"USER","password":"PASS"},"auth": null,"id":0}' http://fqdn/zabbix/api_jsonrpc.php
