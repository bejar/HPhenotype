"""
.. module:: GOAnnotations

GOAnnotations
*************

:Description: GOAnnotations

    

:Authors: bejar
    

:Version: 

:Created on: 16/05/2017 14:26 

"""

__author__ = 'bejar'

class GOAnnotations:
    """
    Class for the genone ontology annotations
    
    Indexes the gene name with the codes in the Gene Ontology
    """
    dfile = None
    GtoGO = None

    def __init__(self, dfile):
        """
        Just initialize the datastructures
        """
        self.GtoGO = {}
        self.dfile = dfile

    def load_data(self):
        """
        Parses the file 
        
        
        :return: 
        """

        afile = open(self.dfile, 'r')

        line = afile.readline()  # skip first line
        while line[0] == '!':
            line = afile.readline()

        while line:
            ann = line.split()
            if ann[2] in self.GtoGO:
                self.GtoGO[ann[2]].append(ann[3])
            else:
                self.GtoGO[ann[2]] = [ann[3]]








if __name__ == '__main__':
    from HPhenotype.Config.Paths import GOann

    goa = GOAnnotations(GOann)

    goa.load_data()
    print len(goa.GtoGO)
