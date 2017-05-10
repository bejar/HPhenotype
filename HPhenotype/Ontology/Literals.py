"""
.. module:: Literals

Literals
*************

:Description: Literals

    

:Authors: bejar
    

:Version: 

:Created on: 10/05/2017 13:37 

"""

from rdflib import Literal
from rdflib.namespace import XSD

__author__ = 'bejar'

# Gene Ontology
mole_func = Literal('molecular_function', datatype=XSD.string)
biol_proc = Literal('biological_process', datatype=XSD.string)
cell_comp = Literal('cellular_component', datatype=XSD.string)

# Human Phenotype
human_phen = Literal('human_phenotype', datatype=XSD.string)
