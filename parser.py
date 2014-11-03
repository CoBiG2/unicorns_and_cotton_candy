#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  parser.py
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
#

import argparse

parser = argparse.ArgumentParser(description="Remote tool to getting zones or "
                                 "links or something for rad sequence data "
                                 "Creates a map or something")

parser.add_argument("-d", dest="dir", help="Optional, if provided searches the"
                    " specified directory for tags.tsv files, if no file"
                    " directory is provided uses current dir.")

arg = parser.parse_args()

#import string
import re
import glob

path_tags = arg.dir

tag_files = []

#Gets an array of tag.tsv files.
if path_tags is None:
    tag_files = glob.glob("*.tags.tsv")
else:
    tag_files = glob.glob(path_tags + "/*.tags.tsv")


class Rad(object):
    def __init__(self):

        #Initializing main attributes ordered as in Stacks manual
        self.sequence = None
        self.strand = None
        self.locus = None
        #mudar nome nao sei se intressa ou o que e
        self.SECnd_El = None
        self.type = None


class NoName(object):
    def __init__(self):
        #loads data
        primary = []
        secondary = []
        for i in tag_files:
            tag = open(i, "r")
            for tag_line in tag:
                #pre parses line removing consequetive tabs
                pre = re.split("\t+", tag_line)
                if pre[3] == "model":
                    if re.search("E", pre[4]):
                        add = True
                    else:
                        add = False
                if pre[3] == "primary":
                    if add:
                        linha = Rad()
                        linha.seq = pre[6]
                        linha.strand = "+"
                        linha.locus = pre[1]
                        linha.SECnd_El = pre[2]
                        linha.type = "primary"
                        primary.append([pre[5], linha])

                if pre[3] == "secondary":
                    if add:      
                        linha = Rad()
                        linha.seq = pre[5]
                        linha.strand = "-"
                        linha.locus = pre[1]
                        linha.SECnd_El = pre[2]
                        linha.type = "secondary"
                        primary.append([pre[5], linha])
        self.primary = dict(primary)
        self.secondary = dict(secondary)

    def merge(self):
        #merges primary reads? with secundary reads?
        print("Merged")

    def sequence(self, id):
        #returns the sequence for the id
        return self.primary[id].seq

#Loads data into array
db = NoName()
print(db.primary)
#print db.sequence("7_1116_11084_29627_1")

__author__ = "Bruno Costa, Diogo N. Silva, Francisco Pina-Martins, Joana Fino"
__credits__ = ["Bruno Costa", "Diogo N. Silva", "Francisco Pina-Martins, "
              "Joana Fino"]
__copyright__ = "Copyright 2014, CoBiG²"
__version__ = "1.0"