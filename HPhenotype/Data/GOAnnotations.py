"""
.. module:: GOAnnotations

GOAnnotations
*************

:Description: GOAnnotations

    

:Authors: bejar
    

:Version: 

:Created on: 16/05/2017 14:26 

"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

__author__ = 'bejar'


class GOAnnotations:
    """
    Class for the genone ontology annotations
    
    Indexes the gene name with the codes in the Gene Ontology
    """
    dfile = None
    GenetoGO = None
    GOtoGene = None
    hpheno = False
    inmemory = False

    def __init__(self, dfile, dbase=None, inmemory=False, hpsel=None):
        """
        Just initialize the datastructures
        """
        self.GenetoGO = {}
        self.GOtoGene = {}
        self.dfile = dfile
        self.dbase = dbase
        self.inmemory = inmemory
        self.hpheno = hpsel

    def load_from_file(self):
        """
        Parses the file 
        
        Only selects the genes that are present in hpsel (Human Phenotype Annotations)
        :return: 
        """
        self.inmemory = True
        afile = open(self.dfile, 'r')

        line = afile.readline()  # skip first line
        while line[0] == '!':
            line = afile.readline()

        counte = 0
        while line:
            ann = line.split()
            if self.hpheno and self.hpheno.exists_gene(ann[2]):

                if ann[2] in self.GenetoGO:
                    self.GenetoGO[ann[2]].add(ann[3])
                else:
                    self.GenetoGO[ann[2]] = set()
                    self.GenetoGO[ann[2]].add(ann[3])
                    print(ann[2])
                    counte += 1

                if ann[3] in self.GOtoGene:
                    self.GOtoGene[ann[2]].add(ann[2])
                else:
                    self.GOtoGene[ann[2]] = set()
                    self.GOtoGene[ann[2]].add(ann[2])

            line = afile.readline()

        print counte

    def save_to_database(self):
        """
        Saves the in memory structures to the database
        :return: 
        """

        if self.inmemory:
            client = MongoClient(self.dbase[0])
            db = client[self.dbase[1]]
            col = db['GeneToGO']
            for gen in self.GtoP:
                col.insert({'gene': gen, 'geneonto': [v for v in self.GenetoGO[gen]]})

            col = db['GOToGene']
            for go in self.GtoP:
                col.insert({'geneonto': go, 'gene': [v for v in self.GOtoGene[go]]})







if __name__ == '__main__':
    from HPhenotype.Config.Paths import GOann
    from HPhenotype.Config.Paths import HPann
    from HPhenotype.Private.DBConfig import mgdatabase
    from HPhenotype.Data import HPAnnotations

    hpa = HPAnnotations(HPann, dbase=mgdatabase)

    goa = GOAnnotations(GOann, dbase=mgdatabase, hpsel=hpa)

    goa.load_from_file()
    goa.save_to_database()
    # print len(goa.GtoGO)
