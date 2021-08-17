# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 11:44:12 2021

@author: euris
"""
from random import shuffle
from random import seed
from cobweb import CobwebArvore
from cluster import cluster

from carregar_arquivos import carregar_cogumelos
from carregar_arquivos import carregar_votos_congresso
from carregar_arquivos import carregar_fogo_floresta
"""---------------------------Cogumelos------------------------------------"""
seed(0)
"""Carrega o arquivo json"""
cogumelos = carregar_cogumelos()
"""Embaralha o vetor de características"""
shuffle(cogumelos)

arvoreCogumelo = CobwebArvore()
"""Carrega as instâncias do dataset sem a classe"""
cogumelosSemClasse = [{a: cogumelos[a] for a in cogumelos
                       if a != 'classification'} for cogumelos in cogumelos]

clustersCogumelo = next(cluster(arvoreCogumelo, cogumelosSemClasse))

print(clustersCogumelo)

print("---------------------------------------------------------------------")
"""--------------------------Votos do Congresso----------------------------"""
seed(0)
"""Carrega o arquivo json"""
votosCongresso = carregar_votos_congresso()
"""Embaralha o vetor de características"""
shuffle(votosCongresso)

arvoreVotos = CobwebArvore()
"""Carrega as instâncias do dataset sem a classe"""
votoSemClasse = [{a: votos[a]
                    for a in votos if a != 'Class Name'} for votos in votosCongresso]

clustersVoto = next(cluster(arvoreVotos, votoSemClasse))

print(clustersVoto)
print("---------------------------------------------------------------------")
"""---------------------------Fogo na Floresta-----------------------------"""
seed(0)
"""Carrega o arquivo json"""
fogoFloresta = carregar_fogo_floresta()
"""Embaralha o vetor de características"""
shuffle(fogoFloresta)

arvoreFogo = CobwebArvore()
clustersFogo = next(cluster(arvoreFogo, fogoFloresta))

clust_set = {v: i for i, v in enumerate(list(set(clustersFogo)))}

print(clustersFogo)