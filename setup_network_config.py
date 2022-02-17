#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from subprocess import PIPE
import sys

args = sys.argv
malware_repository_ipaddr = args[1]

def run_cmd(cmd):
    proc = subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    return proc

run_cmd("sudo iptables -N  userchain_forward")
run_cmd("sudo iptables -A userchain_forward -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT")
run_cmd("sudo iptables -A userchain_forward -i mybridge -o eth0 -j ACCEPT")
run_cmd("sudo iptables -I FORWARD 1 -j userchain_forward")

run_cmd("sudo iptables -I userchain_forward -p tcp --dport 23 -j DROP")
run_cmd("sudo iptables -I userchain_forward -p udp --dport 23 -j DROP")
run_cmd("sudo iptables -I userchain_forward -p tcp --dport 2323 -j DROP")
run_cmd("sudo iptables -I userchain_forward -p udp --dport 2323 -j DROP")

#iptables input
run_cmd("sudo iptables -N userchain_input")
run_cmd("sudo iptables -I userchain_input -p udp --dport 67 -i mybridge -j ACCEPT")
run_cmd("sudo iptables -I userchain_input -p udp --dport 53 -s 172.20.0.0/16 -j ACCEPT")
run_cmd("sudo iptables -I userchain_input -p tcp --dport 53 -s 172.20.0.0/16 -j ACCEPT")
run_cmd("sudo iptables -I INPUT 1 -j userchain_input")

run_cmd("sudo iptables -I userchain_input -p tcp --dport 23 -j DROP")
run_cmd("sudo iptables -I userchain_input -p udp --dport 23 -j DROP")
run_cmd("sudo iptables -I userchain_input -p tcp --dport 2323 -j DROP")
run_cmd("sudo iptables -I userchain_input -p udp --dport 2323 -j DROP")

## This is to suppress the excessive access to port 23 (telnet) that could be caused by Mirai.
run_cmd("iptables -I INPUT -p tcp -i mybridge --syn --dport 23 -m connlimit --connlimit-above 5 -j REJECT")


proc = subprocess.run(["pgrep", "-f", "dnsmasq"], stdout=PIPE, stderr=PIPE)
dnsmasq_pid = proc.stdout.decode("utf-8")
if len(dnsmasq_pid) > 0:
    run_cmd("pgrep -f dnsmasq | xargs sudo kill -KILL")


run_cmd("sudo brctl addbr mybridge")
run_cmd("sudo ip link set mybridge up")
run_cmd("sudo dnsmasq --interface=mybridge --bind-interfaces --dhcp-range=172.20.222.2,172.20.222.254")
run_cmd("sudo ip addr add 172.20.0.1/16 dev mybridge")
run_cmd("sudo ip tuntap add mode tap vport1 user shun")
run_cmd("sudo brctl addif mybridge vport1")
run_cmd("sudo ifconfig vport1 promisc up")

run_cmd("sudo ip tuntap add mode tap vport2 user shun")
run_cmd("sudo brctl addif mybridge vport2")
run_cmd("sudo ifconfig vport2 promisc up")

run_cmd("sudo iptables -t nat -I POSTROUTING -o mybridge -j MASQUERADE")
# 172.20.222.xxx (Sandbox machine is at 172.20.222.240), redirect to fakedns
run_cmd("sudo iptables -t nat -I PREROUTING -i mybridge -p udp --dport 53 -j DNAT -s 172.20.222.0/24 --to 172.20.100.100:53")

run_cmd("sudo iptables -t nat -I PREROUTING -i mybridge -p tcp --dport 8000 -j DNAT -s 172.20.222.0/24 --to {}:8000".format(malware_repository_ipaddr))

run_cmd("sudo iptables -A INPUT -p tcp --syn -m state --state NEW --dport 8000 -m limit --limit 4/m --limit-burst 4 -j ACCEPT")
run_cmd("sudo iptables -A INPUT -p tcp --syn -m state --state NEW --dport 8000 -j DROP")


activated_port = [21, 22, 23, 25, 443, 990, 1, 995, 37, 7, 9, 6667, 13, 2222, 110, 2223, 79, 80, 2224, 465, 17, 113, 19]
for i in activated_port:
    comm = "sudo iptables -t nat -I PREROUTING -i mybridge -p tcp --dport {port} -j DNAT -s 172.20.222.0/24 --to 172.20.100.100:{port}".format(port=i)
    run_cmd(comm)

#Use "-A" option to add new rule at the end of the chain. As for destination ports from 1 to 65535 that are not set above, direct them to an arbitrary port, 6667 or IRC.
run_cmd("sudo iptables -A PREROUTING -t nat -i mybridge -p tcp --dport 1:65535 -j DNAT --to-destination 172.20.100.100:6667")


#dns setting (backup)
run_cmd("sudo cp /etc/resolv.conf ./resolv.conf.backup")


