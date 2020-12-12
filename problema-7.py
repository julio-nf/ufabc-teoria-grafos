#
# UFABC - Teoria dos Grafos
# Prof. Maycon Sambinelli
# --------------------------
# Nome: Julio Novais da Fonseca  RA: 21073215
# 
# Problema 7
#
# O problema pode ser transformado num problema de encontrar caminhos mínímos
# Utilizei o algoritmo de Dijkstra para encontrar o caminho minímo de u a v
# e imprimir seu custo.
# O algoritmo utiliza as classes auxiliares DigraphHandler, que tem o método
# de inserir arcos; Arc que é a representação de um arco de um digrafo com
# peso; CustomKey para ser utilizdo como chave da Heap; CustomHeap que é uma
# implementação customizada da fila de prioridades (Heap) e finalmente
# a classe Dijkstra que faz o cálculo dos caminhos mínimos e possui os
# métodos auxiliares hasPathTo pra nos dizer se há um caminho entre u e v
# e pathCostTo que retorna o custo do menor caminho de u a v.
# Também foi utilizado a biblioteca padrão decimal, para melhorar a precisão
# dos cálculos já que tive alguns problemas com o cálculo usando float.
#

# Importação do decimal para fazer os cálculos em decimal ao inves de float
from decimal import *

# Classe auxiliar DigraphHandler com o método de inserir arco ao digrafo
class DigraphHandler(object):

  # Método para inserir um arco ao digrafo recebendo como parâmetro o digrafo
  # uma tupla com dois valores que representam um arco entre os vértices x,y
  # e um peso associado ao arco
  def insert_arc(self, d, arc, w):
    (u,v) = arc

    if u in d:
      d[u].append(Arc(u, v, Decimal(w)))
    elif v is None:
      d[u] = []
    else:
      d[u] = [Arc(u, v, Decimal(w))]


# Classe auxiliar Arc que representa um arco de u a v com peso
class Arc(object):

  def __init__(self, x, y, w):
    self.tail = x
    self.head = y
    self.weight: Decimal = w

# Classe auxiliar CustomKey, utilizada como chave para a Heap tem um atributo
# vertex que representa um vertice no digrafo e um atributo weight, utilizado
# para comparação na Heap, representando o menor peso daquele vértice
class CustomKey(object):

  def __init__(self, v, w):
    self.vertex: int = v
    self.weight: Decimal = w


# Classe auxiliar CustomHeap, que é uma implementação customizada de uma fila
# de prioridades (Heap) utilizando o CustomKey como chaves e comparando os
# membros pelo CustomKey.weight
class CustomHeap(object):

  def __init__(self):
    # Deixamos a primeira posição da heap inútil para podermos utilizar
    # a nomenclatura a partir de 1
    self.heap = [CustomKey(-1, -1)]
    self.size = 0

  # Métodos auxziliares para encontrar o pai, e os filhos da esq e dir de um i
  def father(self, i):
    return i//2

  def left_child(self, i):
    return 2*i

  def right_child(self, i):
    return (2*i)+1

  # Método corrige_subindo que vai trocando filhos com os pais sempre que o pai
  # tem chave menor que o filho
  def up_correct(self, i):
    while i//2 > 0:
      j = self.father(i)
      if self.heap[j].weight > self.heap[i].weight:
        aux = self.heap[j]
        self.heap[j] = self.heap[i]
        self.heap[i] = aux
      i = j

  # Método auxiliar para encontar o filho com a menor chave, utilizado pelo
  # corrige_descendo para saber onde descer
  def min_el(self, i):
    l = self.left_child(i)
    r = self.right_child(i)

    if r > self.size:
      return l
    else:
      if self.heap[l].weight < self.heap[r].weight:
        return l
      else:
        return r

  # Método corrige descendo que usa a função de cima para ir descendo trocando
  # os filhos que tem menor chave que o pai
  def down_correct(self, i):
    while self.left_child(i) <= self.size:
      min_child = self.min_el(i)

      if self.heap[i].weight > self.heap[min_child].weight:
        aux = self.heap[i]
        self.heap[i] = self.heap[min_child]
        self.heap[min_child] = aux

      i = min_child

  # Método para diminuir a chave de um dado vértice na heap
  def decrease_key(self, vertex, value):
    i = self.find_index(vertex)
    self.heap[i].weight = value
    self.up_correct(i)

  # Método para achar o índice correspondente de um dado vértice na Heap
  def find_index(self, vertex):
    return next((i for i, item in enumerate(self.heap) if item.vertex == vertex), -1)

  # Método para inserir um elemento na Heap, utilizando o corrige_subindo para
  # manter a propriedade de Heap
  def insert_heap(self, item):
    self.heap.append(item)
    self.size += 1
    self.up_correct(self.size)

  # Método para extrair o menor filho da Heap e diminuir o tamanho dela
  # Utiliza o corrige_descendo para manutenção da propriedade de Heap
  def extract_min(self):
    min = self.heap[1]
    self.heap[1] = self.heap[self.size]
    self.size -= 1
    self.down_correct(1)

    return min


# Classe auxiliar de implementação do algoritmo de Dijkstra
class Dijkstra(object):

  # Atributos auxiliares para o funcionamento do algoritmo
  def __init__(self, d: dict, s):
    self.cost = []
    self.pred = []
    self.vis = []
    self.queue = CustomHeap();

    # Inicializando os atributos iniciais
    for x in d:
      self.cost.append(Decimal('Infinity'))
      self.pred.append(None)
      self.vis.append(False)
      self.queue.insert_heap(CustomKey(x, Decimal('Infinity')))

    # Começando o cálculo de caminhos a partir de s
    self.cost[s] = Decimal('0.0')
    self.pred[s] = s
    self.vis[s] = True
    self.queue.decrease_key(s, Decimal(0.0))

    # Enquanto temos vértices não visitados na fila de prioridades
    while self.queue.size > 0:
      # Visitamos o vértice no topo da Heap
      u = self.queue.extract_min()
      self.vis[u.vertex] = True
      # Com peso infinito não temos caminho até ele e fechamos o algoritmo
      if u.weight == Decimal('Infinity'):
        break
      else:
        # Senão "relaxamos" cada vértice vizinho desse u
        for arc in d[u.vertex]:
          self._relax(arc)

  # Função auxiliar para "relaxar" um arco, atualizando os custos para caso
  # exista um caminho mais barato de u a v
  def _relax(self, a: Arc):
    u = int(a.tail)
    v = int(a.head)

    if self.vis[v] is False:
      if self.cost[v] > self.cost[u] + Decimal(a.weight):
        self.cost[v] = self.cost[u] + Decimal(a.weight)
        self.pred[v] = u
        self.queue.decrease_key(v, self.cost[v])

  # Método auxiliar para verificar se existe um caminho de u a v no grafo
  def hasPathTo(self, v):
    return self.cost[v] < Decimal('Infinity')

  # Método auxiliar para retornar o menor custo de u a v
  def pathCost(self, v):
    return self.cost[v]


if __name__ == "__main__":
  # Pegando o número de pontos do armázem no input
  n_pontos_list = list(range(int(input())))

  # Montando o digrafo com o numero de pontos
  digraph = dict.fromkeys(n_pontos_list)
  graph_handler = DigraphHandler()
  for u in digraph:
    digraph[u] = []

  # Pegando o numero de corredores do armázem no input
  n_corredores = int(input())

  # Para cada input de corredor que recebemos inserimos o arco ao digrafo
  for x in range(n_corredores):
    a, b, c = input().split()
    graph_handler.insert_arc(digraph, (int(a), int(b)), Decimal(c))

  # Pegamos o vertice origem e destino do input
  origem, destino = map(int, input().split())

  # Rodamos o algoritmo de Dijkstra partindo da origem
  dijkstra = Dijkstra(digraph, origem)

  # Se existe caminho até o destino mostramos o custo desse caminho com
  # 4 casas de precisão
  if dijkstra.hasPathTo(destino):
    print('%.4f'%dijkstra.pathCost(destino))
  else:
    # Se não existir o caminho imprimimos ERRO 3.1415 na tela
    print('ERRO: 3.1415')
