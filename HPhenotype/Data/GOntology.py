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
from HPhenotype.Data import GOAnnotations
from HPhenotype.Config.Paths import GOann
from HPhenotype.Private.DBConfig import mgdatabase

__author__ = 'bejar'

class GOntology(BioOntology):
    """
    
    """
    def __init__(self, ofile, pterm, dbase=None, inmemory=False, nodesDB=None):
        """
        Creates the empty 
        :param pterm: 
        """
        BioOntology.__init__(self, ofile, pterm, dbase=dbase, inmemory=inmemory, nodesDB=nodesDB)

    def check_annotations(self):
        """
        Checks if the tems in the Phenotype ontology exist in the Phenotype Annotations
        Terms in the onlology have an underscore as separator, annotations use a colon
        :return: 
        """
        goa = GOAnnotations(GOann, dbase=mgdatabase)
        for d in self.terms_info:
            if goa.exists_geneonto(d):
                self.terms_info[d].annotation = True

    def count_genes(self):
        """
        Counts for all the ontology the number of different genes annotated
        :return:
        """
        hpa = GOAnnotations(GOann, dbase=mgdatabase)
        hpa.load_from_database()
        self._i_count_genes(str(self.parent_term).split('/')[-1].replace('_', ':'), hpa)

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
                lgenes.extend(hpa.get_gene_for_geneonto(term))
            return lgenes
        else:
            return []


if __name__ == '__main__':
    from HPhenotype.Config import GOonto
    from HPhenotype.Ontology.Classes import biol_proc_c, cell_comp_c, mole_func_c

    # go = GOntology(GOonto, mole_func_c, dbase=mgdatabase, nodesDB='MoleFuncOnto')
    go = GOntology(GOonto, biol_proc_c, dbase=mgdatabase, nodesDB='BiolProcOnto')
    # go = GOntology(GOonto, cell_comp_c, dbase=mgdatabase, nodesDB='CellCompOnto')
    go.load_from_database()
    # go.compute_level()
    # go.check_annotations()
    # go.count_genes()
    # print go.terms_info[str(go.parent_term).split('/')[-1].replace('_', ':')]

    # go.statistics()
    # go.save_to_database()
    # go.check_annotations()
    l = go.select_level(4)
    for g in l:
        if go.terms_info[g].ngenes>0:
            print g, go.terms_info[g].ngenes, go.terms_info[g].label


