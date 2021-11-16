#!/usr/bin/env bash

set -eu -o pipefail

function setup_iface() {
  local w_iface=${1:-wlp6s0}
  local channel=${2:-12}
  local mon_iface="mon${channel}"

  if [ ! -d "/sys/class/net/${w_iface}" ]; then
    echo "Could not find interface '${w_iface}'" >&1
    return 1
  fi
  if [ -d "/sys/class/net/${mon_iface}" ]; then
    echo "interface already exists: '${mon_iface}'" >&1
    return 1
  fi

  local phy_index
  phy_index="$(cat "/sys/class/net/${w_iface}/phy80211/index")"
  
  sudo iw dev "${w_iface}" del
  sudo iw phy "phy${phy_index}" interface add "${mon_iface}" type monitor
  sudo ip link set "${mon_iface}" up
  sudo iw dev "${mon_iface}" set channel "${channel}"
}

if [ $# -ne 2 ]; then
  echo "Quick and drity tool to simplify putting a 802.11 interface in monitoring mode."
  echo "Monitoring interface are named mon<channel>, e.g. mon12"
  echo "Usage: $(basename $0) <wifi-interface> <channel>"
  exit 1
fi

setup_iface $1 $2
