#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 23:23:13 2018

@author: sschultz
"""
from datetime import datetime
import json
import sys
from pprint import pprint

import pylatex

from pylatex.base_classes import Environment
from pylatex.package import Package
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import NoEscape, italic, bold
from pylatex.lists import Enumerate, Itemize


import re

convFile=sys.argv[1]

with open(convFile) as data_file:    
    data = json.load(data_file)

#pprint(data)
title=data["title"]
due_date=datetime.strptime(data["due_date"],'%Y-%m-%dT%H:%M:%SZ').date()


#pprint(content)
class amsmath(Environment):
#    """A class to wrap LaTeX's alltt environment."""
#
    packages = [Package('amsmath')]
    escape = False
    content_separator = "\n"
    
def strip(string):
    #strip html tags
    string=re.sub('<[^<]+?>', '', string)
    
    #mathjax stuff
    string=string.replace('\\(','$')
    string=string.replace('\\)','$')
    
    string=string.replace('&amp;','&')
    string=string.replace('&nbsp;', '')
    
    return string

doc = Document()

doc.generate_tex()

doc.preamble.append(Command('title', title))
#doc.preamble.append(Command('author', 'Anonymous author'))
doc.preamble.append(Command('date', due_date))
doc.append(NoEscape(r'\maketitle'))

#TODO: deal with tables
#TODO: deal with q's that aren't multiple choice or T/F

#TODO: need amsmath package

with doc.create(Section('Questions')):
    #i=0
    for q in data["questions"]:

        qTitle=q['title']   
        with doc.create(Subsection(qTitle)):
            content=q['content']
            
            content=strip(content)
            
            doc.append(NoEscape(content))
            if q['content_type']=='question':
                if q['mode']=='multiple' or q['mode']=='true':
                    with doc.create(Enumerate(enumeration_symbol=r"\alph*)")) as enum:

                        for a in q['choices']:
                            ans=a['answer']
                            #change mathjax to standard latex
                            #TODO: fix this (pylatex likes to make them "textblackslash" in latex)
                            ans=strip(ans)        
                            enum.add_item(ans)
    #hack to make sure amsmath package is declared
    with doc.create(amsmath()):
        doc.append('')
            

tex = doc.dumps()
doc.generate_tex('./test2Tex_1')