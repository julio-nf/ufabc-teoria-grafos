#
# UFABC - Teoria dos Grafos
# Prof. Maycon Sambinelli
# --------------------------
# Nome: Julio Novais da Fonseca  RA: 21073215
# 
#
# Descrição do Programa:
# Meu programa usa uma classe de apoio Graph, que recebe uma dict no construtor
# aonde as chaves são os vértices do grafo e os valores das chaves são listas
# que representam as arestas a qual o vértice está conectado.
# Ao iniciar o programa precisamos inserir as entradas n (no de aeroportos),
# m (no de voos diretos da Pingu) e [x,y]*m (cada voo direto operado).
# Após receber as entradas usamos o no de aeroportos como uma lista (range) e
# convertemos essa lista como dict de entrada para a classe Graph, que cria
# uma chave para cada item da lista e uma nova lista vazia para cada valor das
# chaves.
# Com a entrada dos voos operados usamos o metodo insert_edge para inserir as
# arestas no grafo.
# Após tudo isso começamos a percorrer o grafo duas vezes, fixando um vértice
# e verificando se conseguimos chegar a todos os outros vértices a partir dele
# utilizando o método search_v. Caso não seja possível chegar a algum vertice
# adicionamos essa aresta no grafo para as próximas buscas e aumentamos um
# contador, que representa nossos novos voos diretos, e continuamos o loop.
# Finalizado o loop imprimimos na tela o valor do contador para informarmos
# qual a quantidade novos voos que a Pingu precisa começar a operar para
# atingir seus objetivos.



class Graph(object):

  # Método construtor do gráfico que recebe uma dict aonde as keys são os
  # vértices e os values são listas que mostram a quais outros vértices
  # este vértice está ligado
  def __init__(self, g):
    self.graph_dict = g
    self.initialize_dict()

  # Inicializa a dict do grafo fazendo cada valor das chaves que seja nulo
  # virar uma lista vazia
  def initialize_dict(self):
    for u, v in self.graph_dict.items():
      if v is None:
        self.graph_dict[u] = []

  # Método para inserir uma aresta recebendo como parâmetro uma tupla com dois
  # valores (x,y) que representam uma aresta entre os vértices x e y
  def insert_edge(self, edge):
    (u,v) = edge

    if u in self.graph_dict:
      self.graph_dict[u].append(v)
      self.graph_dict[v].append(u)
    else:
      self.graph_dict[u] = v
      self.graph_dict[v] = u

  # Método de busca por largura usando o mesmo algoritmo mostrado em aula
  # O método recebe como parâmetro um nó inicial e o nó a ser buscado
  # e retorna True caso o nó s seja encontrado e False caso não
  def search_v(self, s, w):
    vis = []
    pred = []

    for x in self.graph_dict:
      vis.append(False)
      pred.append(None)

    pred[s] = True

    fila = []
    fila.append(s)

    while len(fila) > 0:
      u = fila.pop()

      for v in self.graph_dict[u]:
        if v == w:
          return True
        elif vis[v] == False:
          vis[v] = True
          pred[v] = u
          fila.append(v)

    return False



if __name__ == "__main__":

  # Recebe o inteiro do número de aeroportos e transforma em uma lista contendo o range
  # do tamanho do int passado
  n_airports = list(range(int(input())))

  # Inicia o grafo usando uma dict aonde as chaves vem da lista de aeroportos do comando
  # anterior, inicialmente com valores vazios em todas as chaves
  graph = Graph(dict.fromkeys(n_airports))

  # Recebe o número de voos diretos operados pela Pingu
  n_direct_flights = int(input())

  # Para cada voo direto, recebe a entrada dos vertices separado por espaço (u v)
  # e insere a aresta no grafo
  for x in range(n_direct_flights):
    a, b = map(int, input().split())
    graph.insert_edge((a, b))

  # Contador de novos voos diretos que a Pingu precisa começar a operar
  cnt_new_flights = 0

  # Loop para percorrer todos os v do grafo e comparar se conseguimos chegar
  # de todos os v a todos os v, usando o método search_v
  for u in graph.graph_dict:
    for v in range(len(graph.graph_dict)):
      # Ignora se estivermos verificando o mesmo vértice
      if v == u: pass

      # Caso não seja possível chegar em v a partir de u
      elif graph.search_v(u, v) is False:
        # Aumentamos o contador de novos voos diretos e inserimos
        # a aresta de u a v para as próximas buscas
        cnt_new_flights += 1
        graph.insert_edge((u,v))

  # Por fim, imprimimos na tela o contador com a quantidade de novos
  # voos diretos que a Pingu precisa operar para atingir seu objetivo
  print(f'# de novos voos: {cnt_new_flights}')
