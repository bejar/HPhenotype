"""
.. module:: TermInfo

TermInfo
*************

:Description: TermInfo

    

:Authors: bejar
    

:Version: 

:Created on: 25/05/2017 13:57 

"""

__author__ = 'bejar'

class TermInfo:
    """
    Stores the information of an ontology term
    """
    name = None
    level = None
    descendants = None
    ascendants = None
    label = None
    annotation = False
    ngenes = None

    def __init__(self, name):
        """
        Initialized with the term name
        
        :param name: 
        """
        self.name = name
        self.level = 0
        self.ascendants = []
        self.descendants = []
        self.label = ''
        self.ngenes = 0

    def add_ascendant(self, name):
        """
        Adds a name terms to the ascendants list
        :param name:
        :return:
        """
        self.ascendants.append(name)

    def is_ascendant(self, name):
        """
        Checks if it is in the acendants list

        :param name:
        :return:
        """
        return name in self.ascendants

    def add_descendant(self, name):
        """
        Adds a name terms to the ascendants list
        :param name:
        :return:
        """
        self.descendants.append(name)

    def is_descendant(self, name):
        """
        Checks if it is in the ascendants list

        :param name:
        :return:
        """
        return name in self.descendants

    def is_annotated(self):
        """
        Returns if the term is annotated
        :param name:
        :return:
        """
        return self.annotation

    def __str__(self):
        """
        Convers to string the term info

        :return:
        """
        res = ''

        res += 'Name= %s\n' % self.name
        res += 'L= %d\n' % self.level
        res += 'A= %s\n' % str(self.ascendants)
        res += 'D= %s\n' % str(self.descendants)
        res += 'NG= %d\n' % self.ngenes
        return res

