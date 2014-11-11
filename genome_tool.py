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

import re
import argparse

parser = argparse.ArgumentParser(description="Tool that performs miscellaneous "
                                             "operations on genome files")

parser.add_argument("-in", dest="genome_file", help="The input genome file in "
                    "Fasta format")
parser.add_argument("-r", dest="restriction_enzyme", help="Digest the genome "
                    "with one or more restriction enzymes. For now it will "
                    "only print the number of fragments expected from a "
                    "digestion. Provide the name(s) of the enzyme(s) "
                    "separated by spaces (e.g. SBFI PSTI)")
parser.add_argument("--add-enzyme", dest="add_enzyme", nargs="*", help="Add "
                    "new enzyme. For each enzyme, three fields must be "
                    "entered: [enzyme_name enzyme_string cut_site]. For "
                    "example to add SBFI this option should be used as "
                    "follows: SBFI CCTGCAGG 6.")

arg = parser.parse_args()


def parser(file_string):
    """
    Simple fasta parser that returns a dictionary with contig name as key
    and sequence as value
    :param file_string: Fasta file name
    """

    file_handle = open(file_string)
    contig_storage = {}

    for line in file_handle:
        if line.startswith(">"):
            contig_name = line[1:].strip()
            contig_storage[contig_name] = ""

        else:
            sequence = line.strip()
            try:
                contig_storage[contig_name] += sequence
            except KeyError:
                raise SystemError("Possibly badly formatted fasta file?")

    return contig_storage


class Genome():
    """
    A genome class that contains in its simplest form, a dictionary with the
    contigs and sequences. I created this as a class so that several methods
    that process/modify the genome dictionary can be easily added and
    share/set common attributes
    """

    def __init__(self, dic_object):
        """
        Initialization of a Genome object only requires a dictionary for now
        :param dic_object: Methods for Genome object will assume the
        dictionary has some sort of sequence name as keys and sequence as values
        """

        self.genome_lib = dic_object

    @staticmethod
    def _set_enzyme_table(self, **kwargs):

        self.enzyme_table = {"SBFI": ["CCTGCAGG", 6],
                        "PSTI": ["CTGCAG", 5],
                        "NSII": ["ATGCAT", 5],
                        "NOTI": ["GCGGCCGC", 2],
                        "EAEI": ["YGGCCR", 1],
                        "EAGI": ["CGGCCG", 1],
                        "ECORI": ["GAATTC", 1],
                        "APOI": ["RAATTY", 1],
                        "MFEI": ["CAATTG", 1],
                        "BAMHI": ["GGATCC", 1],
                        "BCLI": ["TGATCA", 1],
                        "BGLII": ["AGATCT", 1],
                        "BSTYI": ["RGATCY", 1],
                        "BBVCI": ["CCTCAGC", 1],
                        "SPHI": ["GCATGC", 5],
                        "MSPI": ["GCGG", 1],
                        "MLUCI": ["AATT", 0],
                        "NLAIII": ["CATG", 4]}

        for key, val in kwargs:
            self.enzyme_table[key] = val

    def digest(self, *args):
        """
        This method simulates the results of digesting a genome with one or
        more restriction enzymes
        :param args: A list containing the restriction enzyme names that will
        digest the genome
        :return:
        """

        fragment_number = 0

        for contig, sequence in self.genome_lib.items():

            # Restarting all_hits for each sequence
            all_hits = []

            for enzyme in args:
                try:
                    enzyme_string = self.enzyme_table[enzyme.upper()][0]
                    cut_mismatch = self.enzyme_table[enzyme.upper()][1]

                    # Find all instances of the restriction site substring in
                    # the sequence and adds the distance of the actual cut site
                    all_hits.extend([(x.start() + cut_mismatch) for x in
                                    re.finditer(enzyme_string, sequence)])

                # Handle common exception of providing a non-existent
                # restriction enzyme name
                except KeyError:
                    raise SystemError("The enzyme %s is not present on the "
                                      "restriction enzyme table. Use "
                                      "_set_enzyme_table to add new enzymes." %
                                      enzyme)

            # Once the restriction sites have been recorded for all enzymes,
            # get the number of fragments
            else:
                fragments = []
                start = 0

                for hit in all_hits:
                    fragments.append(sequence[start:hit])

                    #Updating start for next cut site
                    start = hit + 1
                else:
                    fragments.append(sequence[start:])

                # Right now I only want the number of fragments but the
                # method has been written so that further operations may be
                # performed
                fragment_number += len(fragments)

        return fragment_number


def main():
    # Arguments
    genome_file = arg.genome_file

main()

__author__ = 'diogo'
