#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  snp_tool.py
#
# Copyright 2014 CoBiG^2
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

import argparse
import parser as ps

parser = argparse.ArgumentParser(description="Tool for processing of stacks "
                                             "snp and allele files")

parser.add_argument("-in", dest="snp_file", help="The input snps or allele "
                    "file")
parser.add_argument("-s", dest="stats", nargs="*", choices=["1", "2"],
                    help="Generate descriptive stats. 1: Histogram of species "
                    "coverage per variable locus; 2: Histogram of number of "
                    "SNPs per locus and general information on snps")
parser.add_argument("-tags", dest="tags_file", help="Provide auxiliary tags "
                    "file. Required for some operations")
parser.add_argument("-o", dest="output_file", help="Name for the output file")

arg = parser.parse_args()


def main():
    # Arguments
    infile = arg.snp_file
    outfile = arg.output_file

    # Initializing SNPs object
    snp_obj = ps.SNPs(infile)

    # Perform operations
    if arg.stats:
        if "1" in arg.stats:
            snp_obj.get_snp_coverage(arg.tags_file)

        if "2" in arg.stats:
            snp_obj.snp_statistics()

main ()