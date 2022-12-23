#!/bin/bash
echo "Undeploy Taxis.ear"
curl -S -H "content-Type: application/json" -d '{"operation":"undeploy", "address":[{"deployment":"Taxis.ear"}]}' --digest http://admin:adminadmin@localhost:10790/management
echo ""

echo "Remove Taxis.ear"
curl -S -H "content-Type: application/json" -d '{"operation":"remove", "address":[{"deployment":"Taxis.ear"}]}' --digest http://admin:adminadmin@localhost:10790/management
echo ""

echo "Upload Taxis.ear"
bytes_value=`curl -F "file=@Taxis.ear" --digest http://admin:adminadmin@localhost:10790/management/add-content | perl -pe 's/^.*"BYTES_VALUE"\s*:\s*"(.*)".*$/$1/'`
echo $bytes_value

json_string_start='{"content":[{"hash": {"BYTES_VALUE" : "'
json_string_end='"}}], "address": [{"deployment":"Taxis.ear"}], "operation":"add", "enabled":"true"}'
json_string="$json_string_start$bytes_value$json_string_end"

echo "Deploy Taxis.ear"
result=`curl -S -H "Content-Type: application/json" -d "$json_string" --digest http://admin:adminadmin@localhost:10790/management | perl -pe 's/^.*"outcome"\s*:\s*"(.*)".*$/$1/'`
echo $result

if [ "$result" != "success" ]; then
  exit -1
fi
