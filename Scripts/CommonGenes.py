"""
.. module:: CommonGenes

CommonGenes
*************

:Description: CommonGenes

    

:Authors: bejar
    

:Version: 

:Created on: 30/05/2017 15:16 

"""

from HPhenotype.Ontology.Literals import biol_proc, cell_comp, mole_func, human_phen
from HPhenotype.Data import GOntology, HPOntology, GOAnnotations, HPAnnotations
from HPhenotype.Config import GOonto
from HPhenotype.Private.DBConfig import mgdatabase
from HPhenotype.Config.Paths import HPann, GOann, GOonto
from HPhenotype.Ontology.Classes import biol_proc_c, cell_comp_c, mole_func_c

__author__ = 'bejar'

if __name__ == '__main__':
    hpo = HPOntology(dbase=mgdatabase)
    hpo.load_from_database()

    goo = GOntology(GOonto, biol_proc_c, dbase=mgdatabase, nodesDB='BiolProcOnto')
    goo.load_from_database()




