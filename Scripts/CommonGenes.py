"""
.. module:: CommonGenes

CommonGenes
*************

:Description: CommonGenes

    

:Authors: bejar
    

:Version: 

:Created on: 30/05/2017 15:16 

"""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.manifold import MDS, Isomap, TSNE, SpectralEmbedding
from scipy.spatial.distance import cdist, pdist

from HPhenotype.Data import GOntology, HPOntology, GOAnnotations, HPAnnotations
from HPhenotype.Config.Paths import HPann, GOann, GOonto
from HPhenotype.Ontology.Classes import biol_proc_c, cell_comp_c, mole_func_c
from HPhenotype.Private.DBConfig import mgdatabase

__author__ = 'bejar'

if __name__ == '__main__':

    levelph = 4
    levelgn = 1
    ngene_threshold = 25

    # ---- Phenotype
    hpo = HPOntology(dbase=mgdatabase)
    hpo.load_from_database()
    hpa = HPAnnotations(HPann, dbase=mgdatabase)

    pheno_level = hpo.select_level(levelph)

    dpheno = {}
    for ph in pheno_level:
        dpheno[ph] = hpo.recursive_descendants(ph)

    gpheno = {}
    for ph in pheno_level:
        if hpo.terms_info[ph].is_annotated():
            gpheno[ph] = hpa.get_gene_for_phenotypes(ph)
        else:
            gpheno[ph] = []

        for dph in dpheno[ph]:
            if hpo.terms_info[dph].is_annotated():
                gpheno[ph].extend(hpa.get_gene_for_phenotypes(dph))

        gpheno[ph] = set(gpheno[ph])

    # for ph in pheno_level:
    #     print ph, hpo.terms_info[ph].label, len(gpheno[ph])
    for ph in pheno_level:
        if len(gpheno[ph]) < ngene_threshold:
            del gpheno[ph]

    print 'Phenotype gene annotated %d' % len(gpheno)

    # -- Genotype
    # goo = GOntology(GOonto, mole_func_c, dbase=mgdatabase, nodesDB='MoleFuncOnto')
    # goo = GOntology(GOonto, cell_comp_c, dbase=mgdatabase, nodesDB='CellCompOnto')
    goo = GOntology(GOonto, biol_proc_c, dbase=mgdatabase, nodesDB='BiolProcOnto')
    goo.load_from_database()

    goa = GOAnnotations(GOann, dbase=mgdatabase)

    geno_level = goo.select_level(levelgn)

    dgeno = {}
    for gn in geno_level:
        dgeno[gn] = goo.recursive_descendants(gn)

    ggeno = {}
    for gn in geno_level:
        if goo.terms_info[gn].is_annotated():
            ggeno[gn] = goa.get_gene_for_geneonto(gn)
        else:
            ggeno[gn] = []
        for dgn in dgeno[gn]:
            if goo.terms_info[dgn].is_annotated():
                ggeno[gn].extend(goa.get_gene_for_geneonto(dgn))

        ggeno[gn] = set(ggeno[gn])

    # for gn in geno_level:
    #     print gn, goo.terms_info[gn].label, len(ggeno[gn])

    for gn in geno_level:
        if len(ggeno[gn]) < ngene_threshold:
            del ggeno[gn]
    print 'Genotype gene annotated %d' % len(ggeno)

    ann_dmatrix = np.zeros((len(gpheno), len(ggeno)))

    sim_threshold = 0.5

    count_thresh = 0
    for i, ph in enumerate(gpheno):
        for j, gn in enumerate(ggeno):
            ann_dmatrix[i, j] = float(len(gpheno[ph].intersection(ggeno[gn]))) / float(len(gpheno[ph].union(ggeno[gn])))
            if ann_dmatrix[i, j] > sim_threshold:
                count_thresh += 1

    # print '%d Over threshold %3.2f' % (count_thresh, sim_threshold)
    # ax = sns.heatmap(ann_dmatrix)
    plt.show()

    count_thresh = 0
    ph_dmatrix = np.zeros((len(gpheno), len(gpheno)))
    for i, ph1 in enumerate(gpheno):
        for j, ph2 in enumerate(gpheno):
            ph_dmatrix[i, j] = float(len(gpheno[ph1].intersection(gpheno[ph2]))) / float(
                len(gpheno[ph1].union(gpheno[ph2])))
            if ph_dmatrix[i, j] > sim_threshold and i != j:
                count_thresh += 1
    print '%d Over threshold %3.2f' % (count_thresh, sim_threshold)
    # ax = sns.heatmap(ph_dmatrix)
    # plt.show()

    count_thresh = 0
    gn_dmatrix = np.zeros((len(ggeno), len(ggeno)))
    for i, gn1 in enumerate(ggeno):
        for j, gn2 in enumerate(ggeno):
            gn_dmatrix[i, j] = float(len(ggeno[gn1].intersection(ggeno[gn2]))) / float(
                len(ggeno[gn1].union(ggeno[gn2])))
            if gn_dmatrix[i, j] > sim_threshold and i != j:
                count_thresh += 1

    print '%d Over threshold %3.2f' % (count_thresh, sim_threshold)
    # ax = sns.heatmap(gn_dmatrix)
    # plt.show()

    # print ph_dmatrix.shape, ann_dmatrix.shape, gn_dmatrix.shape

    m1 = np.concatenate((ph_dmatrix, ann_dmatrix), axis=1)
    m2 = np.concatenate((ann_dmatrix.T, gn_dmatrix), axis=1)
    mdist = np.concatenate((m1, m2), axis=0)

    # ax = sns.heatmap(mdist)
    # plt.show()

    # fdata = 1 -mdist
    # imap = MDS(n_components=3, dissimilarity='precomputed')

    fdata = mdist
    imap = SpectralEmbedding(n_components=3, affinity='precomputed')

    fdata = imap.fit_transform(fdata)

    # color = ['r'] * len(gpheno) + ['b'] * len(ggeno)
    #
    # fig = plt.figure(figsize=(10, 10))
    # ax = fig.add_subplot(111, projection='3d')
    # plt.scatter(fdata[:, 0], fdata[:, 1], zs=fdata[:, 2], depthshade=False, s=100, c=color, cmap=plt.get_cmap('jet') )
    # plt.show()

    offset = len(gpheno)

    nmdist = cdist(fdata[0:offset], fdata[offset:])
    md = np.min(mdist)
    print 'Min distance %f' % md

    lgeno = ggeno.keys()
    for i, ph in enumerate(gpheno):
        j = np.argmin(nmdist[i])
        # if nmdist[i,j] < (md *2):
        print nmdist[i, j], hpo.terms_info[ph].label, '->', goo.terms_info[lgeno[j]].label