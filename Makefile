set_datasource:
	curl --header "Content-Type: application/json" \
  		--request POST \
  		--data '{"orgId": 1, "name": "ClickHouse","type": "grafana-clickhouse-datasource","typeName": "ClickHouse","access": "proxy","isDefault": true,"jsonData": {"port": 9000, "protocol": "native", "server": "172.17.0.2"},"readOnly": false}' \
  		-u admin:admin \
  		http://localhost:3000/api/datasources
