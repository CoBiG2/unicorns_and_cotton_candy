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

parser = argparse.ArgumentParser(description="Tool that performs miscellaneous "
                                             "operations on genome files")

parser.add_argument("-in", dest="genome_file", help="The input genome file in "
                    "Fasta format")

arg = parser.parse_args()


def main():
    # Arguments
    genome_file = arg.genome_file

main()

__author__ = 'diogo'
