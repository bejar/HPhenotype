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
        BioOntology.__init__(self, HPHonto, pheno_abno_c, dbase=dbase, inmemory=inmemory)

    def check_annotations(self):
        """
        Checks if the terms in the Phenotype ontology exist in the Phenotype Annotations
        Terms in the onlology have an underscore as separator, annotations use a colon
        :return: 
        """
        hpa = HPAnnotations(HPann, dbase=mgdatabase)
        cpos = 0
        cneg = 0
        for d in self.down:
            if hpa.exists_phenotype(d):
                print '+', d, self.terms_info[d].level
                cpos += 1
            else:
                print '-', d
                cneg += 1
        print cpos, cneg


if __name__ == '__main__':
    o = HPOntology()
    o.load_from_file()
    o.compute_level()
    o.check_annotations()