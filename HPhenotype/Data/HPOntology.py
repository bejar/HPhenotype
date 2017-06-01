"""
.. module:: HPOntology

HPOntology
*************

:Description: HPOntology

    

:Authors: bejar
    

:Version: 

:Created on: 18/05/2017 9:24 

"""

from HPhenotype.Data.BioOntology import BioOntology
from HPhenotype.Config import HPHonto
from HPhenotype.Ontology.Classes import pheno_abno_c
from HPhenotype.Data import HPAnnotations
from HPhenotype.Config.Paths import HPann
from HPhenotype.Private.DBConfig import mgdatabase

from pymongo import MongoClient



__author__ = 'bejar'

class HPOntology(BioOntology):
    """
    
    """
    def __init__(self, dbase=None, inmemory=False):
        """
        Creates the empty 
        :param pterm: 
        """
        BioOntology.__init__(self, HPHonto, pheno_abno_c, dbase=dbase, inmemory=inmemory, nodesDB='PhenotypeOnto')

    def check_annotations(self):
        """
        Checks if the terms in the Phenotype ontology exist in the Phenotype Annotations
        Terms in the onlology have an underscore as separator, annotations use a colon
        :return: 
        """
        hpa = HPAnnotations(HPann, dbase=mgdatabase)
        for d in self.terms_info:
            if hpa.exists_phenotype(d):
                self.terms_info[d].annotation = True



if __name__ == '__main__':
    o = HPOntology(dbase=mgdatabase)
    o.load_from_database()

    lev = o.select_level(4)

    for t in lev:
        print t, len(o.recursive_descendants(t))
    # o.compute_level()
    # o.check_annotations()
    # o.statistics()
    # o.save_to_database()
