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
"""----------------------------------------Cogumelos-------------------------------------------------------"""
seed(0)
"""Carrega o arquivo json"""
cogumelos = carregar_cogumelos()
"""Embaralha o vetor de características"""
shuffle(cogumelos)
"""Carrega 150 instâncias do vetor de características"""
cogumelos = cogumelos[:150]

arvoreCogumelo = CobwebArvore()
"""Carrega 150 instâncias do vetor de características sem a classe"""
cogumelosSemClasse = [{a: cogumelos[a] for a in cogumelos
                       if a != 'classification'} for cogumelos in cogumelos]

clustersCogumelo = next(cluster(arvoreCogumelo, cogumelosSemClasse))

cogumelosComClasse = [cogumelos[a] for cogumelos in cogumelos for a in cogumelos
                  if a == 'classification']

clust_set = {v: i for i, v in enumerate(list(set(clustersCogumelo)))}
class_set = {v: i for i, v in enumerate(list(set(cogumelosComClasse)))}

print(clustersCogumelo)
print(clustersCogumelo.count("Conceito52"))
print(clustersCogumelo.count("Conceito1158"))
print(clustersCogumelo.count("Conceito659"))
print("---------------------------------------------------------------------------------")
"""------------------------------------Votos do Congresso--------------------------------------------------"""
seed(0)
"""Carrega o arquivo json"""
votosCongresso = carregar_votos_congresso()
"""Embaralha o vetor de características"""
shuffle(votosCongresso)
"""Carrega 150 instâncias do vetor de características"""
votosCongresso = votosCongresso[:150]

arvoreVotos = CobwebArvore()

votoSemClasse = [{a: votos[a]
                    for a in votos if a != 'Class Name'} for votos in votosCongresso]
clustersVoto = next(cluster(arvoreVotos, votoSemClasse))

votoComClasse = [votos[a] for votos in votosCongresso for a in votos if a == 'class']

clust_set = {v: i for i, v in enumerate(list(set(clustersVoto)))}
class_set = {v: i for i, v in enumerate(list(set(votoComClasse)))}

print(clustersVoto)
print(clustersVoto.count("Conceito10719"))
print(clustersVoto.count("Conceito10733"))
print("---------------------------------------------------------------------------------")
"""------------------------------------Fogo na Floresta---------------------------------------------------"""
seed(0)
"""Carrega o arquivo json"""
fogoFloresta = carregar_fogo_floresta()
"""Embaralha o vetor de características"""
shuffle(fogoFloresta)
"""Carrega 150 instâncias do vetor de características"""
fogoFloresta = fogoFloresta[:150]

arvoreFogo = CobwebArvore()
clustersFogo = next(cluster(arvoreFogo, fogoFloresta))

clust_set = {v: i for i, v in enumerate(list(set(clustersFogo)))}

print(clustersFogo)
print(clustersFogo.count("Conceito32089"))
print(clustersFogo.count("Conceito22130"))
print(clustersFogo.count("Conceito21326"))