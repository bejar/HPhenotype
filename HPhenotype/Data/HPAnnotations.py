"""
.. module:: Annotations

Annotations
*************

:Description: Annotations

    

:Authors: bejar
    

:Version: 

:Created on: 16/05/2017 14:03 

"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

__author__ = 'bejar'


class HPAnnotations:
    """
    Class for the human Phenotype Annotations
    
    Double dictionary for cross indexing
    
    data can be in memory for fast access or in the database
    """

    GtoP = None
    PtoG = None
    dfile = None
    dbase = None
    inmemory = None

    def __init__(self, dfile, dbase=None, inmemory=False):
        """
        Just initialize the datastructures
        """
        self.GtoP = {}
        self.PtoG = {}
        self.dfile = dfile
        self.dbase = dbase
        self.inmemory = inmemory

    def load_from_file(self):
        """
        Parses the file and generates the double index
        
        for GtoP indexed by gene name, value=[geneid, list of phenotypes]
        for PtoG indexed by pheotype id, value=[phenotype description, list of genes] 
        
        :return: 
        """
        self.inmemory = True
        afile = open(self.dfile, 'r')

        afile.readline()  # skip first line

        for line in afile:
            ann = line.split()

            # print ann

            if ann[1] in self.GtoP:
                self.GtoP[ann[1]][1].append(ann[-1])
            else:
                self.GtoP[ann[1]] = [ann[0], [ann[-1]]]

            if ann[-1] in self.PtoG:
                self.PtoG[ann[-1]][1].append(ann[1])
            else:
                self.PtoG[ann[-1]] = [' '.join(ann[2:-1]), [ann[1]]]

    def save_to_database(self):
        """
        Saves the in memory structures to the database
        :return: 
        """
        if self.inmemory:
            client = MongoClient(self.dbase[0])
            db = client[self.dbase[1]]
            col = db['GenToPhenotype']
            for gen in self.GtoP:
                col.insert({'gene': gen, 'gid': self.GtoP[gen][0], 'phenotype': self.GtoP[gen][1]})

            col = db['PhenotypeToGen']
            for phen in self.PtoG:
                col.insert({'phenotype': phen, 'desc': self.PtoG[phen][0], 'gene': self.PtoG[phen][1]})

    def load_from_database(self):
        """
        Loads the data from the database to memory
        :return: 
        """
        self.inmemory = True
        self.GtoP = {}
        self.PtoG = {}
        client = MongoClient(self.dbase[0])
        db = client[self.dbase[1]]
        col = db['GeneToPhenotype']
        res = col.find({}, {'gene':1, 'gid':1, 'phenotype': 1})

        for r in res:
           self.GtoP[r['gene']] = [r['gid'], r['phenotype']]

        col = db['PhenotypeToGene']
        res = col.find({}, {'gene':1, 'desc':1, 'phenotype': 1})
        for r in res:
           self.PtoG[r['phenotype']] = [r['desc'], r['gene']]


    def get_phenotypes_for_gene(self, gene):
        """
        Retrieves the list of phenotypes associated to a gene
        
        :param gene: 
        :return: 
        """
        if self.inmemory:
            if gene in self.GtoP:
                return self.GtoP[gene]
            else:
                raise Exception('Invalid gene')
        else:
            client = MongoClient(self.dbase[0])
            db = client[self.dbase[1]]
            col = db['GeneToPhenotype']
            res = col.find_one({'gene': gene}, {'phenotype': 1})
            if res is not None:
                return res['phenotype']
            else:
                raise Exception('Invalid gene')

    def get_gene_for_phenotypes(self, phen):
        """
        Retrieves the list of genes associated to a phenotype
        
        :param phen: 
        :return: 
        """
        if self.inmemory:
            if phen in self.PtoG:
                return self.PtoG[phen]
            else:
                raise Exception('Invalid phenotype')
        else:
            client = MongoClient(self.dbase[0])
            db = client[self.dbase[1]]
            col = db['PhenotypeToGene']
            res = col.find_one({'phenotype': phen}, {'gene': 1})
            if res is not None:
                return res['gene']
            else:
                raise Exception('Invalid phenotype')

    def exists_gene(self, gene):
        """
        Returns if a gene is in the datastructure
        
        :param gene: 
        :return: 
        """
        if self.inmemory:
            return gene in self.GtoP
        else:
            client = MongoClient(self.dbase[0])
            db = client[self.dbase[1]]
            col = db['GeneToPhenotype']
            res = col.find_one({'gene': gene}, {'phenotype': 1})
            return res is not None

    def exists_phenotype(self, phen):
        """
        Returns if a phenotype is in the datastructure
        
        :param phen: 
        :return: 
        """
        if self.inmemory:
            return phen in self.PtoG
        else:
            client = MongoClient(self.dbase[0])
            db = client[self.dbase[1]]
            col = db['PhenotypeToGene']
            res = col.find_one({'phenotype': phen}, {'gene': 1})
            return res is not None


if __name__ == '__main__':
    from HPhenotype.Config.Paths import HPann
    from HPhenotype.Private.DBConfig import mgdatabase

    hpa = HPAnnotations(HPann, dbase=mgdatabase)
    # hpa.load_from_file()
    # hpa.save_to_database()
    hpa.load_from_database()
    print len(hpa.GtoP)
    print len(hpa.PtoG)
    print hpa.get_phenotypes_for_gene('CREBBP')
    print hpa.exists_gene('CREBBP')
