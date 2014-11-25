#!/usr/bin/python3

#Usage: python3 freq_plotter freq_file.txt

import numpy as np
import matplotlib.pyplot as plt
from sys import argv
from collections import OrderedDict


def parser(filename):
    infile = open(argv[1],"r")

    d = OrderedDict()
    for lines in infile:
        lines=lines.strip()
        if lines != "0":
            lines = str(int(int(lines)/2))
        if lines in d:
            d[lines] += 1
        else:
            d[lines] = 1

    return d

def freq_plotter(d):
    '''Plots the frequencies of the SNPs per missing individuals'''
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
    '''Plots the cumulative frequencies of the SNPs per missing individuals'''
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


d = parser(argv[1])
comul_plotter(d)
