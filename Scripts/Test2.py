"""
.. module:: Test2

Test2
*************

:Description: Test2

    

:Authors: bejar
    

:Version: 

:Created on: 10/05/2017 13:42 

"""

from HPhenotype.Config import GOonto, HPHonto
from HPhenotype.Ontology.Literals import biol_proc, cell_comp, mole_func, human_phen
from HPhenotype.Ontology.Properties import has_OBO_ns
from HPhenotype.Ontology.Classes import pheno_abno_c, biol_proc_c, cell_comp_c, mole_func_c
from HPhenotype.Util.Extract import hierarchy_breadth_first, hierarchy_terms_depth
from rdflib import Graph, Literal
from rdflib.namespace import XSD, OWL, RDF, RDFS
import gzip
from collections import deque
__author__ = 'bejar'

if __name__ == '__main__':

    g = Graph()
    ontofile = gzip.open(GOonto)
    g.parse(ontofile)
    lterms = hierarchy_terms_depth(g, biol_proc_c)
    lterms = hierarchy_terms_depth(g, cell_comp_c)
    lterms = hierarchy_terms_depth(g, mole_func_c)

    g = Graph()
    ontofile = gzip.open(HPHonto)
    g.parse(ontofile)
    lterms = hierarchy_terms_depth(g, pheno_abno_c)


    # for t in lterms:
    #     lab = [str(l) for _, _, l in g.triples((t[0], RDFS.label, None))]
    #     print t, lab
    #
    # print len(lterms)

