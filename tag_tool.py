#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  tag_tool.py
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
#

import argparse
import parser as ps

parser = argparse.ArgumentParser(description="Tool for processing of stacks "
                                             "tag files")

parser.add_argument("-in", dest="tag_file", nargs="*", help="The input tags "
                    "file")
parser.add_argument("--export", dest="export", choices=["fasta", "tsv"],
                    help="Option to export some values of the tsv file into "
                    "new file")
parser.add_argument("--coverage", dest="coverage", action="store_const",
                    const=True, help="Generate a plot with the coverage "
                    "distribution for each RAD tag.")
parser.add_argument("-o", dest="output_file", help="Name for the output file")

arg = parser.parse_args()


def main():
    # Arguments
    if len(arg.tag_file) == 1:
        tag_file = arg.tag_file[0]
    else:
        tag_file = arg.tag_file

    output_filename = arg.output_file

    tag_object = ps.Tags(tag_file)

    if arg.export:

        if "fasta" in arg.export:
            tag_object.export_consensus(output_filename)

    if arg.coverage:
        tag_object.coverage()

main()