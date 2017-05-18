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

__author__ = 'bejar'

class BioOntology:
    """
    Class for representing an ontology
    """

    descendants = None
    ascendants = None
    ofile = None
    parent_term = None

    def __init__(self, ofile, pterm):
        """
        Creates the empty 
        :param pterm: 
        """
        self.ofile = ofile
        self.parent_term = pterm
        self.descendants = {}
        self.ascendants = {}

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
            term_id = str(term).split('/')[-1]
            self.descendants[term_id] = []
            for c in candidates:
                desc_id = str(c).split('/')[-1]
                self.descendants[term_id].append(desc_id)
                if desc_id not in self.ascendants:
                    if desc_id != term_id:
                        self.ascendants[desc_id] = [term_id]
                    else:
                        print desc_id
                else:
                    if desc_id not in self.ascendants[desc_id]:
                        self.ascendants[desc_id].append(term_id)
                    else:
                        print desc_id
                if c not in term_set:
                    pending.append(c)
                    term_set.add(c)

if __name__ == '__main__':

    from HPhenotype.Config import HPHonto, GOonto
    from HPhenotype.Ontology.Classes import pheno_abno_c, biol_proc_c, cell_comp_c, mole_func_c
    onto = BioOntology(GOonto, biol_proc_c)

    onto.load_from_file()

    # for o in onto.descendants:
    #     print o, onto.descendants[o]
    #
    # for o in onto.ascendants:
    #     print o, onto.ascendants[o]
