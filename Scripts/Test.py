"""
.. module:: Test

Test
*************

:Description: Test

    

:Authors: bejar
    

:Version: 

:Created on: 10/05/2017 10:35 

"""

from HPhenotype.Config import GOonto, HPHonto
from HPhenotype.Ontology.Namespaces import oboInOwl, obo, go
from HPhenotype.Ontology.Literals import biol_proc, cell_comp, mole_func
from HPhenotype.Ontology.Properties import has_OBO_ns
from rdflib import Graph, Literal
from rdflib.namespace import XSD, OWL
import gzip

__author__ = 'bejar'

if __name__ == '__main__':

    g = Graph()

    ontofile = gzip.open(GOonto)
    g.parse(ontofile)

    mf = [a for a,_,_ in g.triples((None, oboInOwl.hasOBONamespace, biol_proc))]
    print len(mf)

    mf = [a for a,_,_ in g.triples((None, oboInOwl.hasOBONamespace, cell_comp))]
    print len(mf)

    mf = [a for a,_,_ in g.triples((None, oboInOwl.hasOBONamespace, mole_func))]
    print len(mf)

