#!/usr/bin/env python3
"""
Security Monitoring Automation Script
Integrates Suricata, Zeek, and Nmap for automated threat detection
"""

import json
import nmap
import requests
from datetime import datetime
from elasticsearch import Elasticsearch

class SecurityMonitor:
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.suricata_log = "/var/log/suricata/eve.json"
        self.zeek_log = "/opt/zeek/logs/current/conn.log"
    
    def scan_network(self, target):
        """Perform network vulnerability scan"""
        print(f"[{datetime.now()}] Scanning {target}...")
        self.nm.scan(target, arguments='-sV -sC --script vuln')
        return self.nm.csv()
    
    def parse_suricata_alerts(self):
        """Parse Suricata EVE JSON alerts"""
        alerts = []
        try:
            with open(self.suricata_log, 'r') as f:
                for line in f:
                    event = json.loads(line)
                    if event.get('event_type') == 'alert':
                        alerts.append(event)
        except FileNotFoundError:
            pass
        return alerts
    
    def send_alert(self, alert_data):
        """Send alert to SIEM or webhook"""
        # Example: Send to webhook
        webhook_url = "https://your-siem.com/webhook"
        try:
            requests.post(webhook_url, json=alert_data, timeout=5)
        except:
            pass
    
    def monitor(self):
        """Main monitoring loop"""
        print(f"[{datetime.now()}] Security monitoring started")
        alerts = self.parse_suricata_alerts()
        print(f"Found {len(alerts)} alerts")
        
        for alert in alerts[-10:]:  # Last 10 alerts
            print(f"  - {alert.get('alert', {}).get('signature', 'Unknown')}")

if __name__ == "__main__":
    monitor = SecurityMonitor()
    monitor.monitor()
