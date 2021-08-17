# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 13:51:44 2021

@author: euris
"""

import copy

"""
   O método cluster categoriza uma lista de instâncias em uma arvore e retorna
   uma lista de rotulos agrupados, com base em divisões sucessivas da árvore.
   
   Parametros:
       arvore: Uma árvore de categorias para gerar os clusters;
       instancias: Lista de instâncias a ser agrupada;
       mindiv: Número mínimo de divisões a ser aplicado na árvore;
       maxdiv: Número máximo de divisões a ser aplicado na árvore;
       modificar: Determina se as instâncias serão modificadas ou categorizadas;
"""
def cluster(arvore, instancias, mindiv=1, maxdiv=1, modificar=True):

    for c in agrupamento(arvore, instancias, heuristica=UC, mindiv=mindiv,
                          maxdiv=maxdiv, modificar=modificar, labels=True):
        yield c[0]


"""
   Calcula a utilidade de uma categoria baseado em um estado da arvore
"""
def UC(cluster, folhas):
    raiz_temp = cluster[0].__class__()
    raiz_temp.tree = cluster[0].tree
    for c in set(cluster):
        filho_temp = cluster[0].__class__()
        filho_temp.tree = c.tree
        for folha in folhas:
            if c.e_pai(folha):
                filho_temp.atualizar_contagem_no(folha)
        raiz_temp.atualizar_contagem_no(filho_temp)
        raiz_temp.children.append(filho_temp)
    return -raiz_temp.category_utility()

"""
   Realiza o agrupamento baseado em conceitos
"""
def agrupamento(arvore, instancias, heuristica=UC, mindiv=1, maxdiv=100000,
                 modificar=True, labels=True):

    if mindiv < 1:
        raise ValueError("Mindiv deve ser >= 1")
    if mindiv > maxdiv:
        raise ValueError("Maxdiv deve ser >= Mindiv")
    if len(instancias) == 0:
        raise ValueError("Não é possível agrupar uma lista vazia.")
    if isinstance(heuristica, str):
        if heuristica.upper() == 'UC':
            heuristica = UC
        else:
            raise ValueError('Heuristica informada não é válida: ', heuristica)
    #Cria uma cópia da árvore
    arvore = copy.deepcopy(arvore)

    #Verifica se precisa fazer alguma modificação na instância
    if modificar:
        cluster_temporario = [arvore.verifica(instancia) for instancia in instancias]
    
    for enesima_div in range(1, maxdiv+1):

        atribuir_cluster = []
        atribuir_cluster_filho = []
        if enesima_div >= mindiv:
            clusters = []
            for i, c in enumerate(cluster_temporario):
                child = None
                while (c.parent and c.parent.parent):
                    child = c
                    c = c.parent
                if labels:
                    clusters.append("Conceito" + str(c.concept_id))
                else:
                    clusters.append(c)
                atribuir_cluster.append(c)
                atribuir_cluster_filho.append(child)
            yield clusters, heuristica(atribuir_cluster, cluster_temporario)

        split_cus = []

        for i, alvo in enumerate(set(atribuir_cluster)):
            if len(alvo.children) == 0:
                continue
            c_labels = [label if label != alvo else atribuir_cluster_filho[j]
                        for j, label in enumerate(atribuir_cluster)]
            split_cus.append((heuristica(c_labels, cluster_temporario), i, alvo))

        split_cus = sorted(split_cus)

        if not split_cus:
            break

        arvore.root.split(split_cus[0][2])

        enesima_div += 1
