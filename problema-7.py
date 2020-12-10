#
# UFABC - Teoria dos Grafos
# Prof. Maycon Sambinelli
# --------------------------
# Nome: Julio Novais da Fonseca  RA: 21073215
# 
# Problema 7
#
# O problema pode ser transformado num problema de ordenação topológica
# utilizando digrafos. Apesar de nao utilizar o algoritmo de descoberta
# da ordenação topológica a lógica que utilizei foi de inserir os arcos
# ao digrafo de forma que fiquem ordenados, a partir daí uma busca em
# profundidade para capturar todas as dependências de um módulo é suficiente
# para imprirmos as instruções do makefile em ordem correta e recompilarmos
# a solução.
# Meu programa utiliza duas classes auxiliares: GraphHandler, que tem métodos
# de adicionar arcos ao digrafo e iniciar uma DFS no grafo; e Modules, que é
# uma representação em forma de objeto dos módulos do makefile, contendo o
# nome, a lista de suas dependências e suas instruções
#

# Classe auxiliar DigraphHandler que possui os métodos de inserir arco
class DigraphHandler(object):

  # Método construtor do digrafo que apenas guarda os vertices visitados
  def __init__(self):
    self._vis = []

  # Método para inserir um arco ao digrafo recebendo como parâmetro o digrafo
  # e uma tupla com dois valores que representam um arco entre os vértices x,y
  def insert_arc(self, d, arc, w):
    (u,v) = arc

    if u in d:
      d[u].append(Arc(u, v, w))
    elif v is None:
      d[u] = []
    else:
      d[u] = [Arc(u, v, w)]


class Arc(object):

  def __init__(self, x, y, w):
    self.tail = x
    self.head = y
    self.weigth = w


class CustomKey(object):

  def __init__(self, v, w):
    self.vertex = v
    self.weight = w


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
    while i > 1 and self.heap[self.father(i)].weight > self.heap[i].weight:
      j = self.father(i)
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


class Dijkstra(object):

  def __init__(self, d: dict, s):
    self.cost = []
    self.pred = []

    self.queue = CustomHeap();
    for x in d.items():
      self.cost.append(float('inf'))
      self.queue.insert_heap(CustomKey(x, float('inf')))

    self.cost[s] = 0.0
    self.pred[s] = s
    self.queue.change_key(s, 0)

    while len(self.queue.heap) > 0:
      u = self.queue.extract_min()
      if u.weight == float('inf'):
        break
      else:
        for arc in d[u]:
          self._relax(arc)

  def _relax(self, a: Arc):
    u = int(a.tail)
    v = int(a.head)

    if self.cost[v] > self.cost[u] + a.weigth:
      self.cost[v] = self.cost[u] + a.weigth
      self.pred[v] = u
      self.queue.change_key(v, self.cost[v])


if __name__ == "__main__":
  print('oi')