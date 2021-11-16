#!/usr/bin/env python3
import argparse
import logging
import os
import sys

import pandas
from matplotlib import pyplot as plt
from tabulate import tabulate

from rtl8xxxu.analyze import get_metadata, process_pcap_file

log = logging.getLogger("rtl8xxxu_visualize")


def pandas_series(file_name, mac_ap: str, mac_sta: str):
    results = process_pcap_file(file_name, mac_ap, mac_sta)
    d = {r.name: r for r in results}

    jobs = [
        # Title, Test, Value
        ('Global: Packets', 'Total', d['global'].count),
        ('Global: Packets', 'Retries', d['global.retries'].count),
        ('Network: Packets', 'Total', d['global.network'].count),
        ('Network: Packets', 'By AP', d['global.network.by_ap'].count),
        ('Network: Packets', 'By DUT', d['global.network.by_dut'].count),
        ('Network: Packets', 'By other senders', d['global.network.by_others'].count),
        ('Network: Packets', 'By unknown senders', d['global.network.no_ta'].count),
        ('Network: Retry fraction', 'By AP', d['global.network.by_ap.retries']/d['global.network.by_ap']),
        ('Network: Retry fraction', 'By DUT', d['global.network.by_dut.retries']/d['global.network.by_dut']),
        ('Network: PHY Rate', 'By AP: 802.11b', d['global.network.by_ap.802_11b'].count),
        ('Network: PHY Rate', 'By DUT: 802.11b', d['global.network.by_dut.802_11b'].count),
        ('Network: PHY Rate', 'By AP: 802.11g', d['global.network.by_ap.802_11g'].count),
        ('Network: PHY Rate', 'By DUT: 802.11g', d['global.network.by_dut.802_11g'].count),
        ('Network: PHY Rate', 'By AP: 802.11n', d['global.network.by_ap.802_11n'].count),
        ('Network: PHY Rate', 'By DUT: 802.11n', d['global.network.by_dut.802_11n'].count),
        ('Network: Block ACK', 'Requests', d['global.network.ba_requests'].count),
        ('Network: Block ACK', 'Replies', d['global.network.ba_replies'].count),
    ]

    print(tabulate(jobs))

    return pandas.Series(
        [job[2] for job in jobs],
        index=pandas.MultiIndex.from_tuples([(t[0], t[1]) for t in jobs], names=['Title', 'Value']),
        dtype=float)


def main():
    parser = argparse.ArgumentParser(description="rtl8xxxu PCAP analyzer")
    parser.add_argument('pcap', metavar='<PCAP file name>', type=str, nargs='+', help="PCAP file to parse")
    parser.add_argument("--sta", metavar="<STA MAC address>", type=str, required=True)
    parser.add_argument("--ap", metavar="<AP MAC address>", type=str, required=True)
    parser.add_argument("-v", "--verbose",
                        dest='verbose_count',
                        action='count',
                        default=0,
                        help="Increase log verbosity for each occurrence.")
    args = parser.parse_args()
    log_level = max(3 - args.verbose_count, 1) * 10
    log.setLevel(log_level)
    log.info(f"Setting logging level to {log_level}")

    series = {}
    for file_name in args.pcap:
        if not os.path.isfile(file_name):
            log.error(f'"{file_name}" does not exist')
            sys.exit(-1)
        driver_name, driver_version, _, direction = get_metadata(file_name)
        key = (driver_name, driver_version, direction)
        if key in series:
            log.error(f"Multiple PCAP files for {driver_name}, {driver_version}, {direction}")
            sys.exit(-1)
        series[key] = pandas_series(file_name, args.ap, args.sta)
        # series[key].name = f"{driver_name}: {direction}"

    multi_index = pandas.MultiIndex.from_tuples(series.keys(), names=['Driver', 'Version', 'Direction'])
    df = pandas.DataFrame(series.values(), index=multi_index)
    for title in dict.fromkeys(df.axes[1].get_level_values('Title')):
        ax = df[title].plot.bar(title=title, table=True, xticks=[], fontsize=10)
        ax.set_xlabel(None)
        ax.tables[0].auto_set_font_size(False)
        ax.tables[0].set_fontsize(5)
        plt.subplots_adjust(bottom=.25)
    plt.show()

    sys.exit(0)


if __name__ == '__main__':
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    main()
