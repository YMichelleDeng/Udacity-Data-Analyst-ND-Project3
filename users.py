#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

""" Load the OSM file """
OSMFILE = "hksample.osm"


def get_user(element):
    return


def process_map(filename):
    """ count the user id in the filename. """
    users = set()
    users = {}
    for _, element in ET.iterparse(filename):
        if element.tag == "node" or element.tag =="way" or element.tag =="relation": 
            for tag in element.iter(element.tag):
                uid = tag.get("uid")
                if uid not in users.keys():
                    users[uid] = 1
        pass
    return users


def test():

    users = process_map(OSMFILE)
    pprint.pprint(users)
    # assert len(users) == 6



if __name__ == "__main__":
    test()
