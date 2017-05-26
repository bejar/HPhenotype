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

    def __init__(self, name):
        """
        Initialized with the term name
        
        :param name: 
        """
        self.name = name