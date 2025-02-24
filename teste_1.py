#Teste 1: Análise de Dados de Filmes
#Crie um script em Python que receba uma lista de filmes e processe os seguintes resultados:

#Participação por Ator: Identifique quantos filmes cada ator participou e exiba o total por ator.
#Frequência de Gêneros: Conte quantas vezes cada gênero aparece na lista e exiba os resultados.
#Top 5 Atores com Maior Bilheteria: Gere uma lista dos 5 atores que somam as maiores bilheterias nos filmes fornecidos.

import requests
import copy

#Define que o criterio usado no sort vai ser pelo name
def mySort(e): 
  return e['name']

#Lista os atores e atrizes que participaram nos filmes da lista, contando em quantos filmes aparecem.
#Recebe como parametros, uma lista de filmes, uma lista inicialmente vazia de atores e o header para acessar a api do themoviedb.
def listarAtores(movieList, actors, header):

  #Caso seja informado apenas um inteiro, é criado uma lista com esse inteiro
  if isinstance(movieList, int):
    movieList=[movieList]

  if isinstance(movieList, (float, str, dict, tuple)):
    print('O tipo usado não esta correto, tente como []')
    exit()
  
  #Faz uma copia da lista de filmes, essa copia é passada para demais funções.
  #Caso haja alteração da lista nesta função, as demais funções não precisam refazer as alterações.
  list=copy.deepcopy(movieList)
  
  print('Analizando...\n')

  for movie in movieList:
    #Testa a lista, caso esteja no padrão themoviedb entra no try, caso seja apenas um array de IDs, entra na except
    try:
      movie_id=movie['id']
    except:
      movie_id=movie

    movieCastList=requests.get("https://api.themoviedb.org/3/movie/{}/credits?language=en-US".format(movie_id), headers=header).json()

    #Caso algum ID não pertença ao themoviedb remove da list.
    if 'success' in movieCastList and movieCastList['success'] == False:
      print('Filme não encontrado no themoviedb, id revomido da lista: ', movie_id, '\n')
      list.remove(movie)
    else:
      movieDetails=requests.get("https://api.themoviedb.org/3/movie/{}".format(movie_id), headers=header).json()
      for cast in movieCastList['cast']:
        if cast['known_for_department'] == "Acting":
          for actor in actors:
            if actor['name'] == cast['name']:
              index=actors.index(actor)
              actors[index]={'name':actor['name'], 'revenue': actor['revenue'] + movieDetails['revenue'], 'count': actor['count'] + 1}
              break
          else:
            actors.append({'name':cast['name'], 'revenue': movieDetails['revenue'] , 'count':1})

  if actors != []:
    actors.sort(key=mySort)
    print('Lista de atores/atrizes que participaram dos filmes da lista \n (pode ser muita longa para aparecer toda no console :) \n')
    for actor in actors:
      print('nome: ', actor['name'] +',', 'participações:', actor['count'],'\n')

  listarGeneros(list, header)
  listarMaioresBilheterias(actors)

#Lista os generos dos filmes da lista, contando quantas vezes aparecem.
#Recebe como parametros, uma lista de filmes e o header para acessar a api do themoviedb.
def listarGeneros(movieList, header):
  typesGenres=requests.get("https://api.themoviedb.org/3/genre/movie/list?language=en", headers=header).json()
  genres=[]

  for movie in movieList:
    if isinstance(movie, dict):
      for genre in movie['genre_ids']:
        for g in genres:
          if genre == g['id']:
            index=genres.index(g)
            genres[index]={'id': genre,'name': g['name'], 'count': g['count'] + 1}
            break
        else:
          for type in typesGenres['genres']:
            if type['id'] == genre:
              genres.append({'id': genre, 'name': type['name'], 'count': 1})
    else:
      movie=requests.get("https://api.themoviedb.org/3/movie/{}".format(movie), headers=header).json()
      for genre in movie['genres']:
        for g in genres:
          if genre == g['id']:
            index=genres.index(g)
            genres[index]={'id': genre,'name': g['name'], 'count': g['count'] + 1}
            break
        else:
          for type in typesGenres['genres']:
            if type['id'] == genre['id']:
              genres.append({'id': genre, 'name': type['name'], 'count': 1})

  if genres != []:
    genres.sort(key=mySort)
    print('Lista de generos presente na lista de filmes:')
    for genre in genres:
      print('nome: ', genre['name'] +',', 'count: ', genre['count'] ,'\n')

#Lista os 5 atores ou atrizes com maior bilheteria.
#Recebe como parametro uma lista de atores preenchida pela função listarAtores.
def listarMaioresBilheterias(actors):
  #Define que o criterio usado no sort vai ser pelo revenue
  def mySort(e): 
    return e['revenue']
  
  if actors != []:
    actors.sort(reverse = True, key=mySort)
    print('Lista dos atores/atrizes com maior bilheteria da lista de filmes:')
    for actor in actors[0:5]:
      print('Nome: ', actor['name'] + ',', 'Bilheteria: ', actor['revenue'])

#Função principal, executa as demais funções
def executarTeste():
  movieListUrl = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"

  headers = {
  "accept": "application/json",
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YjVkMTNlYmMxNzA1YTIyZTg5ZTcxNjM1NzJlODhjNiIsIm5iZiI6MTc0MDIyOTY0NS42NTIsInN1YiI6IjY3YjljYzBkYTRiZjFjMTkyOGJlYjg2MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.U760IpT1d9wNaGNGX__fEc2-j4hv9CWy-6SAzPimxAA"
  }

  actorsList=[]
  response = requests.get(movieListUrl, headers=headers).json()

  #Recebe um array de objetos contendo informações de filmes, conforme o padrão usado no themoviedb
  movieListResponse = response['results']
  
  if movieListResponse == []:
    print('Lista de filmes vazia')
  else:
    listarAtores(movieListResponse, actorsList, headers)
    
executarTeste()
