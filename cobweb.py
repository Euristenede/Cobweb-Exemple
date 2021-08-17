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
        self.root.tree = self
    #Limpa os nós da arvore
    def clear(self):
        self.root = CobwebNo()
        self.root.tree = self

    def __str__(self):
        return str(self.root)

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
            # the current.count == 0 here is for the initially empty tree.
            if not current.children and (current.is_exact_match(instancia) or
                                         current.count == 0):
                # print("leaf match")
                current.increment_counts(instancia)
                break

            elif not current.children:
                # print("fringe split")
                new = current.__class__(current)
                current.parent = new
                new.children.append(current)

                if new.parent:
                    new.parent.children.remove(current)
                    new.parent.children.append(new)
                else:
                    self.root = new

                new.increment_counts(instancia)
                current = new.create_new_child(instancia)
                break

            else:
                best1_cu, best1, best2 = current.two_best_children(instancia)
                _, best_action = current.get_best_operation(instancia, best1,
                                                            best2, best1_cu)

                # print(best_action)
                if best_action == 'melhor':
                    current.increment_counts(instancia)
                    current = best1
                elif best_action == 'novo':
                    current.increment_counts(instancia)
                    current = current.create_new_child(instancia)
                    break
                elif best_action == 'somar':
                    current.increment_counts(instancia)
                    new_child = current.merge(best1, best2)
                    current = new_child
                elif best_action == 'dividir':
                    current.split(best1)
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
    def __init__(self, otherNode=None):
        self.concept_id = self.gensym()
        self.count = 0.0
        self.av_counts = {}
        self.children = []
        self.parent = None
        self.tree = None

        if otherNode:
            self.tree = otherNode.tree
            self.parent = otherNode.parent
            self.atualizar_contagem_no(otherNode)

            for child in otherNode.children:
                self.children.append(self.__class__(child))
    """
       Cria uma cópia superficial do nó atual, somente o nó sem os seus filhos.
       A cópia desse nó pode ser usado para copiar apenas as informações relevantes
       do nó para a tabela de probabilidade, sem manter referência de outros elementos
       da arvore, exeto para a raiz que é necessário calcular a CU categoria utilitária.
    """
    def copia_inicial(self):
        temp = self.__class__()
        temp.tree = self.tree
        temp.parent = self.parent
        temp.atualizar_contagem_no(self)
        return temp
    
    """
       Faz uma interação sobre os atributos do nó aplicando alguns filtros.
       Por padrão o filtro irá ignorar os atributos ocultos e produzir todos os outros.
       Se a string all for informada todos os atributos serão produzidos. Em nenhum caso 
       o filtro retornará verdadeiro ou falso se um atributo deve ser gerado ou não.
    """
    def attrs(self, attr_filter=None):
        if attr_filter is None:
            return filter(lambda x: x[0] != "_", self.av_counts)
        elif attr_filter == 'all':
            return self.av_counts
        else:
            return filter(attr_filter, self.av_counts)


    """
       Incrementa as contagens do nó atual de acordo com a instância especificada.
    """
    def increment_counts(self, instance):
        self.count += 1
        for attr in instance:
            if attr not in self.av_counts:
                self.av_counts[attr] = {}
            if instance[attr] not in self.av_counts[attr]:
                self.av_counts[attr][instance[attr]] = 0
            self.av_counts[attr][instance[attr]] += 1

    
    """
       Incrementa as contagens do nó atual de acordo com o nó especificado
    """
    def atualizar_contagem_no(self, node):
        self.count += node.count
        for attr in node.attrs('all'):
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
    def expected_correct_guesses(self):
        correct_guesses = 0.0
        attr_count = 0

        for attr in self.attrs():
            attr_count += 1
            if attr in self.av_counts:
                for val in self.av_counts[attr]:
                    prob = (self.av_counts[attr][val]) / self.count
                    correct_guesses += (prob * prob)

        return correct_guesses / attr_count


    """
       Retorna a utilidade da categoria de uma divisão particular de um determinado
       conceito nos nós filhos.
       A utilidade da categoria é sempre calculada em referencia a um nó pai e seus filhos.
       É usado como heurística para criar um conceito. Inserir a matemática
    """
    def category_utility(self):
        if len(self.children) == 0:
            return 0.0

        child_correct_guesses = 0.0

        for child in self.children:
            p_of_child = child.count / self.count
            child_correct_guesses += (p_of_child *
                                      child.expected_correct_guesses())

        return ((child_correct_guesses - self.expected_correct_guesses()) /
                len(self.children))


    """
       Dado uma instância, os dois melhores filhos com base na utilidade da 
       categoria e um conjunto de operações possíveis, o método abaixo encontra 
       a operação que gera a melor utilidade da categoria e e, seguida retorna 
       a utilidade da categoria e a descrição utilizada para gerar a melhor categoria.
       Em caso de dar empate, um operador é aleatóriamente escolhido.
    """
    def get_best_operation(self, instance, best1, best2, best1_cu,
                           possible_ops=["melhor", "novo", "somar", "dividir"]):
        if not best1:
            raise ValueError("Precisa de pelo menos um melhor filho.")

        operations = []

        if "melhor" in possible_ops:
            operations.append((best1_cu, random(), "melhor"))
        if "novo" in possible_ops:
            operations.append((self.cu_for_new_child(instance), random(),
                               'novo'))
        if "somar" in possible_ops and len(self.children) > 2 and best2:
            operations.append((self.cu_for_merge(best1, best2, instance),
                               random(), 'somar'))
        if "dividir" in possible_ops and len(best1.children) > 0:
            operations.append((self.cu_for_split(best1), random(), 'dividir'))

        operations.sort(reverse=True)
        # print(operations)
        best_op = (operations[0][0], operations[0][2])
        # print(best_op)
        return best_op


    """
       Calcula a utilidade da categoria para inserir a instância em cada um dos
       nó filhos e retorna os dois melhores. Em caso de empate os filhos são classificados 
       primeiro pela utilidade da categoria, depois por tamanho e, em seguida,por um valor aleatório.
    """
    def two_best_children(self, instance):
        if len(self.children) == 0:
            raise Exception("Não há fihos.")

        children_relative_cu = [(self.relative_cu_for_insert(child, instance),
                                 child.count, random(), child) for child in
                                self.children]
        children_relative_cu.sort(reverse=True)

        # Converte as UCs relativas dos dois melhores nós filhos em pontuação UC
        # que pode ser comparado com as outras operações
        const = self.compute_relative_CU_const(instance)

        best1 = children_relative_cu[0][3]
        best1_relative_cu = children_relative_cu[0][0]
        best1_cu = (best1_relative_cu / (self.count+1) / len(self.children)
                    + const)

        best2 = None
        if len(children_relative_cu) > 1:
            best2 = children_relative_cu[1][3]

        return best1_cu, best1, best2


    """
       Calcula o valor constante que é usado para converter entre CU e
       pontuações CU relativas. O valor constante é basicamente a utilidade da 
       categoria que resulta da adição da instância ao nó raiz.
    """
    def compute_relative_CU_const(self, instance):
        temp = self.copia_inicial()
        temp.increment_counts(instance)
        ec_root_u = temp.expected_correct_guesses()

        const = 0
        for c in self.children:
            const += ((c.count / (self.count + 1)) *
                      c.expected_correct_guesses())

        const -= ec_root_u
        const /= len(self.children)
        return const


    """
       Calcula uma pontuação UC relativa para cada operação de inserção. A UC relativa
       é mais eficiente para calcular uma operação de inserção e garante ter a mesma 
       ordem de classificação que a pontuação da UC para verificar qual operação 
       de inserção é a melhor.
    """
    def relative_cu_for_insert(self, child, instance):
        temp = child.copia_inicial()
        temp.increment_counts(instance)
        return ((child.count + 1) * temp.expected_correct_guesses() -
                child.count * child.expected_correct_guesses())
    
    
    """
       Calcule a utilidade da categoria para adicionar a instância a um nó filho especificado.
    """
    def cu_for_insert(self, child, instance):
        temp = self.copia_inicial()
        temp.increment_counts(instance)

        for c in self.children:
            temp_child = c.copia_inicial()
            temp.children.append(temp_child)
            temp_child.parent = temp
            if c == child:
                temp_child.increment_counts(instance)
        return temp.category_utility()


    """
       Cria um novo nó filho para o nó atual com as contagens inicializadas pela
       instância fornecida.
    """
    def create_new_child(self, instance):
        new_child = self.__class__()
        new_child.parent = self
        new_child.tree = self.tree
        new_child.increment_counts(instance)
        self.children.append(new_child)
        return new_child

    
    """
       Crie um novo nó filho para o nó atual com as contagens inicializadas pela
       contagen do nó atual.
    """
    def create_child_with_current_counts(self):
        if self.count > 0:
            new = self.__class__(self)
            new.parent = self
            new.tree = self.tree
            self.children.append(new)
            return new

    """
       Retorne a utilidade de categoria para criar um novo nó filho utilizando a
       instância fornecida.
    """
    def cu_for_new_child(self, instance):
        temp = self.copia_inicial()
        for c in self.children:
            temp.children.append(c.copia_inicial())


        temp.increment_counts(instance)
        temp.create_new_child(instance)
        return temp.category_utility()
    
    
    """
       Mesclar dois nós
    """
    def merge(self, best1, best2):
        new_child = self.__class__()
        new_child.parent = self
        new_child.tree = self.tree

        new_child.atualizar_contagem_no(best1)
        new_child.atualizar_contagem_no(best2)
        best1.parent = new_child        
        best2.parent = new_child
        new_child.children.append(best1)
        new_child.children.append(best2)
        self.children.remove(best1)
        self.children.remove(best2)
        self.children.append(new_child)

        return new_child
    
    
    """
       Retorna a utilidade da categoria para mesclar os dois nós.
    """
    def cu_for_merge(self, best1, best2, instance):
        temp = self.copia_inicial()
        temp.increment_counts(instance)

        new_child = self.__class__()
        new_child.tree = self.tree
        new_child.parent = temp
        new_child.atualizar_contagem_no(best1)
        new_child.atualizar_contagem_no(best2)
        new_child.increment_counts(instance)
        temp.children.append(new_child)

        for c in self.children:
            if c == best1 or c == best2:
                continue
            temp_child = c.copia_inicial()
            temp.children.append(temp_child)

        return temp.category_utility()
    
    
    """
       Dividir um nó em dois nós filhos.
    """
    def split(self, best):
        self.children.remove(best)
        for child in best.children:
            child.parent = self
            child.tree = self.tree
            self.children.append(child)

    
    """
       Retorna a utilidade da categoria para realizar uma divisão de franja, 
       adicionar um nó folha a um outro nó folha.
    """
    def cu_for_fringe_split(self, instance):
        temp = self.copia_inicial()

        temp.create_child_with_current_counts()
        temp.increment_counts(instance)
        temp.create_new_child(instance)

        return temp.category_utility()


    """
       Retorna a utilidade da categoria para dividir o melhor nó filho.
    """
    def cu_for_split(self, best):
        temp = self.copia_inicial()

        for c in self.children + best.children:
            if c == best:
                continue
            temp_child = c.copia_inicial()
            temp.children.append(temp_child)

        return temp.category_utility()
    
    
    """
       Retorna verdadeiro se o conceito corresponde com a instância informada.
    """
    def is_exact_match(self, instance):
        for attr in set(instance).union(set(self.attrs())):
            if attr[0] == '_':
                continue
            if attr in instance and attr not in self.av_counts:
                return False
            if attr in self.av_counts and attr not in instance:
                return False
            if attr in self.av_counts and attr in instance:
                if instance[attr] not in self.av_counts[attr]:
                    return False
                if not self.av_counts[attr][instance[attr]] == self.count:
                    return False
        return True


    """
       Gera um id unico para nomear os conceitos
    """
    def gensym(self):
        self.__class__._counter += 1
        return self.__class__._counter
    
    
    """
       Chama o método imprime_arvore
    """
    def __str__(self):
        return self.imprime_arvore()

    
    """
       Imprime a arvore de categorias
    """
    def imprime_arvore(self, depth=0):

        ret = str(('\t' * depth) + "|-" + str(self.av_counts) + ":" +
                  str(self.count) + '\n')

        for c in self.children:
            ret += c.imprime_arvore(depth+1)

        return ret


    """
       Retorna verdadeiro se um conceito é pai de outro conceito
    """
    def e_pai(self, other_concept):
        temp = other_concept
        while temp is not None:
            if temp == self:
                return True
            try:
                temp = temp.parent
            except Exception:
                print(temp)
                assert False
        return False

