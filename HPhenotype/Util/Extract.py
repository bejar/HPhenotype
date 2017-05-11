"""
.. module:: Extract

Extract
*************

:Description: Extract

    

:Authors: bejar
    

:Version: 

:Created on: 10/05/2017 14:43 

"""

import gzip
from collections import deque
from rdflib import Graph, Literal
from rdflib.namespace import XSD, OWL, RDF, RDFS

__author__ = 'bejar'


def hierarchy_breadth_first(ontograph, term):
    """
    Extracts levelwise all the terms from an ontology (RDFlib Graph) that are descendent from a term 
    
    (includes the term)
    
    :param ontofile: 
    :param term: 
    :return: 
    """

    term_set = set()
    pending = deque()

    pending.append(term)
    term_set.add(term)
    lterms = []
    while len(pending) != 0:
        term = pending.popleft()
        lterms.append(term)
        candidates = [a for a,_,_ in ontograph.triples((None, RDFS.subClassOf, term))]
        for c in candidates:
            if c not in term_set:
                pending.append(c)
                term_set.add(c)
    return lterms