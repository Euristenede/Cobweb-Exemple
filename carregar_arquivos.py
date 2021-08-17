# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 17:10:55 2021

@author: euris
"""

"""Carregar os arquivos formatados para o Cobweb"""
from os.path import dirname
from os.path import join
import json

"""Carrega dataset e gera um objeto python"""
def _load_json(filename, num_instances=None):
    module_path = dirname(__file__)
    output = []
    with open(join(module_path, 'arquivos', filename)) as dat:
        for idx, lin in enumerate(dat):
            if num_instances is not None and idx > num_instances:
                break
            output.append(json.loads(lin.strip('[],\n')))
    return output


def carregar_fogo_floresta():
    return _load_json('fogo_floresta.json')

def carregar_votos_congresso():
    return _load_json('votos_congresso.json')

def carregar_cogumelos():
    return _load_json('cogumelos.json')
