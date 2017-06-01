"""
.. module:: Ontology

Ontology
*************

:Description: Ontology

    Data structure for storing a ontology
    
    First implementation as dictionaries double indexing parents, descendants
    
    Later we can use a graph library

:Authors: bejar
    

:Version: 

:Created on: 18/05/2017 9:26 

"""

import gzip
from collections import deque
from rdflib import Graph, Literal
from rdflib.namespace import XSD, OWL, RDF, RDFS
from pymongo import MongoClient
from HPhenotype.Private.DBConfig import mgdatabase
from HPhenotype.Ontology.Properties import obo_id
from HPhenotype.Data.TermInfo import TermInfo

__author__ = 'bejar'

class BioOntology:
    """
    Class for representing an ontology
    """

    nodesDB = None
    ofile = None
    parent_term = None
    dbase = None
    inmemory = True
    terms_info = None

    def __init__(self, ofile, pterm, dbase=None, inmemory=False, nodesDB=None):
        """
        Creates the empty 
        :param pterm: 
        """
        self.ofile = ofile
        self.parent_term = pterm
        self.dbase = dbase
        self.inmemory = inmemory
        self.terms_info = {}
        self.nodesDB = nodesDB

    def load_from_file(self, labels=True):
        """
        Loads the ontology from a RDF file extracting all the nodes that recursivelly descend from
        the parent term using breadth first traversal
        
        :return: 
        """

        self.inmemory = True
        ontograph = Graph()
        ontofile = gzip.open(self.ofile)
        ontograph.parse(ontofile)

        term_set = set()
        pending = deque()

        pending.append(self.parent_term)
        term_set.add(self.parent_term)
        lterms = []

        term_id = str(self.parent_term).split('/')[-1].replace('_', ':')
        self.terms_info[term_id] = TermInfo(term_id)
        if labels:
            tlabel = [v for v in ontograph.triples((self.parent_term, RDFS.label, None))]
            if tlabel is not None:
                self.terms_info[term_id].label = str(tlabel[0][2])
        while len(pending) != 0:
            term = pending.popleft()
            lterms.append(term)
            candidates = [a for a, _, _ in ontograph.triples((None, RDFS.subClassOf, term))]
            term_id = str(term).split('/')[-1].replace('_', ':')
            for c in candidates:
                desc_id = str(c).split('/')[-1].replace('_', ':')
                self.terms_info[term_id].add_descendant(desc_id)
                if desc_id not in self.terms_info: # Not yet visited
                    if desc_id != term_id: # Not a self arc
                        self.terms_info[desc_id] = TermInfo(term_id)
                        self.terms_info[desc_id].add_ascendant(term_id)
                        if labels:
                            tlabel = [v for v in ontograph.triples((c, RDFS.label, None))]
                            if tlabel is not None:
                                self.terms_info[desc_id].label = str(tlabel[0][2])
                else: # Already visited
                    if not self.terms_info[desc_id].is_ascendant(desc_id): # Not a self arc
                        self.terms_info[desc_id].add_ascendant(term_id)
                if c not in term_set:
                    pending.append(c)
                    term_set.add(c)

    def compute_level(self):
        """
        Computes the depth level of each term in the ontology
        :return: 
        """

        if self.inmemory:
            term_set = set()
            term_set.add(str(self.parent_term).split('/')[-1].replace('_', ':'))

            currlevel = []
            currlevel.append(str(self.parent_term).split('/')[-1].replace('_', ':'))

            nlevel = 0
            while len(currlevel) != 0:
                pending = []
                for term in currlevel:
                    candidates = self.terms_info[term].descendants
                    for c in candidates:
                        if c not in term_set:
                            pending.append(c)
                            term_set.add(c)
                    self.terms_info[term].level = nlevel
                nlevel += 1
                currlevel = pending
        else:
            raise NameError('Ontology not in memory')

    def statistics(self):
        """
        Some statistics about the graph
        :return:
        """
        if self.inmemory:
            nascendants = 0.0
            ndescendants = 0.0
            asccount = 0
            descount = 0
            nleaves = 0
            nannot = 0

            for term in self.terms_info:
                if self.terms_info[term].annotation:
                    nannot += 1
                tmp = len(self.terms_info[term].ascendants)
                if tmp != 0:
                    nascendants += tmp
                    asccount += 1
                tmp = len(self.terms_info[term].descendants)
                if tmp != 0:
                    ndescendants += tmp
                    descount += 1
                else:
                    nleaves += 1
        else:
            raise NameError('Ontology not in memory')

        print 'Nodes = %d' % len(self.terms_info)
        print 'Leaves = %d' % nleaves
        print 'Annotated = %d' % nannot
        print 'Mean ascendants = %3.2f' % (nascendants/asccount)
        print 'Mean descendants = %3.2f' % (ndescendants/descount)

    def save_to_database(self):
        """
        Stores in a database the node information and the links

        :return:
        """
        if self.inmemory:
            client = MongoClient(self.dbase[0])
            db = client[self.dbase[1]]
            col = db[self.nodesDB]
            col.drop()
            for term in self.terms_info:
                col.insert({'node': term, 'level': self.terms_info[term].level,
                            'label': self.terms_info[term].label,
                            'ascendants': self.terms_info[term].ascendants,
                            'descendants': self.terms_info[term].descendants,
                            'annotation': self.terms_info[term].annotation
                            })

    def load_from_database(self):
        """

        :return:
        """
        client = MongoClient(self.dbase[0])
        db = client[self.dbase[1]]
        col = db[self.nodesDB]
        res = col.find({}, {'node':1, 'level':1, 'ascendants': 1, 'descendants': 1, 'label': 1, 'annotation':1})
        self.terms_info = {}

        for r in res:
            tinfo = TermInfo(r['node'])
            tinfo.level = r['level']
            tinfo.ascendants = r['ascendants']
            tinfo.descendants = r['descendants']
            tinfo.label = r['label']
            tinfo.annotation = r['annotation']
            self.terms_info[r['node']] = tinfo
        self.inmemory = True

    def select_level(self, level):
        """
        returns the terms in a level of the ontology
        :param level:
        :return:
        """

        # if self.inmemory:
        #     pass
        # else:
        client = MongoClient(self.dbase[0])
        db = client[self.dbase[1]]
        col = db[self.nodesDB]
        res = col.find({'level': level}, {'node':1})
        lterms = [v['node'] for v in res]

        return lterms

    def recursive_descendants(self, term):
        """
        Returns the list of recursive descendants of a term

        :param term:
        :return:
        """
        def i_recursive_descendants(term):
            lterms = []
            for desc in self.terms_info[term].descendants:
                lterms.extend([desc])
                lterms.extend(self.recursive_descendants(desc))
            return lterms
        return list(set(i_recursive_descendants(term)))



if __name__ == '__main__':

    from HPhenotype.Config import HPHonto, GOonto
    from HPhenotype.Ontology.Classes import pheno_abno_c, biol_proc_c, cell_comp_c, mole_func_c
    onto = BioOntology(HPHonto, pheno_abno_c, dbase=mgdatabase, nodesDB='PhenotypeOnto')

    # onto.load_from_file(labels=True)
    onto.load_from_database()
    onto.statistics()
    # onto.save_to_database()

    # for o in onto.descendants:
    #     print o, onto.descendants[o]

    # for o in onto.ascendants:
    #     print o, onto.ascendants[o]

    # onto.compute_level()
    #
    # llev = sorted([(onto.terms_info[t].level,t) for t in onto.terms_info])
    #
    # for v in llev:
    #     print v
