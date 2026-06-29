#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage: $(basename "$0") <host_web_interface> <robot_web_interface>

Enable IP forwarding and NAT so traffic from the robot subnet (192.168.123.0/24)
can reach the host network via the host web interface.

Arguments:
  host_web_interface   Outbound interface (e.g. eno1)
  robot_web_interface  Interface on the robot subnet (e.g. eno2)
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -ne 2 ]]; then
  usage >&2
  exit 1
fi

host_web_interface="$1"
robot_web_interface="$2"

# 1. Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# 2. NAT traffic from the robot subnet out through the host web interface
sudo iptables -t nat -A POSTROUTING -s 192.168.123.0/24 -o "$host_web_interface" -j MASQUERADE

sudo iptables -A FORWARD -i "$robot_web_interface" -o "$host_web_interface" -j ACCEPT

sudo iptables -A FORWARD -i "$host_web_interface" -o "$robot_web_interface" -m state --state RELATED,ESTABLISHED -j ACCEPT
