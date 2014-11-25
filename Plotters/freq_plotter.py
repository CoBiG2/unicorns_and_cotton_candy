#!/usr/bin/python3
#  freq_plotter.py
#
# Copyright 2014 CoBiG^2 <f.pinamartins@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

# Usage: python3 freq_plotter freq_file.txt graph_type
# graph_type can be either "c" for cumulative graph or "f" for frequency graph.

import numpy as np
import matplotlib.pyplot as plt
from sys import argv
from collections import OrderedDict


def parser(filename):
    """Parse the frequencies file. Returns an OrderedDict."""
    infile = open(argv[1], "r")

    d = OrderedDict()
    for lines in infile:
        lines = lines.strip()
        if lines != "0":
            lines = str(int(int(lines)/2))
        if lines in d:
            d[lines] += 1
        else:
            d[lines] = 1

    infile.close()

    return d


def freq_plotter(d):
    """Plot the frequencies of the SNPs per missing individuals."""
    n_groups = len(d)
    groups = list(d.keys())

    SNPs = [d[i] for i in groups]

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.7

    rects1 = plt.bar(index, SNPs, bar_width, color='grey')

    plt.xlabel('Number of missing individuals')
    plt.ylabel('Number of SNPs')
    plt.title('Distribution of missing SNPs')
    plt.xticks(index + bar_width/2, groups)
    plt.legend()

    plt.tight_layout()
    plt.show()


def comul_plotter(d):
    """Plot the cumulative frequencies of the SNPs per missing individuals."""
    n_groups = len(d)
    groups = list(d.keys())
    SNPs = np.cumsum(np.array(list(d.values())))

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.7

    rects1 = plt.bar(index, SNPs, bar_width, color='grey')

    plt.xlabel('Number of missing individuals')
    plt.ylabel('Number of SNPs')
    plt.title('Cumulative distribution of missing SNPs')
    plt.xticks(index + bar_width/2, groups)
    plt.legend()

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    d = parser(argv[1])
    if argv[2] == "c":
        comul_plotter(d)
    elif argv[2] == "f":
        freq_plotter(d)
    else:
        print("Error, please specify the plot type (\"c\" or \"f\")")
