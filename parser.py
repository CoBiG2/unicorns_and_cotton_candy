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
import matplotlib.pyplot as plt
from collections import OrderedDict

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
    """
    To facilitate an efficient parsing of large tsv files, methods of the Tag
    object read the file multiple times instead of storing the information in
    data structures.
    """
    def __init__(self, tag_file):

        self.tag_file = tag_file
        self.line_size = self.__count_lines()

    def __count_lines(self):

        return float(sum(1 for line in open(self.tag_file)))

    def export_column(self, file_name, *args, **kwargs):
        """
        Exports a single or multiple columns of a given tag file, depending
        on certain conditions of the line.
        USAGE:
        :param: file_name, string with the name of the output file
        :param: args, provide the index of the columns to be exported (e.g. 3,5)
        :param: kwargs, provide the conditions to be met following the syntax
        condition = [index] (e.g. consensus=6, will only export columns from
        a line whose column index 6 contains the word consensus)
        """

        tag_handle = open(self.tag_file)
        output_handle = open(file_name, "w")

        for line in tag_handle:
            fields = line.split("\t")

            # Checking conditions
            for ind, condition in kwargs:
                if fields[ind] != condition:
                    continue

            # Exporting values
            values = "".join([line[x] for x in args])

            output_handle.write("%s\n" % values)

        tag_handle.close()
        output_handle.close()

    def export_consensus(self, file_name):
        """
        Exports the consensus sequences from a tsv file into a new Fasta file
        """

        tag_handle = open(self.tag_file)
        output_handle = open(file_name, "w")

        for line in tag_handle:
            fields = line.split("\t")

            if fields[6] == "consensus":
                sequence_id = "locus%s" % fields[2]
                sequence = fields[9]
                output_handle.write(">%s\n%s\n" % (sequence_id, sequence))

        output_handle.close()
        tag_handle.close()


class SNPs():
    """
    Class that deals with snps and alleles files. In the future it could be
    inherited by or inherit the Tags class to perform some operations that
    require both kinds of files
    """

    def __init__(self, snps_file):

        self.snps_file = snps_file

        # Initializing attributes
        self.snp_storage = {}
        self.snp_number = 0

        # Parsing
        print("\rReading snps/allele file", end="")
        self._parse()

    def _count_lines(self):

        return float(sum(1 for line in open(self.snps_file)))

    def _parse(self):

        file_handle = open(self.snps_file)

        for line in file_handle:
            fields = line.split("\t")

            # Add to SNP counter
            self.snp_number += 1

            # Fields of interest
            # Skips empty or badly structured strings
            try:
                locus = fields[2]
                position = fields[3]
                transition = (fields[6], fields[7])
            except IndexError:
                continue

            # Adding to storage
            try:
                self.snp_storage[locus].append((locus, position, transition))
            except KeyError:
                self.snp_storage[locus] = [(locus, position, transition)]

    def get_loci_list(self):
        """ Returns a list with the index number of the loci containing snps """

        return [k for k in self.snp_storage]

    def get_snp_coverage(self, tags_file):
        """
        This will generate a table and histogram reporting the taxa coverage
        for each variable loci.
        :param: tags_file, string with the file name of the tags file
        containing the assembly of stacks for multiple species
        """

        variable_loci = self.get_loci_list()
        data = dict((x, []) for x in variable_loci)

        tag_handle = open(tags_file)

        # Populating data
        print("\rProcessing tags file", end="")
        for tag in tag_handle:
            tag_fields = tag.strip().split("\t")
            locus = tag_fields[2]

            # Checking if current locus has snps
            if locus in variable_loci and data[locus] == []:
                sequence_id_list = set([x.split("_")[0] for x in tag_fields[
                                        8].split(",")])
                data[locus].extend(sequence_id_list)

        # Transforming data into histogram format
        taxa_frequency_list = [len(x) for x in list(data.values()) if x != []]

        # Generating plot
        plt.hist(taxa_frequency_list)
        plt.title("Species frequency per variable loci")
        plt.xlabel("Species number")
        plt.ylabel("Frequency")
        plt.savefig("Species_frequency.png")

        # Generating table
        output_handle = open("Species_frequency.csv", "w")
        table_data = OrderedDict((str(x), 0) for x in range(1, 25))

        for freq in taxa_frequency_list:
            table_data[str(freq)] += 1

        for x, y in table_data.items():
            output_handle.write("%s; %s\n" % (x, y))

        output_handle.close()

#Loads data into array
#db = NoName()
#print(db.primary)
#print db.sequence("7_1116_11084_29627_1")

__author__ = "Bruno Costa, Diogo N. Silva, Francisco Pina-Martins, Joana Fino"
__credits__ = ["Bruno Costa", "Diogo N. Silva", "Francisco Pina-Martins, "
              "Joana Fino"]
__copyright__ = "Copyright 2014, CoBiG²"
__version__ = "1.0"