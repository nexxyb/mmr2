import requests
import environ
import os


env= environ.Env()
# Take environment variables from .env file
environ.Env.read_env()

def get_movies_from_tastedive(name):
    #go to https://tastedive.com/api to get your api key
    #api_key = env('api_key')
    api_key= os.environ.get('api_key')
    parameters= {}
    parameters['q'] = name
    parameters['type'] = 'movie'
    parameters['limit'] = 8
    parameters['info'] =1
    parameters['k'] = api_key
    response = requests.get('https://tastedive.com/api/similar', params= parameters)
    return response.json()

def extract_movie_titles(result_function):
    titles=[]
    title_list= result_function['Similar']['Results']
    for result in title_list:
        titles.append((result['Name'], result['yUrl']))
    if len(titles) > 1:
        return titles
    else:
        return f'No Similar movies'

def get_related_titles(title):
    related_titles = []
    each_title= extract_movie_titles(get_movies_from_tastedive(title))
    if type(each_title) == list:
        for new_title in each_title:
            if new_title[0] not in related_titles:
                related_titles.append(new_title)
        return related_titles  
    else:
        return f'No Similar movies' 

def get_movie_data(movie_title):
    
    parameters= {}
    parameters['t'] = movie_title
    parameters['type'] = 'movie'
    parameters['apikey'] = os.environ.get('api_key2')
    response = requests.get('http://www.omdbapi.com/', params= parameters)
    res =  response.json()
    if res['Response'] == 'True':
        return res
    else:
        return 'N/A'

def get_movie_rating(movie):
    mov_details= get_movie_data(movie)
    if type(mov_details) == dict:
        ratings= mov_details['Ratings']
        if len(ratings) >= 1:
            rating = ratings[0]
            if rating['Source'] == 'Internet Movie Database':
                act_rating= rating['Value']
                if act_rating == '0%' or act_rating == None :
                    actual_rating= 0
                else:
                    actual_rating= float(act_rating[:3])
                    
            else:
                actual_rating= 0       
        else:
            actual_rating= 0
        actors= mov_details['Actors']
        plot= mov_details['Plot']
        year= mov_details['Year']
        movie_details=[year,actual_rating,actors,plot]
        #print(m_url)
        return movie_details

def get_movie(movie_list ):
    recom1= []
    recom2 = []
    l_movie_list= []
    for m in movie_list:
        l_movie_list.append(m.lower())
    recommendations= []
    #final_recommendations= []
    for movie in l_movie_list:
        related_titles = get_related_titles(movie_list) #list of tuples
        if related_titles and type(related_titles) == list:
            #print(related_titles)
            for movie in related_titles:
                #print(movie)
                movie_rating = get_movie_rating(movie[0]) # list
                if movie_rating:
                    recom1.append(movie[0])
                    movie_rating.append(movie[1])
                    recom2.append(movie_rating)
               
           
    r_dict= dict(zip(recom1,recom2))
    recom= {k:v for k,v in sorted(r_dict.items(), key=lambda item: item[1][1], reverse=True)}
    return recom