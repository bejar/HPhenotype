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

if __name__ == '__main__':
    from HPhenotype.Config import GOonto
    from HPhenotype.Ontology.Classes import biol_proc_c, cell_comp_c, mole_func_c

    go = GOntology(GOonto, mole_func_c, dbase=mgdatabase, nodesDB='MoleFuncOnto')
    #go = GOntology(GOonto, biol_proc_c, dbase=mgdatabase, nodesDB='BiolProcOnto')
    #go = GOntology(GOonto, cell_comp_c, dbase=mgdatabase, nodesDB='CellCompOnto')
    go.load_from_file()
    go.compute_level()
    go.check_annotations()
    go.statistics()
    go.save_to_database()
    # go.check_annotations()


