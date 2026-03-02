#!/bin/bash
set -e

INTERFACE=${MONITOR_INTERFACE:-eth0}
echo "[*] Starting Security Monitor on $INTERFACE"

suricata -c /etc/suricata/suricata.yaml -i $INTERFACE -D
/opt/zeek/bin/zeek -i $INTERFACE /opt/zeek/share/zeek/site/local.zeek &

if [ -n "$WAZUH_MANAGER" ]; then
    sed -i "s/<address>MANAGER_IP<\/address>/<address>$WAZUH_MANAGER<\/address>/" /var/ossec/etc/ossec.conf
    /var/ossec/bin/wazuh-control start
fi

echo "[*] Services started. Logs: /var/log/suricata | /opt/zeek/logs | /var/ossec/logs"
tail -f /dev/null
