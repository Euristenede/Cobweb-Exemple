# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 13:52:47 2021

@author: euris
"""
from random import uniform
from random import random

"""
   Dado uma lista de tuplas, retorna um valor aleatório, onde a escolha é 
   proporcional ao peso dividido pela soma de todos os pesos.
   Obs.: Todos os pesos deve ser maior ou igual a Zero.
"""
def escolha_ponderada(lista):
    total = sum(x for y, x in lista)
    z = uniform(0, total)
    result = 0
    for y, x in lista:
        if x < 0:
            raise ValueError('Todos os pesos devem ser maiores ou iguais a 0.')
        if result + x > z:
            return y
        result += x
    raise ValueError("As opções não podem ser uma lista vazia")

"""
   Dado uma lista de tuplas, retorna o valor com maior peso
"""
def escolha_provavel(lista):
    if len(lista) == 0:
        raise ValueError("As opções não podem ser uma lista vazia")

    valores = [x for _, x in lista if x < 0]
    if len(valores) > 0:
        raise ValueError('Todos os pesos devem ser maiores ou iguais a 0')

    lista_atualizada = [(prob, random(), val) for val, prob in lista]
    return sorted(lista_atualizada, reverse=True)[0][2]
