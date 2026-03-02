# Security Monitoring Docker Platform

Production-ready all-in-one security monitoring container with Suricata, Wazuh, Zeek, Nmap, and Python automation tools.

## Features

- **IDS/IPS**: Suricata 7.0.2
- **SIEM Agent**: Wazuh 4.7.0
- **Network Monitoring**: Zeek 6.0.3
- **Vulnerability Scanning**: Nmap
- **Python Libraries**: requests, pandas, scapy, python-nmap, elasticsearch

## Quick Start

### Build the Image

```bash
docker build -t security-monitor:latest .
```

### Run with Docker

```bash
docker run -d \
  --name security-monitor \
  --network host \
  --cap-add=NET_ADMIN \
  --cap-add=NET_RAW \
  --cap-add=SYS_NICE \
  --privileged \
  -e MONITOR_INTERFACE=eth0 \
  -e WAZUH_MANAGER=192.168.1.100 \
  -v $(pwd)/logs/suricata:/var/log/suricata \
  -v $(pwd)/logs/zeek:/opt/zeek/logs \
  -v $(pwd)/logs/wazuh:/var/ossec/logs \
  security-monitor:latest
```

### Run with Docker Compose

```bash
docker-compose up -d
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONITOR_INTERFACE` | Network interface to monitor | `eth0` |
| `WAZUH_MANAGER` | Wazuh manager IP/hostname | None (optional) |
| `TZ` | Timezone | `UTC` |

## Ports

- **1514**: Wazuh agent communication (TCP)
- **1515**: Wazuh agent communication (UDP)
- **55000**: Wazuh API

## Volumes

- `/var/log/suricata` - Suricata IDS logs and alerts
- `/opt/zeek/logs` - Zeek network analysis logs
- `/var/ossec/logs` - Wazuh agent logs
- `/opt/security/rules` - Custom detection rules
- `/opt/security/scripts` - Custom automation scripts

## Usage Examples

### Run Nmap Scan

```bash
docker exec security-monitor nmap -sV 192.168.1.0/24
```

### View Suricata Alerts

```bash
docker exec security-monitor tail -f /var/log/suricata/fast.log
```

### Access Python Environment

```bash
docker exec -it security-monitor python3
```

### Custom Monitoring Script

```python
# /opt/security/scripts/custom_monitor.py
import nmap
from scapy.all import sniff
import requests

nm = nmap.PortScanner()
nm.scan('192.168.1.0/24', '22-443')
```

## Best Practices

### Resource Optimization

- **CPU**: Allocate 2-4 cores minimum
- **Memory**: 4GB minimum, 8GB recommended
- **Storage**: 50GB+ for logs

```bash
docker run --cpus="4" --memory="8g" ...
```

### Network Mode

Use `--network host` for full packet capture capabilities. For isolated environments, use bridge mode with port mappings.

### Security Considerations

1. **Privileged Mode**: Required for raw packet capture
2. **Capabilities**: NET_ADMIN, NET_RAW, SYS_NICE are essential
3. **Log Rotation**: Implement log rotation to prevent disk exhaustion
4. **Secrets**: Use Docker secrets for sensitive configurations

### Log Management

```bash
# Create log directories
mkdir -p logs/{suricata,zeek,wazuh}

# Set up log rotation
cat > /etc/logrotate.d/security-monitor << EOF
/path/to/logs/*/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

### Performance Tuning

Edit `docker-compose.yml` to adjust resources:

```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 8G
    reservations:
      cpus: '2'
      memory: 4G
```

## Maintenance

### Update Suricata Rules

```bash
docker exec security-monitor suricata-update
docker exec security-monitor systemctl restart suricata
```

### Check Service Status

```bash
docker exec security-monitor ps aux | grep -E 'suricata|zeek|wazuh'
```

### Backup Configuration

```bash
docker cp security-monitor:/etc/suricata/suricata.yaml ./backup/
docker cp security-monitor:/opt/zeek/etc/ ./backup/zeek/
```

## Troubleshooting

### Container won't start
- Check interface name: `ip link show`
- Verify privileged mode is enabled
- Check logs: `docker logs security-monitor`

### No packets captured
- Verify interface is up: `docker exec security-monitor ip link show eth0`
- Check promiscuous mode: `docker exec security-monitor ip link set eth0 promisc on`

### High CPU usage
- Reduce Suricata workers in `/etc/suricata/suricata.yaml`
- Limit Zeek scripts in `/opt/zeek/share/zeek/site/local.zeek`

## License

Production use - ensure compliance with tool licenses (Suricata: GPL, Zeek: BSD, Wazuh: GPL)
