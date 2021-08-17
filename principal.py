# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 11:44:12 2021

@author: euris
"""
from random import shuffle
from random import seed
from cobweb import CobwebArvore
from cluster import cluster
import json
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
dicionario = {}
for i in range(len(clustersCogumelo)):
    dicionario[i] = {'grupo' : clustersCogumelo[i]}    
    
for i in range(len(cogumelos)):
    cogumelos[i].update(dicionario[i])

jsonString = json.dumps(cogumelos)
with open('cogumelos.txt', 'w') as outfile:
    json.dump(cogumelos, outfile)
    
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

dicionario = {}
for i in range(len(clustersVoto)):
    dicionario[i] = {'grupo' : clustersVoto[i]}    
    
for i in range(len(votosCongresso)):
    votosCongresso[i].update(dicionario[i])

jsonString = json.dumps(votosCongresso)
with open('votosCongresso.txt', 'w') as outfile:
    json.dump(votosCongresso, outfile)
print("---------------------------------------------------------------------")
"""---------------------------Fogo na Floresta-----------------------------"""
seed(0)
"""Carrega o arquivo json"""
fogoFloresta = carregar_fogo_floresta()
"""Embaralha o vetor de características"""
shuffle(fogoFloresta)

arvoreFogo = CobwebArvore()
clustersFogo = next(cluster(arvoreFogo, fogoFloresta))

dicionario = {}
for i in range(len(clustersFogo)):
    dicionario[i] = {'grupo' : clustersFogo[i]}    
    
for i in range(len(fogoFloresta)):
    fogoFloresta[i].update(dicionario[i])

jsonString = json.dumps(fogoFloresta)
with open('fogoFloresta.txt', 'w') as outfile:
    json.dump(fogoFloresta, outfile)

