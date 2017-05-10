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
from HPhenotype.Ontology.Namespaces import oboInOwl, obo, go
from HPhenotype.Ontology.Literals import biol_proc, cell_comp, mole_func, human_phen
from HPhenotype.Ontology.Properties import has_OBO_ns
from HPhenotype.Ontology.Classes import pheno_abno_c
from rdflib import Graph, Literal
from rdflib.namespace import XSD, OWL, RDF, RDFS
import gzip

__author__ = 'bejar'

if __name__ == '__main__':

    g = Graph()
    ontofile = gzip.open(HPHonto)
    g.parse(ontofile)

    term_set = set()

    mf = [a for a,_,_ in g.triples((None, RDFS.subClassOf, pheno_abno_c))]
    print len(mf)
    print mf

