"""
.. module:: GOntology

GOntology
*************

:Description: GOntology

    Data structure for the Genome Ontology

:Authors: bejar
    

:Version: 

:Created on: 18/05/2017 9:24 

"""

from HPhenotype.Data.BioOntology import BioOntology

__author__ = 'bejar'

class GOntology(BioOntology):
    """
    
    """
    def __init__(self, ofile, pterm):
        """
        Creates the empty 
        :param pterm: 
        """
        BioOntology.__init__(self, ofile, pterm)

