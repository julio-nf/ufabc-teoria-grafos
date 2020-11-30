#
# UFABC - Teoria dos Grafos
# Prof. Maycon Sambinelli
# --------------------------
# Nome: Julio Novais da Fonseca  RA: 21073215
# 
# Problema 5
#
# Meu programa usa uma classe de apoio Graph que recebe uma dict no construtor
# aonde as chaves são os vértices do grafo e os valores das chaves são listas
# que representam as arestas a qual o vértice está conectado.
# Ao iniciar o programa precisamos inserir as entradas n (no de terminais),
# m (no de ferrovias) e [x,y]*m (cada conexão de ferrovia).
# Após receber as entradas usamos o no de terminais como uma lista (range) e
# convertemos essa lista como dict de entrada para a classe Graph, que cria
# uma chave para cada item da lista e uma nova lista vazia para cada valor das
# chaves.
# Com a entrada das ligações das ferrovias usamos o metodo insert_edge para
# inserir as arestas no grafo.
# Um terminal é um possível alvo se sua destruição causa desconexão de pelo
# menos dois terminais e por isso podemos "reduzir" esse problemas ao de
# encontrar vértices de corte.
# Sendo assim chamamos o método search_vertices_corte da classe Graph que
# percorre todas as componentes conexas do grafo usando uma busca DFS
# pelo método _dfs_search_corte e retorna a lista de vértices de corte
# ordenada para o programa.
# Já com a lista apenas imprimimos a quantidade dos vertices de corte e os 
# vertices em si, representando os possíveis terminais alvo.
#

import math
from math import inf

class Graph(object):

  # Método construtor do gráfico que recebe uma dict aonde as keys são os
  # vértices e os values são listas que mostram a quais outros vértices
  # este vértice está ligado
  def __init__(self, g):
    # Dict do grafo, reproduzindo uma lista de adjacências
    self._graph_dict = g
    self._initialize_dict()


  # Inicializa a dict do grafo fazendo cada valor das chaves que seja nulo
  # virar uma lista vazia
  def _initialize_dict(self):
    for u, v in self._graph_dict.items():
      if v is None:
        self._graph_dict[u] = []

    self.add_edges()

  def add_edges(self):
    for u in self._graph_dict:
      for v in self._graph_dict:
        if u == v: pass

        self.insert_edge((u, v))


  # Método para inserir uma aresta recebendo como parâmetro uma tupla com dois
  # valores (x,y) que representam uma aresta entre os vértices x e y
  def insert_edge(self, edge):
    (u, v) = edge

    if u in self._graph_dict:
      self._graph_dict[u].append(v)
      self._graph_dict[v].append(u)
    else:
      self._graph_dict[u] = v
      self._graph_dict[v] = u


  def prim(self):
    queue = CustomHeap()
    conexoes = []

    for v in self._graph_dict:
      queue.insert_heap(CustomKey(float('inf'), v))

    queue.change_key(list(self._graph_dict)[-1], 0)

    while len(queue.heap) > 0:
      u = queue.extract_min()

      for v in self._graph_dict[u.vertex]:
        if queue.check_contains(v) and (w := self.calculate_weigth(u.vertex, v)) < queue.heap[queue.find_index(v)].weight:
          queue.change_key(v, w)
          conexoes.append((u, v))

    print(f'comprimento de cabeamento minimo: {sum(i.weight for i in queue.heap):4f}')

    return conexoes

  def calculate_weigth(self, u, v):
    (ux, uy) = u
    (vx, vy) = v

    return math.sqrt(pow(ux-vx, 2) + pow(uy-vy, 2))


class CustomKey(object):

  def __init__(self, weight, xy):
    self.weight = weight
    self.vertex = xy


class CustomHeap(object):

  def __init__(self):
    self.heap = []

  def father(self, i):
    return i//2

  def left_child(self, i):
    return 2*i

  def right_child(self, i):
    return (2*i)+1

  def up_correct(self, i):
    while i > 1 and self.heap[(j := self.father(i))].weight > self.heap[i].weight:
      aux = self.heap[j]
      self.heap[j] = self.heap[i]
      self.heap[i] = aux

      i = j
  
  def down_correct(self, i):
    l = self.left_child(i)
    r = self.right_child(i)
    min_el = 0

    if l <= len(self.heap) and self.heap[l].weight < self.heap[i].weight:
      min_el = l
    else:
      min_el = i

    if r <= len(self.heap) and self.heap[r].weight < self.heap[min_el].weight:
      min_el = r

    if min_el != i:
      aux = self.heap[i]
      self.heap[i] = self.heap[min_el]
      self.heap[min_el] = aux

      self.down_correct(i)

  def change_key(self, vertex, value):
    i = self.find_index(vertex)

    if value > self.heap[i].weight:
      self.heap[i].weight = value
      self.down_correct(i)
    else:
      self.heap[i].weight = value
      self.up_correct(i)

  def find_index(self, vertex):
    return next((i for i, item in enumerate(self.heap) if item.vertex == vertex), -1)

  def insert_heap(self, item):
    self.heap.append(item)
    self.up_correct(len(self.heap) - 1)

  def extract_min(self):
    min = self.heap[0]
    self.heap[0] = self.heap.pop()
    self.down_correct(0)

    return min

  def check_contains(self, xy):
    return any(x.vertex == xy for x in self.heap)


if __name__ == "__main__":

  # Recebe o inteiro do número de terminais e transforma em uma lista
  # contendo o range do tamanho do int passado
  # ystations = list(range(int(input())))
  # central = ystations.pop()

  ystations = int(input())

  graph_tmp = {}

  for x in range(ystations):
    (x, y) = map(int, input().split())
    graph_tmp[(x, y)] = []

  # Inicia o grafo usando uma dict aonde as chaves vem da lista de terminais
  # do comando anterior, inicialmente com valores vazios em todas as chaves
  graph = Graph(graph_tmp)

  # Para cada ystation/central, recebe a coordenada separada por espaço
  # (u v) e insere a aresta no grafo
  conexoes = graph.prim()

  print(conexoes)
