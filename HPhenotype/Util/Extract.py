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
    Extracts all the terms from an ontology (RDFlib Graph) that are descendent from a term 
    Breadth first traversal 
    
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
        candidates = [a for a, _, _ in ontograph.triples((None, RDFS.subClassOf, term))]
        for c in candidates:
            if c not in term_set:
                pending.append(c)
                term_set.add(c)
    return lterms


def hierarchy_terms_depth(ontograph, term):
    """
    Returns all the terms from an ontology (RDFlib Graph) that are descendent from a term
    including the first term
    :param ontograph: 
    :param term: 
    :return: 
    """
    term_set = set()
    term_set.add(term)

    currlevel = []
    currlevel.append(term)

    lterms = []
    nlevel = 0
    leaves = 0
    brf = 0
    noleaves = 0
    while len(currlevel) != 0:
        pending = []
        for term in currlevel:
            candidates = [a for a, _, _ in ontograph.triples((None, RDFS.subClassOf, term))]
            if len(candidates) != 0:
                noleaves += 1
                brf += len(candidates)
                for c in candidates:
                    if c not in term_set:
                        pending.append(c)
                        term_set.add(c)
                lterms.append((term, nlevel, 'NL'))
            else:
                leaves += 1
                lterms.append((term, nlevel, 'L'))
        print nlevel, len(currlevel)
        nlevel += 1
        currlevel = pending
    print 'L=', leaves, 'NL=', noleaves, 'MBF=', float(brf/noleaves)
    return lterms
