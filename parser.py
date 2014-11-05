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

#import argparse

#parser = argparse.ArgumentParser(description="Remote tool to getting zones or "
                                 #"links or something for rad sequence data "
                                 #"Creates a map or something")

#parser.add_argument("-d", dest="dir", help="Optional, if provided searches the"
                    #" specified directory for tags.tsv files, if no file"
                    #" directory is provided uses current dir.")

#arg = parser.parse_args()

#import string
#import re
#import glob

#path_tags = arg.dir

#tag_files = []

#Gets an array of tag.tsv files.
#if path_tags is None:
#    tag_files = glob.glob("*.tags.tsv")
#else:
#    tag_files = glob.glob(path_tags + "/*.tags.tsv")


class Rad(object):
    """
    As it is, creating an object for each line in a tags file consumes an
    excessive amount of memory. Usage discouraged.
    """
    def __init__(self, string):

        self.string = string

        # Initializing main attributes ordered as in Stacks manual
        self.locus = None
        self.type = None
        self.sequence_id = None
        self.sequence = None
        #self.strand = None

        # Parsing string
        self.parse_string()

    def parse_string(self):
        """ Parses a line of a tsv file from stacks and retrieves information
        for several attributes """

        string_fields = self.string.strip().split("\t")

        self.locus = string_fields[2]
        self.type = string_fields[6]

        if self.type != "consensus" or self.type != "model":
            self.sequence_id = string_fields[8]

        if self.type != "model":
            self.sequence = string_fields[9]


class Tags(object):

    def __init__(self, tag_file):

        self.tag_file = tag_file

        tag_handle = open(self.tag_file)

    def __count_lines(self):

        return float(sum(1 for line in open(self.tag_file)))

    def get_sequence(self, sequence_id):
        #returns the sequence for the id

        return next((x for x in self.rad_object_list if x.sequence_id ==
                     sequence_id), None)

    def get_consensus(self):

        return [x.sequence for x in self.rad_object_list if x.type ==
                "consensus"]

#Loads data into array
#db = NoName()
#print(db.primary)
#print db.sequence("7_1116_11084_29627_1")

__author__ = "Bruno Costa, Diogo N. Silva, Francisco Pina-Martins, Joana Fino"
__credits__ = ["Bruno Costa", "Diogo N. Silva", "Francisco Pina-Martins, "
              "Joana Fino"]
__copyright__ = "Copyright 2014, CoBiG²"
__version__ = "1.0"