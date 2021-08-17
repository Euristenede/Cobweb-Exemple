# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 13:55:26 2021

@author: euris
"""
from random import random


class CobwebArvore(object):
    #Método construtor
    def __init__(self):
        self.root = CobwebNo()
        self.root.arvore = self
    #Limpa os nós da arvore
    def clear(self):
        self.root = CobwebNo()
        self.root.arvore = self

    #Verifica se a instância está ok
    def _verifica_instancia(self, instancia):
        for atributo in instancia:
            try:
                hash(atributo)
                atributo[0]
            except Exception:
                raise ValueError('Atributo inválido: '+str(atributo) +
                                 ' do tipo: '+str(type(atributo)) +
                                 ' na instância: '+str(instancia) +
                                 ',\n'+type(self).__name__ +
                                 ' deve ser do tipo hash ou String ')
            try:
                hash(instancia[atributo])
            except Exception:
                raise ValueError('Valor inválido: '+str(instancia[atributo]) +
                                 ' do tipo: '+str(type(instancia[atributo])) +
                                 ' na instância: '+str(instancia) +
                                 ',\n'+type(self).__name__ +
                                 ' só funciona com valores hash.')
            if instancia[atributo] is None:
                raise ValueError("Os atributos não pode ser vazio")
    
    #Verifica se a instância está em uma forma apropriada
    """
       Verifica se a instância está em uma forma apropriada para o Cobweb e faz
       um ajuste incremental em uma nova instância na arvore e retorna como resultado
       um conceito da instância.
       A instância é passado para arvore e o método Cobweb atualiza cada nó para
       inserir a instância na arvore.
    """
    def verifica(self, instancia):
        self._verifica_instancia(instancia)
        return self.cobweb(instancia)
    """
      O cobweb é o principal método da aplicação, é o método responsável por realizar
      os ajustes e categorização das instâncias. Esse método faz uma série de operações
      de classificação para cada instância e maximiza a utilizade da categoria.
    """
    def cobweb(self, instancia):
        current = self.root

        while current:
            # the current.count == 0 here is for the initially empty arvore.
            if not current.filho and (current.e_corresp(instancia) or
                                         current.count == 0):
                # print("leaf match")
                current.incrementar_contagens(instancia)
                break

            elif not current.filho:
                new = current.__class__(current)
                current.pai = new
                new.filho.append(current)

                if new.pai:
                    new.pai.filho.remove(current)
                    new.pai.filho.append(new)
                else:
                    self.root = new

                new.incrementar_contagens(instancia)
                current = new.cria_no_filho(instancia)
                break

            else:
                melhor1_cu, melhor1, melhor2 = current.dois_melhor_filho(instancia)
                _, best_action = current.obter_melhor_operacao(instancia, melhor1,
                                                            melhor2, melhor1_cu)

                # print(best_action)
                if best_action == 'melhor':
                    current.incrementar_contagens(instancia)
                    current = melhor1
                elif best_action == 'novo':
                    current.incrementar_contagens(instancia)
                    current = current.cria_no_filho(instancia)
                    break
                elif best_action == 'somar':
                    current.incrementar_contagens(instancia)
                    novo_filho = current.mesclar(melhor1, melhor2)
                    current = novo_filho
                elif best_action == 'dividir':
                    current.dividir(melhor1)
                else:
                    raise Exception('A melhor opção escolhida "' + best_action +
                                    '" não é uma opção reconhecida, isso não pode acontecer')

        return current

    
"""
   O método abaixo gera os nós na arvore, ou seja um conceito dentro da base de conhecimento
   Cada nó possui uma tabela de probabilidade que pode ser usado para calcular a probabilidade
   de diferentes atributos dado o conceito que o nó representa.
   O método verifica da classe CobwebArvore inicialmente faz uma interface com o método cobweb
   e em seguida o conceito retornado é usado para calcular as probabilidades dos atributos e 
   determinar os rótulos dos conceitos.
   
"""
class CobwebNo(object):
    # Contador para gerar os nomes dos conceitos
    _counter = 0
    
    # O método construtor abaixo cria um nó com valores padrão
    def __init__(self, outroNo=None):
        self.concept_id = self.idConceito()
        self.count = 0.0
        self.av_counts = {}
        self.filho = []
        self.pai = None
        self.arvore = None

        if outroNo:
            self.arvore = outroNo.arvore
            self.pai = outroNo.pai
            self.atualizar_contagem_no(outroNo)

            for child in outroNo.filho:
                self.filho.append(self.__class__(child))
    """
       Cria uma cópia superficial do nó atual, somente o nó sem os seus filhos.
       A cópia desse nó pode ser usado para copiar apenas as informações relevantes
       do nó para a tabela de probabilidade, sem manter referência de outros elementos
       da arvore, exeto para a raiz que é necessário calcular a CU categoria utilitária.
    """
    def copia_inicial(self):
        temp = self.__class__()
        temp.arvore = self.arvore
        temp.pai = self.pai
        temp.atualizar_contagem_no(self)
        return temp
    
    """
       Faz uma interação sobre os atributos do nó aplicando alguns filtros.
       Por padrão o filtro irá ignorar os atributos ocultos e produzir todos os outros.
       Se a string all for informada todos os atributos serão produzidos. Em nenhum caso 
       o filtro retornará verdadeiro ou falso se um atributo deve ser gerado ou não.
    """
    def interar(self, filtro=None):
        if filtro is None:
            return filter(lambda x: x[0] != "_", self.av_counts)
        elif filtro == 'all':
            return self.av_counts
        else:
            return filter(filtro, self.av_counts)


    """
       Incrementa as contagens do nó atual de acordo com a instância especificada.
    """
    def incrementar_contagens(self, instancia):
        self.count += 1
        for attr in instancia:
            if attr not in self.av_counts:
                self.av_counts[attr] = {}
            if instancia[attr] not in self.av_counts[attr]:
                self.av_counts[attr][instancia[attr]] = 0
            self.av_counts[attr][instancia[attr]] += 1

    
    """
       Incrementa as contagens do nó atual de acordo com o nó especificado
    """
    def atualizar_contagem_no(self, node):
        self.count += node.count
        for attr in node.interar('all'):
            if attr not in self.av_counts:
                self.av_counts[attr] = {}
            for val in node.av_counts[attr]:
                if val not in self.av_counts[attr]:
                    self.av_counts[attr][val] = 0
                self.av_counts[attr][val] += node.av_counts[attr][val]


    """
       Retorna o número de suposições corretas que é esperado de um conceito.
       Calcula a soma da probabilidade de cada valor do atributo ao quadrado.
       Utilizado para calcular a utilidade da categoria.
    """
    def suposicoes_corretas_esperadas(self):
        suposicoes_corretas = 0.0
        contador = 0

        for attr in self.interar():
            contador += 1
            if attr in self.av_counts:
                for val in self.av_counts[attr]:
                    prob = (self.av_counts[attr][val]) / self.count
                    suposicoes_corretas += (prob * prob)

        return suposicoes_corretas / contador


    """
       Retorna a utilidade da categoria de uma divisão particular de um determinado
       conceito nos nós filhos.
       A utilidade da categoria é sempre calculada em referencia a um nó pai e seus filhos.
       É usado como heurística para criar um conceito. Inserir a matemática
    """
    def utilidade_categoria(self):
        if len(self.filho) == 0:
            return 0.0

        filho_suposicao_correta = 0.0

        for i in self.filho:
            p_filho = i.count / self.count
            filho_suposicao_correta += (p_filho *
                                      i.suposicoes_corretas_esperadas())

        return ((filho_suposicao_correta - self.suposicoes_corretas_esperadas()) /
                len(self.filho))


    """
       Dado uma instância, os dois melhores filhos com base na utilidade da 
       categoria e um conjunto de operações possíveis, o método abaixo encontra 
       a operação que gera a melor utilidade da categoria e e, seguida retorna 
       a utilidade da categoria e a descrição utilizada para gerar a melhor categoria.
       Em caso de dar empate, um operador é aleatóriamente escolhido.
    """
    def obter_melhor_operacao(self, instancia, melhor1, melhor2, melhor1_cu,
                           opc_posivel=["melhor", "novo", "somar", "dividir"]):
        if not melhor1:
            raise ValueError("Precisa de pelo menos um melhor filho.")

        operacoes = []

        if "melhor" in opc_posivel:
            operacoes.append((melhor1_cu, random(), "melhor"))
        if "novo" in opc_posivel:
            operacoes.append((self.cu_para_novo_filho(instancia), random(),
                               'novo'))
        if "somar" in opc_posivel and len(self.filho) > 2 and melhor2:
            operacoes.append((self.cu_para_mesclar(melhor1, melhor2, instancia),
                               random(), 'somar'))
        if "dividir" in opc_posivel and len(melhor1.filho) > 0:
            operacoes.append((self.cu_for_split(melhor1), random(), 'dividir'))

        operacoes.sort(reverse=True)
        melhor_op = (operacoes[0][0], operacoes[0][2])
        return melhor_op


    """
       Calcula a utilidade da categoria para inserir a instância em cada um dos
       nó filhos e retorna os dois melhores. Em caso de empate os filhos são classificados 
       primeiro pela utilidade da categoria, depois por tamanho e, em seguida,por um valor aleatório.
    """
    def dois_melhor_filho(self, instancia):
        if len(self.filho) == 0:
            raise Exception("Não há fihos.")

        filho_relativo_cu = [(self.calcula_pontuacao_uc(child, instancia),
                                 child.count, random(), child) for child in
                                self.filho]
        filho_relativo_cu.sort(reverse=True)

        # Converte as UCs relativas dos dois melhores nós filhos em pontuação UC
        # que pode ser comparado com as outras operações
        const = self.calcular_valor_constante(instancia)

        melhor1 = filho_relativo_cu[0][3]
        melhor1_relative_cu = filho_relativo_cu[0][0]
        melhor1_cu = (melhor1_relative_cu / (self.count+1) / len(self.filho)
                    + const)

        melhor2 = None
        if len(filho_relativo_cu) > 1:
            melhor2 = filho_relativo_cu[1][3]

        return melhor1_cu, melhor1, melhor2


    """
       Calcula o valor constante que é usado para converter entre CU e
       pontuações CU relativas. O valor constante é basicamente a utilidade da 
       categoria que resulta da adição da instância ao nó raiz.
    """
    def calcular_valor_constante(self, instancia):
        temp = self.copia_inicial()
        temp.incrementar_contagens(instancia)
        ec_root_u = temp.suposicoes_corretas_esperadas()

        const = 0
        for c in self.filho:
            const += ((c.count / (self.count + 1)) *
                      c.suposicoes_corretas_esperadas())

        const -= ec_root_u
        const /= len(self.filho)
        return const


    """
       Mesclar dois nós
    """
    def mesclar(self, melhor1, melhor2):
        novo_filho = self.__class__()
        novo_filho.pai = self
        novo_filho.arvore = self.arvore

        novo_filho.atualizar_contagem_no(melhor1)
        novo_filho.atualizar_contagem_no(melhor2)
        melhor1.pai = novo_filho        
        melhor2.pai = novo_filho
        novo_filho.filho.append(melhor1)
        novo_filho.filho.append(melhor2)
        self.filho.remove(melhor1)
        self.filho.remove(melhor2)
        self.filho.append(novo_filho)

        return novo_filho

    """
       Calcula uma pontuação UC relativa para cada operação de inserção. A UC relativa
       é mais eficiente para calcular uma operação de inserção e garante ter a mesma 
       ordem de classificação que a pontuação da UC para verificar qual operação 
       de inserção é a melhor.
    """
    def calcula_pontuacao_uc(self, child, instancia):
        temp = child.copia_inicial()
        temp.incrementar_contagens(instancia)
        return ((child.count + 1) * temp.suposicoes_corretas_esperadas() -
                child.count * child.suposicoes_corretas_esperadas())

    """
       Cria um novo nó filho para o nó atual com as contagens inicializadas pela
       instância fornecida.
    """
    def cria_no_filho(self, instancia):
        novo_filho = self.__class__()
        novo_filho.pai = self
        novo_filho.arvore = self.arvore
        novo_filho.incrementar_contagens(instancia)
        self.filho.append(novo_filho)
        return novo_filho

    
    """
       Crie um novo nó filho para o nó atual com as contagens inicializadas pela
       contagen do nó atual.
    """
    def criar_filho_countAtual(self):
        if self.count > 0:
            new = self.__class__(self)
            new.pai = self
            new.arvore = self.arvore
            self.filho.append(new)
            return new

    """
       Retorne a utilidade de categoria para criar um novo nó filho utilizando a
       instância fornecida.
    """
    def cu_para_novo_filho(self, instancia):
        temp = self.copia_inicial()
        for c in self.filho:
            temp.filho.append(c.copia_inicial())


        temp.incrementar_contagens(instancia)
        temp.cria_no_filho(instancia)
        return temp.utilidade_categoria()
    
    
    """
       Retorna verdadeiro se um conceito é pai de outro conceito
    """
    def e_pai(self, conceito):
        temp = conceito
        while temp is not None:
            if temp == self:
                return True
            try:
                temp = temp.pai
            except Exception:
                print(temp)
                assert False
        return False
    
    """
       Retorna a utilidade da categoria para mesclar os dois nós.
    """
    def cu_para_mesclar(self, melhor1, melhor2, instancia):
        temp = self.copia_inicial()
        temp.incrementar_contagens(instancia)

        novo_filho = self.__class__()
        novo_filho.arvore = self.arvore
        novo_filho.pai = temp
        novo_filho.atualizar_contagem_no(melhor1)
        novo_filho.atualizar_contagem_no(melhor2)
        novo_filho.incrementar_contagens(instancia)
        temp.filho.append(novo_filho)

        for c in self.filho:
            if c == melhor1 or c == melhor2:
                continue
            temp_child = c.copia_inicial()
            temp.filho.append(temp_child)

        return temp.utilidade_categoria()
    
    
    """
       Dividir um nó em dois nós filhos.
    """
    def dividir(self, best):
        self.filho.remove(best)
        for child in best.filho:
            child.pai = self
            child.arvore = self.arvore
            self.filho.append(child)


    """
       Retorna a utilidade da categoria para dividir o melhor nó filho.
    """
    def cu_for_split(self, best):
        temp = self.copia_inicial()

        for c in self.filho + best.filho:
            if c == best:
                continue
            temp_child = c.copia_inicial()
            temp.filho.append(temp_child)

        return temp.utilidade_categoria()
    
    
    """
       Retorna verdadeiro se o conceito corresponde com a instância informada.
    """
    def e_corresp(self, instancia):
        for attr in set(instancia).union(set(self.interar())):
            if attr[0] == '_':
                continue
            if attr in instancia and attr not in self.av_counts:
                return False
            if attr in self.av_counts and attr not in instancia:
                return False
            if attr in self.av_counts and attr in instancia:
                if instancia[attr] not in self.av_counts[attr]:
                    return False
                if not self.av_counts[attr][instancia[attr]] == self.count:
                    return False
        return True


    """
       Gera um id unico para nomear os conceitos
    """
    def idConceito(self):
        self.__class__._counter += 1
        return self.__class__._counter


