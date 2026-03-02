FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive MONITOR_INTERFACE=eth0

RUN apt-get update && apt-get install -y \
    wget curl gnupg2 software-properties-common python3-pip nmap iproute2 \
    && add-apt-repository ppa:oisf/suricata-stable -y \
    && curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | gpg --no-default-keyring --keyring gnupg-ring:/usr/share/keyrings/wazuh.gpg --import \
    && chmod 644 /usr/share/keyrings/wazuh.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" > /etc/apt/sources.list.d/wazuh.list \
    && wget -qO - https://download.zeek.org/zeek.gpg | apt-key add - \
    && echo "deb http://download.zeek.org/apt/stable jammy main" > /etc/apt/sources.list.d/zeek.list \
    && apt-get update && apt-get install -y suricata wazuh-agent zeek \
    && suricata-update \
    && pip3 install --no-cache-dir requests pandas scapy python-nmap elasticsearch \
    && ln -s /opt/zeek/bin/zeek /usr/local/bin/zeek \
    && mkdir -p /var/log/suricata /opt/zeek/logs /var/ossec/logs /opt/security \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 1514 1515 55000
WORKDIR /opt/security
ENTRYPOINT ["/entrypoint.sh"]
