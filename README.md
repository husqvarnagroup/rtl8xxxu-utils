# Utilities to assist rtl8xxxu development

## Setup

### Dependencies

```console
pip install -r requirements.txt
```

The scripts have been developed using Python 3.9.

### Devices

- Controller:
    - Has a Wi-Fi device capable of monitoring the channel used by the AP
    - Runs the tools in this repo. Therefore, also builds Linux with its (mainlined) drivers rtl8xxxu and rtl8192cu, as
      well as 8192cu
    - Is part of two (Ethernet) networks:
        - Productive
        - Testing
- Device under Test (DUT):
    - Machine with a RTL8192CUS dongle attached
    - Connected to the productive network
- Access Point (AP):
    - Connected to the testing network

#### Configurations

- DUT: Controller must be able to log into as root user
- AP: Ideally configured to use a non-crowded channel

## Drivers

### rtl8xxxu

- Needs to be built as module and with support for untested chips (CONFIG_RTL8XXXU_UNTESTED=y)
- Patch to register dumping:
  - https://github.com/husqvarnagroup/linux/commit/64c722b8cd7d2cc16e587c0be997780a466def10

### rtlwifi/rtl8192cu

- Needs to be built as module
- Patches for register dumping:
  - https://github.com/husqvarnagroup/linux/commit/b4a9229537aeae83d8e26dca3a9318783a9edb5c
  - https://github.com/husqvarnagroup/linux/commit/887652ea97026e1fb1cefc1b666648ba284aebf0
  - https://github.com/husqvarnagroup/linux/commit/ba3a6055dab637dbff60d73663349a11c8035c22

### 8192cu

- Vendor driver patched to allo register dumping and work with Linux 5.10, cfg80211:
 - https://github.com/husqvarnagroup/rtl8xxxu-8192cu-for-rtl8188cus

## Benchmark

Example usage:

```console
./rtl8xxxu_benchmark.py --log-level INFO \
 --dut machine-with-rtl8188cus-dongle \
 --driver rtl8192cu \
 --direction tx \
 --mon-interface wifi-inteface-in-monitoring-mode \
 --network-ssid rtl8xxxu-testwifi \
 --network-psk=very-secure \
 --linux-build-directory "$HOME/code/3rd-party/build-linux-amd64-5.10"
```

Please note:

- The Linux build directory must be configured and its kernel running on the DUT ahead of the testrun

## Diff Register Dumps

```console
./rtl8xxxu_register_dump_diff.py $HOME/code/3rd-party/linux/drivers/net/wireless/realtek/rtl8xxxu/rtl8xxxu_regs.h latest/*.reg_dump
```

## Analyze PCAP

```console
./rtl8xxxu_analyze.py --ap 00:a0:c5:d0:30:22 --sta 74:da:38:0e:49:7d latest/*pcap
```

## Abbreviations

The code base uses abbreviations extensively, many of which are never fully spelled out. This section attempts to
document them. Please take this with a grain of salt, most of this is just googled!

* ADDA: Analog Digital Digital Analog
* IQ: The term "I/Q" is an abbreviation for "in-phase" and "quadrature."
* PI mode: ?
* SI mode: ?
