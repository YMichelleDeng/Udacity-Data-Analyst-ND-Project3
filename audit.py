#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

""" Load the OSM file """
#OSMFILE = "example.osm"
#OSMFILE = "hksample.osm"
OSMFILE = "hong-kong_china.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
phone_pattern_re = re.compile(r'\D?(\d{0,4}?)\D{0,2}(\d{4})\D?(\d{4})$', re.VERBOSE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Terrace", "Parkway", "Plaza", "Path", "Commons", "Way", "Highway", "Circle"]

phone_expected = ["852"]


# UPDATE THIS VARIABLE
"""Create a dictionary containing possible mistakes"""
mapping = { "St": "Street",
            "St.": "Street",
            "st": "Street",
            "street": "Street",
            "Ave": "Avenue",
            "AVE": "Avenue",
            "Ave.": "Avenue",
            "avenue": "Avenue",
            "Rd.": "Road",
            "Blvd": "Boulevard",
            "Blvd,": "Boulevard",
            "Blvd.": "Boulevard",
            "blvd": "Boulevard",
            "Cres": "Crescent",
            "Ct": "Court",
            "Ctr": "Center",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Hwy": "Highway",
            "Ln.": "Lane",
            "Pl": "Place",
            "Plz": "Plaza",
            "Rd": "Road",
            "Rd.": "Road",
            "parkway": "Parkway",
            "square": "Square",
            
            }


"""Create a dictionary containing possible mistakes"""
phone_mapping = { "", "853"}


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    """Extract street names from osmfile. Perhaps the addr:full should also need to be fixed"""
    return (elem.attrib['k'] == "addr:street") or (elem.attrib['k'] == "addr:full")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                    
    osm_file.close()
    return street_types


def update_name(name, mapping):
    """Fixed the abreviate street names according to the mapping dictionary.""" 
    words = name.split()
    for w in range(len(words)):
        if words[w] in mapping:
           #print words[w]
           words[w] = mapping[words[w]]
           name = " ".join(words)
    return name




def audit_phone_pattern(phone_patterns, phone_number):
    m = phone_pattern_re.search(phone_number)
    if m:
        phone_pattern = m.groups()[0]
        if phone_pattern not in phone_expected:
            phone_patterns[phone_pattern].add(phone_number)


def is_phone_number(elem):
    """Extract phone_numbers from osmfile."""
    return (elem.attrib['k'] == "phone")


def audit_phone(osmfile):
    osm_file = open(osmfile, "r")
    phone_patterns = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_phone_number(tag):
                    audit_phone_pattern(phone_patterns, tag.attrib['v'])
                    
    osm_file.close()
    return phone_patterns


def update_phone(phone, phone_mapping):
    """Fixed the phone numbers. """
    results = []
    for iphone in re.split(',|;',phone):
        patterns = phone_pattern_re.search(iphone)
        if patterns:
            numbers = patterns.groups()
            if numbers[0] == "852":
                results.append(re.compile(r'\D?(\d{0,4}?)\D{0,2}(\d{4})\D?(\d{4})$', iphone))
            elif numbers[0] in phone_mapping:
                results.append ("+852"+ " " + numbers[1] + numbers[2])
            return ';'.join(results)



def test():
    #st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    #pprint.pprint(dict(st_types))

    #for st_type, ways in st_types.iteritems():
    #    for name in ways:
    #        better_name = update_name(name, mapping)
    #        print name, "=>", better_name
    #        if name == "West Lexington St.":
    #            assert better_name == "West Lexington Street"
    #        if name == "Baldwin Rd.":
    #            assert better_name == "Baldwin Road"

    phone_types = audit_phone(OSMFILE)
    pprint.pprint(dict(phone_types))

    for phone_types, ways in phone_types.iteritems():
        for phone in ways:
            better_phone = update_phone(phone, phone_mapping)
            print phone, "=>", better_phone



if __name__ == '__main__':
    test()
