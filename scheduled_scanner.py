#!/usr/bin/env python3
"""
Automated Scheduled Security Scans
Runs periodic vulnerability assessments
"""

import logging
import os
import time
import nmap
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScheduledScanner:
    def __init__(self):
        self.scan_interval = int(os.getenv('SCAN_INTERVAL', '3600'))  # Default: 1 hour
        self.scan_targets = os.getenv('SCAN_TARGETS', '192.168.1.0/24').split(',')
        self.output_dir = '/opt/security/scan_results'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def run_scan(self, target):
        """Execute vulnerability scan"""
        logging.info(f"Starting scan on {target}")
        nm = nmap.PortScanner()
        
        try:
            nm.scan(target, arguments='-sV -sC --script vuln')
            
            results = {
                'timestamp': datetime.now().isoformat(),
                'target': target,
                'hosts': {}
            }
            
            for host in nm.all_hosts():
                results['hosts'][host] = {
                    'state': nm[host].state(),
                    'protocols': {}
                }
                
                for proto in nm[host].all_protocols():
                    results['hosts'][host]['protocols'][proto] = {}
                    for port in nm[host][proto].keys():
                        results['hosts'][host]['protocols'][proto][port] = nm[host][proto][port]
            
            # Save results
            filename = f"{self.output_dir}/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            
            logging.info(f"Scan completed. Results saved to {filename}")
            return results
            
        except Exception as e:
            logging.error(f"Scan failed: {e}")
            return None
    
    def start(self):
        """Start scheduled scanning"""
        logging.info(f"Starting scheduled scanner (interval: {self.scan_interval}s)")
        logging.info(f"Targets: {self.scan_targets}")
        
        while True:
            for target in self.scan_targets:
                self.run_scan(target.strip())
            
            logging.info(f"Waiting {self.scan_interval}s until next scan...")
            time.sleep(self.scan_interval)

if __name__ == "__main__":
    scanner = ScheduledScanner()
    scanner.start()
