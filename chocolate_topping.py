#!/usr/bin/python3

# Copyright 2014 CoBiG^2 <f.pinamartins@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Bruno Costa
# Author: Francisco P Martins
# Author: Joana Fino
# Last update: 03/10/2014

#Usage: python3 chocolate_topping.py file.tags.tsv
from sys import argv

def parser(tags_filename):
    '''Parses the tags.tsv file and returns a dict with the id of
    loci that have SNPs, and the reads that compose it.'''
    infile = open(tags_filename,  'r')
    loci_data = {}
    for lines in infile:
        lines = lines.split()
        if lines[-1] == "0":
            parse = 0
        elif lines[3] == "model":
            if  "E" in lines[4]:
                parse = 1
        elif parse == 1:
            locus_id = str(lines[2])
            if locus_id in loci_data:
                if lines[3] == "primary":
                    loci_data[locus_id].append(lines[5])
                else:
                    loci_data[locus_id].append(lines[4])
            else:
                if lines[3] == "primary":
                    loci_data[locus_id] = [lines[5]]
                else:
                    loci_data[locus_id] = [lines[4]]

    return(loci_data)

if __name__ == "__main__":
    loci = parser(argv[1])
    print(loci)
