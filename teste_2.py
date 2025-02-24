#Teste 2: Sistema de Recomendação de Filmes
#Crie outro script em Python que receba como entrada apenas um filme e retorne uma recomendação de 5 filmes baseados em critérios definidos.”

import requests
import copy

def recomendarFilmes(movie_id):
  url = "https://api.themoviedb.org/3/movie/{}/recommendations?language=en-US".format(movie_id)
  
  headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YjVkMTNlYmMxNzA1YTIyZTg5ZTcxNjM1NzJlODhjNiIsIm5iZiI6MTc0MDIyOTY0NS42NTIsInN1YiI6IjY3YjljYzBkYTRiZjFjMTkyOGJlYjg2MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.U760IpT1d9wNaGNGX__fEc2-j4hv9CWy-6SAzPimxAA"
  }
  movie=requests.get("https://api.themoviedb.org/3/movie/{}".format(movie_id), headers=headers).json()

  def mySort(e): 
    return e['popularity']
  
  print('Analizando...\n')
  if 'success' in movie and movie['success'] == False:
    print('Filme não encontrado no themoviedb', movie_id, '\n')
  else:

    #Recomendação por genero
    response = requests.get(url, headers=headers).json()
    print('Recomendações por genero:')
    for genre in movie['genres']:
      recommendations=[]
      for res in response['results']:
        for g_id in res['genre_ids']:
          if g_id == genre['id']:
            recommendations.append(res['title'])
      if recommendations != []:
        print('\n', genre['name'])
        for r in recommendations[0:5]:
          print('*', r)
    
    #Recomendação pelos 3 ator ou atrizes mais populares
    movieCastList=requests.get("https://api.themoviedb.org/3/movie/{}/credits?language=en-US".format(movie_id), headers=headers).json()
    movieCastList['cast'].sort(reverse=True, key=mySort)
    castList=copy.deepcopy(movieCastList['cast'][0:3])

    print('\n', 'Recomendações por ator/atriz mais populares:')
    print('(filmes ordenados por popularidade)')

    for cast in castList:
      print('\n', cast['name'])
      recommendations=[]
      response=requests.get("https://api.themoviedb.org/3/person/{}/movie_credits?language=en-US".format(cast['id']), headers=headers).json()
      response['cast'].sort(reverse=True, key=mySort)
      for res in response['cast']:
        if res['id'] != movie_id:
          recommendations.append(res['title'])
      
      if recommendations !=[]:
        for r in recommendations[0:5]:
          print('*', r)
      else:
        print('Não há outras recomendações para esse ator/atriz')

    #Recomendação por diretor/diretora
    for crew in movieCastList['crew']:
      if crew['job'] == 'Director':
        print('\n', 'Recomendações com o mesmo diretor/diretora: ', crew['name'])
        print('(ordenados por popularidade)')
        recommendations=[]
        response=requests.get("https://api.themoviedb.org/3/person/{}/movie_credits?language=en-US".format(crew['id']), headers=headers).json()
        response['crew'].sort(reverse=True, key=mySort)
        
        for res in response['crew']:
          if res['id'] != movie_id:
            if res['job'] == 'Director':
              recommendations.append(res['title'])

        if recommendations !=[]:
          for r in recommendations[0:5]:
            print('*', r)
        else:
          print('Não há outras recomendações para esse diretor/diretora')

#Função que executa o codigo, basta alterar o numero do parametro para obter informação de outro filme.
recomendarFilmes(101)