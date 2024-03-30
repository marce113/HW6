# Your name: Marcela Passos
# Your student id: 32478548
# Your email: marcelap@umich.edu
#Worked with Devyani Jain
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.  
# e.g.: 
# Asked Chatgpt hints for debugging and suggesting the general structure of the code


import requests
import json
import unittest
import os
import re

#TO DO: 
# assign this variable to your API key
# if you are doing the extra credit, assign API_KEY to the return value of your read_api_key function

#EXTRA CREDIT
# def read_api_key(file):
#     '''
#     loads in API key from file 

#     ARGUMENTS:  
#         file: file that contains your API key
    
#     RETURNS:
#         your API key
#     '''
#     hidden_key = ""
#     with open (file, "r") as file:
#         new_list = file.readlines().split("=")
#     #hidden_key = new_list[1]
#     print("!!!",new_list)
#     return hidden_key


def load_json(filename):
    '''
    opens file file, loads content as json object

    ARGUMENTS: 
        filename: name of file to be opened

    RETURNS: 
        json dictionary OR an empty dict if the file could not be opened 
    '''
    try:

        with open(filename, 'r') as f:
            movies = json.loads(f.read())
        return movies
    except:
        print('cannot open json file')
        return {}

def write_json(dict, filename):
    '''
    Encodes dict into JSON format and writes
    the JSON to filename to save the search results

    ARGUMENTS: 
        filename: the name of the file to write a cache to
        dict: cache dictionary

    RETURNS: 
        None
    '''

    #check if dictionary is empty
    try:
        with open(filename, "w") as json_file:
            json.dump(dict, json_file)
             
    except:
        print ("Empty Dictionary")
        return None




def get_movie_data(movie):
    '''
    creates API request
    ARGUMENTS: 
        title: title of the movie you're searching for 

    RETURNS: 
        tuple with the response text and url OR None if the 
        request was unsuccesful
    '''

    base_url = "http://omdbapi.com"
    api_key = "8c1513"
    response = requests.get(base_url, {"apikey": api_key, "t": movie})
    data = response.json()
    if data.get('Response') == 'False':
        return None
    else:
        #print ("!!!!!!",data,response.url)
        return (data,response.url)


    

def cache_all_movies(movies, cache_file):
    '''
    iterates through a list of movies, adds their data to the cache

    ARGUMENTS: 
        movies: a list of movies to get data for 
        cache_file: the file that has cached data 

    RETURNS: 
        A string saying the percentage of movies we succesfully got data for 
    '''
    #create movie_cache as a dict that we can edit
    movie_cache = load_json(cache_file)

    count = 0
    # iterate through all movies and get data from tuples from get_movie_data
    for movie in movies:
        movie_data,url = get_movie_data(movie)
        if url not in movie_cache.items():
            count += 1
            movie_cache[url] = movie_data
         
    
    #save dict to json file
    write_json(movie_cache, cache_file)

    print(count)
    percent_saved = count/len(movies)*100
    #print (f"!!!!!!Cached data for {percent_saved} of movies")
    return f"Cached data for {percent_saved} of movies"
    


def get_highest_box_office_by_year(year, cache_file): 
    '''
    gets the movie with the highest box office total for a given year

    ARGUMENTS: 
        year: the year we want to find the highest grossing film for 
        cache_file: the file that has cached data 

    RETURNS:
        a tuple with the title and box office amount
    '''
    #create movie_dict as a dict that we can edit
    movie_dict = load_json(cache_file)
    highest_box_office = 0
    biggest_movie_title = ""
    first_item = next(iter(movie_dict.items()))
    print("!!!!",first_item)
    for url, movie_data in movie_dict.items():
        movie_box_office = movie_data.get("BoxOffice")
        movie_title = movie_data.get("Title")
        print("!!!", int(movie_data.get("Year")), year)
        if int(movie_data.get("Year")) == year:
            box_office_int = int(movie_box_office.replace("$", "").replace(",",""))
            print("!!!",box_office_int)
            if box_office_int > highest_box_office:
                highest_box_office = box_office_int
                biggest_movie_title = movie_title
        if movie_title == '':
            return "No films found"
        
    return (biggest_movie_title, highest_box_office)

    


def get_genres_above_cutoff(cutoff, cache_file):
    '''
    finds the most common movie genres

    ARGUMENTS: 
        cutoff: the cutoff for how many films a genre must 
                be associated with
        cache_file: the file that has cached data 

    RETURNS:
        a list of tuples with the the genres and counts
    '''
    #create movie_dict as a dict that we can edit
    movie_dict = load_json(cache_file)
    genre_dict = {}
    final_dict = {}
    for url, movie_data in movie_dict.items():
        genre_list = movie_data.get('Genre').split(',')
        for genre in genre_list:
            if genre not in genre_dict:
                genre_dict[genre] = 1
            else:
                genre_dict[genre] += 1
    
    for genre, count in genre_dict.items():
        if count >= cutoff:
            final_dict[genre] = count
    
    return final_dict

       

        



#EXTRA CREDIT
def get_rotten_tomatoes_rating(title, cache_file):
    '''
    gets the rotten tomatoes rating for a given film 

    ARGUMENTS: 
        title: the title of the movie we're searching for 
        cache_file: the file that has cached data 

    RETURNS:
        the rating OR 'No review found'
    '''
    pass


class TestHomework6(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.filename = dir_path + '/' + "cache.json"

        with open('movies.txt', 'r') as f: 
            movies = f.readlines()
            
        for i in range(len(movies)): 
            movies[i] = movies[i].strip()
        self.movies = movies

        # NOTE: if you already have a cache file, setUp will open it
        # otherwise, it will cache all movies to use that in the test cases 
        if not os.path.isfile(self.filename):
            self.cache = cache_all_movies(self.movies, 'cache.json')
        else:
            self.cache = load_json(self.filename)

        self.url = "http://www.omdbapi.com/"


    def test_load_and_write_json(self):
        test_dict = {'test': [1, 2, 3]}
        write_json(test_dict, 'test_cache_load_json.json')

        test_dict_cache = load_json('test_cache_load_json.json')
        self.assertEqual(test_dict_cache, test_dict)
        os.remove('test_cache_load_json.json')

        test_dict_2 = {'test_2': {'test_3': ['a', 'b', 'c']}}
        write_json(test_dict_2, 'test_cache_load_json_2.json')
        
        test_dict_2_cache = load_json('test_cache_load_json_2.json')
        self.assertEqual(test_dict_2_cache, test_dict_2)
        os.remove('test_cache_load_json_2.json')


    def test_get_movie_data(self):
        # testing valid movies
        for movie in ['Mean Girls', 'Pulp Fiction', 'Forrest Gump']:
            movie_data = get_movie_data(movie)
            movie = movie.replace(" ", "+")
            self.assertEqual(type(movie_data[0]), dict)
            self.assertTrue(movie in movie_data[1])

        # testing invalid movie 
        invalid_movie_data = get_movie_data('fake movie 123')
        self.assertEqual(invalid_movie_data, None)


    def test_cache_all_movies(self):
        test_movies = ['Mean Girls', 'Pulp Fiction', 'Forrest Gump']
        test_resp = cache_all_movies(test_movies, 'test_cache_movies.json')
        self.assertTrue(test_resp == "Cached data for 100% of movies" or test_resp == "Cached data for 100.0% of movies")
        test_cache = load_json('test_cache_movies.json')
        self.assertIsInstance(test_cache, dict)
        self.assertEqual(len(list(test_cache.keys())), 3)

        for _, data in test_cache.items():
            if data['Ratings']:
                self.assertEqual(type(data['Ratings']), list)
                self.assertEqual(type(data['Ratings'][0]), dict)

        # checking it won't cache duplicates
        test_resp_2 = cache_all_movies(test_movies, 'test_cache_movies.json')
        self.assertTrue(test_resp_2 == "Cached data for 0% of movies" or test_resp_2 == "Cached data for 0.0% of movies")        
        self.assertEqual(len(list(test_cache.keys())), 3)
        os.remove('test_cache_movies.json')


    def test_get_highest_box_office_per_year(self):
        test_1 = get_highest_box_office_by_year(2005, 'cache.json')
        self.assertEqual(test_1, ("Harry Potter and the Goblet of Fire", 290469928))
        test_2 = get_highest_box_office_by_year(2019, 'cache.json')
        self.assertEqual(test_2, ('Little Women', 108101214))
        test_3 = get_highest_box_office_by_year(2012, 'cache.json')
        self.assertEqual(test_3, ('The Avengers', 623357910))
        test_4 = get_highest_box_office_by_year(1990, 'cache.json')
        self.assertEqual(test_4, 'No films found')


    def test_get_genres_above_cutoff(self):
        test_1 = get_genres_above_cutoff(16, 'cache.json')
        self.assertEqual(len(test_1), 1)

        test_2 = get_genres_above_cutoff(5, 'cache.json') 
        self.assertEqual(len(test_2), 6)
        
        test_3 =  get_genres_above_cutoff(0, 'cache.json')
        self.assertEqual(len(test_3), 17)

        test_4 = get_genres_above_cutoff(1, 'cache.json')
        self.assertEqual(len(test_4), len(test_3))

        self.assertEqual(test_4['Drama'], 16)
        self.assertEqual(test_4['Short'], 1)


    # # UNCOMMENT TO TEST EXTRA CREDIT ### 
    # def read_api_key(self):                     
    #     hidden_key = read_api_key('api_key.txt')
    #     self.assertEqual(API_KEY, hidden_key)
    

    # def test_get_rotten_tomatoes_rating(self):
    #     test_titanic = get_rotten_tomatoes_rating('Titanic', self.filename)
    #     self.assertEqual(test_titanic, '88%')
    #     test_avatar = get_rotten_tomatoes_rating('Avatar', self.filename)
    #     self.assertEqual(test_avatar, '82%')
    #     test_topgun = get_rotten_tomatoes_rating('Top Gun', self.filename)
    #     self.assertEqual(test_topgun, '57%')
    #     test_frozen = get_rotten_tomatoes_rating('Frozen 2', self.cache)
    #     self.assertEqual(test_frozen, 'No review found')

    
def main():
    '''
    Note that your cache file will be called 
    cache.json and will be created in your current directory

    Make sure you are in the directory you want to be work in 
    prior to running
    '''
    #######################################
    # DO NOT CHANGE THIS 
    # this code loads in the list of movies and 
    # removes whitespace for you!
    with open('movies.txt', 'r') as f: 
        movies = f.readlines()
        
    for i in range(len(movies)): 
        movies[i] = movies[i].strip()
    #resp = cache_all_movies(movies, 'cache.json')
        
    # DO NOT CHANGE THIS 
    #######################################



if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
