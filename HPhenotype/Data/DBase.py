"""
.. module:: DBase

DBase
*************

:Description: DBase

    Class for database parameters and dataset configuration 

:Authors: bejar
    

:Version: 

:Created on: 19/05/2017 9:57 

"""

__author__ = 'bejar'

class DBase:
    """
    Stores the database info and dataset configuration
    
    """
    dbhost = None # DBmongo host
    dbname = None # DBmongo database
    relations = None # Collections in the DB to store the dataset info

    def __init__(self, dbase, relations):
        """
        
        :param debase: 
        :param relations: 
        """
        self.dbhost = dbase[0]
        self.dbname = dbase[1]
        self.relations = relations