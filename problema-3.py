class Graph(object):

  # Método construtor do gráfico que recebe uma dict aonde as keys são os
  # vértices e os values são listas que mostram a quais outros vértices
  # este vértice está ligado
  def __init__(self, dict):
    self.__graph_dict = dict

  # Método para inserir uma aresta recebendo como parâmetro uma tupla com dois
  # valores (x,y) que representam uma aresta entre os vértices x e y
  def insert_edge(self, edge):
    (u,v) = edge

    if u in self.__graph_dict:
      self.__graph_dict[u].append(v)
    else:
      self.__graph_dict[u] = v

  def search_v(self, s):
    vis = []
    pred = []

    for x in self.__graph_dict:
      vis.append(False)
      pred.append(None)

    pred[s] = True

    fila = []
    fila.append(s)
    print(fila)

    while len(fila) > 0:
      u = fila.pop()

      for v in self.__graph_dict[u]:
        if vis[v] == False:
          vis[v] = True
          pred[v] = u
          fila.append(v)

    print(f'VIS: {vis}')
    print(f'PRED: {pred}')


if __name__ == "__main__":
  g = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1],
    3: [5, 4],
    4: [3, 6],
    5: [3, 6],
    6: [4, 5],
    7: [],
    8: [9],
    9: [8]
  }

  graph = Graph(g)

  graph.insert_edge((7,8))
  graph.search_v(7)