#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage: $(basename "$0") <host_ip>

Configure the robot to route traffic through the host PC for NAT.

Arguments:
  host_ip   IP address of the host on the robot subnet (e.g. 192.168.123.200)

Test connectivity after running:
  ping -c 2 8.8.8.8       # test connectivity
  ping -c 2 google.com    # test DNS
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -ne 1 ]]; then
  usage >&2
  exit 1
fi

host_ip="$1"

# Set gateway to your PC
sudo ip route add default via "$host_ip"

# Set DNS
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
