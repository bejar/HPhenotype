"""
.. module:: Ontology

Ontology
*************

:Description: Ontology

    Data structure for storing a ontology
    
    First implementation as dictionaries double indexing parents, descendants
    
    Later we can use a graph library

:Authors: bejar
    

:Version: 

:Created on: 18/05/2017 9:26 

"""

import gzip
from collections import deque
from rdflib import Graph, Literal
from rdflib.namespace import XSD, OWL, RDF, RDFS
from HPhenotype.Ontology.Properties import obo_id
from HPhenotype.Data.TermInfo import TermInfo

__author__ = 'bejar'

class BioOntology:
    """
    Class for representing an ontology
    """

    down = None
    up = None
    downDB = None
    upDB = None
    ofile = None
    parent_term = None
    dbase = None
    inmemory = True
    terms_info = None

    def __init__(self, ofile, pterm, dbase=None, inmemory=False):
        """
        Creates the empty 
        :param pterm: 
        """
        self.ofile = ofile
        self.parent_term = pterm
        self.down = {}
        self.up = {}
        self.dbase = dbase
        self.inmemory = inmemory
        self.terms_info = {}

    def load_from_file(self):
        """
        Loads the ontology from a RDF file extracting all the nodes that recursivelly descend from
        the parent term using breadth first traversal
        
        :return: 
        """

        ontograph = Graph()
        ontofile = gzip.open(self.ofile)
        ontograph.parse(ontofile)

        term_set = set()
        pending = deque()

        pending.append(self.parent_term)
        term_set.add(self.parent_term)
        lterms = []
        while len(pending) != 0:
            term = pending.popleft()
            lterms.append(term)
            candidates = [a for a, _, _ in ontograph.triples((None, RDFS.subClassOf, term))]
            term_id = str(term).split('/')[-1].replace('_', ':')
            self.down[term_id] = []
            self.terms_info[term_id] = TermInfo(term_id)
            for c in candidates:
                desc_id = str(c).split('/')[-1].replace('_', ':')
                self.down[term_id].append(desc_id)
                if desc_id not in self.up:
                    if desc_id != term_id:
                        self.up[desc_id] = [term_id]
                    # else:
                    #     print desc_id
                else:
                    if desc_id not in self.up[desc_id]:
                        self.up[desc_id].append(term_id)
                    # else:
                    #     print desc_id
                if c not in term_set:
                    pending.append(c)
                    term_set.add(c)

    def compute_level(self):
        """
        Computes the depth level of each term in the ontology
        :return: 
        """
        term_set = set()
        term_set.add(str(self.parent_term).split('/')[-1].replace('_', ':'))

        currlevel = []
        currlevel.append(str(self.parent_term).split('/')[-1].replace('_', ':'))

        nlevel = 0
        while len(currlevel) != 0:
            pending = []
            for term in currlevel:
                candidates = self.down[term]
                for c in candidates:
                    if c not in term_set:
                        pending.append(c)
                        term_set.add(c)
                self.terms_info[term].level = nlevel
            nlevel += 1
            currlevel = pending


if __name__ == '__main__':

    from HPhenotype.Config import HPHonto, GOonto
    from HPhenotype.Ontology.Classes import pheno_abno_c, biol_proc_c, cell_comp_c, mole_func_c
    onto = BioOntology(HPHonto, pheno_abno_c)

    onto.load_from_file()



    # for o in onto.descendants:
    #     print o, onto.descendants[o]

    # for o in onto.ascendants:
    #     print o, onto.ascendants[o]

    onto.compute_level()

    llev = sorted([(onto.terms_info[t].level,t) for t in onto.terms_info])

    for v in llev:
        print v
