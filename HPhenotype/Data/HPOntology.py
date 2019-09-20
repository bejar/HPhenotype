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
from HPhenotype.Data import HPAnnotations
from HPhenotype.Config.Paths import HPann
from HPhenotype.Private.DBConfig import mgdatabase
from HPhenotype.Ontology.Classes import pheno_abno_c

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

    def count_genes(self):
        """
        Counts for all the ontology the number of different genes annotated
        :return:
        """
        if self.inmemory:
            hpa = HPAnnotations(HPann, dbase=mgdatabase)
            hpa.load_from_database()
            self._i_count_genes(str(self.parent_term).split('/')[-1].replace('_', ':'), hpa)
        else:
            raise NameError('Data not in memory')

    def _i_count_genes(self, term, hpa):
        """
        stores recursivelly the counts fro all the different genes from a term of the ontology
        :param term:
        :return:
        """
        if self.terms_info[term].descendants:
            lgenes = []
            for t in self.terms_info[term].descendants:
                lgenes.extend(self._i_count_genes(t, hpa))

            self.terms_info[term].ngenes = len(set(lgenes))

            if self.terms_info[term].annotation:
                lgenes.extend(hpa.get_gene_for_phenotypes(term))
            return lgenes
        else:
            return []




if __name__ == '__main__':
    o = HPOntology(dbase=mgdatabase)
    o.load_from_database()

    # o.count_genes()
    #
    # print o.terms_info[str(o.parent_term).split('/')[-1].replace('_', ':')]

    # lev = o.select_level(4)
    #
    # for t in lev:
    #     print t, len(o.recursive_descendants(t))
    # o.compute_level()
    # o.check_annotations()
    # o.statistics()
    # o.save_to_database()
    l = o.select_level(4)
    for g in l:
        if o.terms_info[g].ngenes>0:
            print g, o.terms_info[g].ngenes, o.terms_info[g].label