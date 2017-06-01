"""
.. module:: GOAnnotations

GOAnnotations
*************

:Description: GOAnnotations

    Data structure for the Genome annotations

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
    dbase = None

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

        line = afile.readline()  # skip comment lines
        while line[0] == '!':
            line = afile.readline()

        counte = 0
        while line:
            ann = line.split()
            if self.hpheno and self.hpheno.exists_gene(ann[2]):
                if 'GO' in ann[3]:
                    if ann[2] in self.GenetoGO:
                        self.GenetoGO[ann[2]].add(ann[3])
                    else:
                        self.GenetoGO[ann[2]] = set()
                        self.GenetoGO[ann[2]].add(ann[3])
                        # print(ann[2])
                        counte += 1

                    if ann[3] in self.GOtoGene:
                        self.GOtoGene[ann[3]].add(ann[2])
                    else:
                        self.GOtoGene[ann[3]] = set()
                        self.GOtoGene[ann[3]].add(ann[2])

            line = afile.readline()

        print counte

    def load_from_database(self):
        """
        Loads the data from the database to memory
        :return: 
        """
        self.inmemory = True
        self.GenetoGO = {}
        self.GOtoGene = {}
        client = MongoClient(self.dbase[0])
        db = client[self.dbase[1]]
        col = db['GeneToGO']
        res = col.find({}, {'gene':1, 'geneonto': 1})

        for r in res:
           self.GenetoGO[r['gene']] = r['geneonto']

        col = db['GOToGene']
        res = col.find({}, {'geneonto':1, 'desc':1, 'gene': 1})
        for r in res:
           self.GOtoGene[r['geneonto']] = r['gene']


    def save_to_database(self):
        """
        Saves the in memory structures to the database
        :return: 
        """

        if self.inmemory:
            client = MongoClient(self.dbase[0])
            db = client[self.dbase[1]]
            col = db['GeneToGO']
            for gen in self.GenetoGO:
                col.insert({'gene': gen, 'geneonto': [v for v in self.GenetoGO[gen]]})

            col = db['GOToGene']
            for go in self.GOtoGene:
                col.insert({'geneonto': go, 'gene': [v for v in self.GOtoGene[go]]})

    def exists_geneonto(self, gene):
        """
        Returns if a gene is in the datastructure
        
        :param gene: 
        :return: 
        """
        if self.inmemory:
            return gene in self.GenetoGO
        else:
            client = MongoClient(self.dbase[0])
            db = client[self.dbase[1]]
            col = db['GOToGene']
            res = col.find_one({'geneonto': gene}, {'gene': 1})
            return res is not None


    def get_gene_for_geneonto(self, gonto):
        """
        Gets the genes for the geneonto term
        :param gonto:
        :return:
        """
        if self.inmemory:
            if gonto in self.GOtoGene:
                return self.GOtoGene[gonto]
            else:
                raise NameError('No genome %s in gene annotations' % gonto)
        else:
            client = MongoClient(self.dbase[0])
            db = client[self.dbase[1]]
            col = db['GOToGene']
            res = col.find_one({'geneonto': gonto}, {'gene': 1})
            if res is None:
                raise NameError('No genome %s in gene annotations' % gonto)
            else:
                return res['gene']


    def statistics(self):
        """
        Some statistics about the number of arcs
        :return: 
        """
        if self.inmemory:
            nconn = 0
            for g in self.GenetoGO:
                nconn += len(self.GenetoGO[g])
            print 'num links = %d' % nconn
            print 'Gene mean links = %3.2f' % (nconn/float(len(self.GenetoGO)))
            print 'GeneOnto mean links = %3.2f' % (nconn/float(len(self.GOtoGene)))


if __name__ == '__main__':
    from HPhenotype.Config.Paths import GOann
    from HPhenotype.Config.Paths import HPann
    from HPhenotype.Private.DBConfig import mgdatabase
    from HPhenotype.Data import HPAnnotations

    hpa = HPAnnotations(HPann, dbase=mgdatabase)

    goa = GOAnnotations(GOann, dbase=mgdatabase, hpsel=hpa)

    # goa.load_from_database()
    print goa.get_gene_for_geneonto('GO:0035770')
    # goa.statistics()

    # goa.save_to_database()
    # print len(goa.GtoGO)
