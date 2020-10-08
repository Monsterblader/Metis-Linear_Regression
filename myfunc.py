# Prepares movie data.
import re
import pandas as pd
from bs4 import BeautifulSoup


def make_movie_set():

    def CountFrequency(my_list):
        freq = {}

        for item in my_list:
            if (item in freq):
                freq[item] += 1
            else:
                freq[item] = 1

        return freq

    all_movies = pd.read_csv('data/cleaned_data.csv')

    # Filters distributors who have released more than 80 movies over the data set.
    distributor_count = CountFrequency(all_movies['Distributor'])

    # Manually select studios to reduce the number of featurs.
    # dists = list({k: v for (k, v) in distributor_count.items() if (v > 80) and (k != '-')})
    dists = ['Walt Disney Studios Motion Pictures', 'Universal Pictures', 'Twentieth Century Fox',
             'Sony Pictures Entertainment (SPE)', 'Paramount Pictures', 'Warner Bros.']
    ratings = ['PG', 'PG-13', 'R']
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    movie_set = all_movies.loc[all_movies['Distributor'].apply(
        lambda x: x in dists)]

    # Creates flags for movie by distributor.
    for distributor in dists:
        movie_set[distributor.replace(
            ' ', '')] = movie_set['Distributor'].apply(lambda x: 1 if x == distributor else 0)

    for rating in ratings:
        movie_set[rating] = movie_set['MPAA'].apply(
            lambda x: 1 if x == rating else 0)

    for month in months:
        movie_set[month] = movie_set['Month'].apply(
            lambda x: 1 if x == month else 0)

    def extract_director(node):
        bs_node = BeautifulSoup(node, 'lxml')

        return bs_node.html.body.a.contents[0]

    directors = movie_set['Director'].apply(lambda x: extract_director(x))
    movie_set['Director'] = directors

    rats = movie_set.groupby('Director').mean()
    movie_set['DirUR'] = movie_set['Director'].apply(
        lambda x: rats.loc[x].UserRating)
    movie_set['DirMS'] = movie_set['Director'].apply(
        lambda x: rats.loc[x].Metascore)

    genres = ('Action', 'Adventure', 'Sci-Fi', 'Animation',
              'Comedy', 'Thriller', 'Drama', 'Music', 'Romance',
              'Fantasy', 'Biography', 'Horror', 'Crime', 'Sport', 'Mystery')

    for genre in genres:
        movie_set[genre] = movie_set['Genres'].apply(
            lambda x: 1 if re.search(genre, x) != None else 0)

    # Gross seems to have a polynomial relationship with Theaters.
    movie_set['Thea2'] = movie_set['Theaters']

    movie_set.drop(columns=['ReleaseDate', 'TotalGross', 'Release', 'MPAA', 'Director', 'Genres',
                            'ReleaseURL', 'DistributorURL', 'Distributor', 'datetime', 'Month'], inplace=True)
    return movie_set


make_movie_set()
