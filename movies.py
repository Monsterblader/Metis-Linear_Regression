# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ## Get list of movies from 2020
# This code has successfully retrieved a list of movies for 2020 and is no longer needed.  It is being archived for reference purposes.
#
# ```python
# movies_2020_url = 'https://us.gowatching.com/mainpage/?utm_source=b10002_002_20200306'
# movies_2020 = requests.get(movies_2020_url)
# movies_2020_html = movies_2020.text
# soup_2020 = BeautifulSoup(movies_2020_html, 'lxml')
# soup_list_2020 = soup_2020.find_all(class_='movie_list')
# soup_list_2020 = soup_2020.find_all('a', class_='item owntitle')
# movie_titles_2020 = [title.get('title') for title in soup_list_2020]
#
# movie_file = open('2020_movies.txt', 'w')
# for movie in movie_titles_2020:
#     movie_file.write(movie)
#     movie_file.write('\n')
# movie_file.close()
# ```
# %% [markdown]
# ## Iterate over list of movies and get director, actor, rating, and budget data.
#
# ```python
# # Only run this line once.
# movie_titles_2020 = pd.DataFrame(movie_titles_2020).T
#
# def get_movie_page(url, url_base='https://www.themoviedb.org'):
#     """Get a movie's page from https://www.themoviedb.org.
#
#     Keyword arguments:
#     url_base -- the source website
#     url -- the path to the search page containing the movie
#     """
#     query = '/search?query='
#     page = requests.get(url_base + query + url)
#     result_page = BeautifulSoup(page.text, 'lxml')
#     movie_url = url_base + result_page.find(class_ = 'result').get('href')
#
#     page = requests.get(movie_url)
#     return BeautifulSoup(page.text, 'lxml')
#
# def get_movie_details(movie_page):
#     """Extract a movie's details from the source page
#
#     Keyword arguments:
#     movie_page -- the HTML of the movie's page
#     """
#     rating = movie_page.find('span', class_ = 'certification').contents[0].strip()
#     director_node = movie_page.find('li', class_ = 'profile').find('a')
#     director = {'name': director_node.contents[0], 'url': director_node.get('href')}
#     actor_node = movie_page.find('ol', class_ = 'people scroller').find_all('a')
#     actors = [{'name': a.contents[0], 'url': a.get('href')} for i, a in enumerate(actor_node[:-1]) if i % 2 == 1]
#     budget = movie_page.find('section', class_ = 'facts left_column').find_all('p')[2].contents[1].strip()
#     genre_node = movie_page.find('span', class_ = 'genres').find_all('a')
#     genre = [{'type': node.contents[0], 'url': node.get('href')} for node in genre_node]
#     return [rating, director, actors, budget, genre]
#
# movie_list = []
# for title in movie_titles_2020[0]:
#     movie_page = get_movie_page(title)
#     movie_list.append(get_movie_details(movie_page))
#
# sys.setrecursionlimit(10000)
# pickle_file = open('movie_list.pkl', 'wb')
# pickle.dump(movie_list, pickle_file)
# pickle_file.close()
# sys.setrecursionlimit(3000)
# ```
# %% [markdown]
# ## Get list of top grossing directors.
#
# ```python
# top_directors = get_html('https://en.wikipedia.org/wiki/List_of_highest-grossing_directors')
# director_table = top_directors.find('table').find_all('a')
# director_list = [{'name': director.contents[0], 'url': director.get('href')} for i, director in enumerate(director_table) if i % 3 == 1]
# write_pickle(director_list, 'top_grossing_directors')
# ```
# %% [markdown]
# ## Save list of movies released in 2020 as a pickle file instead of CSV.
#
# ```python
# movie_titles_2020 = pd.DataFrame(movie_titles_2020).T
# write_pickle(movie_titles_2020, 'movie_titles_2020')
# ```
# %% [markdown]
# ## Parses the director list and retrieves his or her filmography.
#
# ```python
# director_list = [dire[1]['name'] for dire in movie_data]
#
# filmography = []
# for director_name in director_list:
#     director_page = search_tmdb(director_name)
#     if director_page != None:
#         filmography.append(
#             {'name': director_name, 'films': get_filmography_from_page(BeautifulSoup(director_page, 'lxml'))})
# ```
# %% [markdown]
# ## Extracts movie data from table into a list
# ```python
# bo_list = []
# for i in date_range:
#     page = requests.get('https://www.boxofficemojo.com/year/' +
#                         str(i) + '/?grossesOption=calendarGrosses')
#     bs_page = BeautifulSoup(page.text, 'lxml')
#     bs_table = bs_page.find_all('table')
#     bs_tr = bs_table[0].find_all('tr')[1:]
#     bo_list.append(bs_tr)
#
# data_list = []
# for row in bo_list[7]:
#     row_td = row.find_all('td')
#     one = row_td[1].find('a').get('href')
#     two = row_td[1].find('a').contents[0]
#     three = row_td[5].contents[0]
#     four = row_td[6].contents[0]
#     five = row_td[7].contents[0]
#     six = row_td[8].contents[0]
#     if row_td[9].find('a'):
#         seven = row_td[9].find('a').get('href')
#         eight = row_td[9].find('a').contents[0]
#     else:
#         seven = '-'
#         eight = '-'
#     data_list.append([one, two, three, four, five, six, seven, eight])
# ```
# %% [markdown]
# ## Functions for scraping TheMovieDB.org
#
# ```python
# def search_tmdb(search_string):
#     """With the given search_string, sends a search request to TheMovieDB.org
#     and returns the search target's page as a BeautifulSoup object.
#
#     Keyword arguments:
#     search_string -- the name for which to search - escaping characters is not necessary.
#     """
#     director_index = None
#     response_text = requests.get(
#         'https://www.themoviedb.org/search/person?query=' + search_string).text
#     response_soup = BeautifulSoup(response_text, 'lxml')
#     results = response_soup.find_all(class_='content')
#
#     for i, result in enumerate(results):
#         if result.p:
#             if result.find_all('p')[1].span.contents[0] == 'Directing':
#                 director_index = i
#                 break
#
#     if director_index != None:
#         target_page = requests.get(
#             'https://www.themoviedb.org' + results[director_index].find(class_='result').get('href')).text
#     else:
#         target_page = None
#
#     return target_page
#
#
# def get_filmography_from_page(page):
#     """Retrieves a director's filmography from TheMoviedb.org.
#
#     Keyword arguments:
#     page -- the HTML of the director's page
#     """
#     directory = []
#     directing_index = -1
#
#     tabl = page.find_all('div', class_='credits_list')
#     h3 = tabl[0].find_all('h3')
#     for i, node in enumerate(h3):
#         if node.contents[0] == 'Directing':
#             directing_index = i
#             break
#     if len(h3):
#         directing = tabl[0].find_all('table', class_='card credits')[
#             directing_index].find_all('table')
#         for movie in directing:
#             year = movie.find('td', class_='year').contents[0]
#             if year.isnumeric() and int(year) < 2020:
#                 aa = movie.find('a')
#                 directory.append(
#                     {'name': aa.contents[0], 'url': aa.get('href')})
#
#     return directory
# ```

# %%
from sklearn.preprocessing import PolynomialFeatures
import csv
import pickle
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import dateutil.parser
from IPython.core.display import display, HTML
from bs4 import BeautifulSoup
import requests

%matplotlib inline

# %%


def write_pickle(data, file_name):
    """Create a pickle file

    Keyword arguments:
    data -- the information to be saved
    file_name -- the name of the file without an extension
    """
    sys.setrecursionlimit(20000)
    pickle_file = open(file_name + '.pkl', 'wb')
    pickle.dump(data, pickle_file)
    pickle_file.close()
    sys.setrecursionlimit(3000)

    return True


def read_pickle(file_name):
    """Import a pickle file

    Keyword arguments:
    file_name -- the name of the file to be read without an extension
    """
    pickle_file = open(file_name + '.pkl', 'rb')
    file = pickle.load(pickle_file)
    pickle_file.close()

    return file


def write_csv(data, file_name):
    """Saves a flat dictionary to a .CSV.

    Keyword arguments:
    data -- a flat dictionary
    file_name -- the desired filename without an extension
    """
    with open(file_name + '.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            if type(row) == dict:
                csv_writer.writerow(list(row.values()))
            else:
                csv_writer.writerow(row)

    return True


def read_csv(file_name):
    """Reads a .CSV into a list.

    Keyword arguments:
    file_name -- the desired file to load without an extension
    """
    result = []
    with open(file_name + '.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csv_reader:
            result.append(row)

    return result


def get_html(url):
    """Loads the HTML from the given URL.

    Keyword arguments:
    url -- the URL to load
    """
    response_text = requests.get(url).text

    return BeautifulSoup(response_text, 'lxml')


# %%
movie_titles_2020 = read_pickle('movie_titles_2020')
movie_data = read_pickle('movie_list')


# %%
# flatten filmography - used for director list, might use for actor list.
flat_filmography = []

for director in filmography:
    for film in director['films']:
        if film['url'].find('tv') == -1:
            flat_filmography.append(
                {'director': director['name'], 'film': film['name'].contents[0], 'url': film['url']})


# %%
# TODO get studio
# TODO get number of studios in release
# TODO get writer?
# TODO get critic/user ratings?

# TODO get actor filmographies
# TODO get list of old releases from actor and director filmographies


# %%
# Load and clean 2018 movies.
movies_2018 = pd.DataFrame(read_csv('data/2018_movies'))
movies_2018['datetime'] = pd.to_datetime(movies_2018[5] + ', 2018')
movies_2017 = pd.DataFrame(read_csv('data/2017_movies'))
movies_2017['datetime'] = pd.to_datetime(movies_2017[5] + ', 2017')
movies_2016 = pd.DataFrame(read_csv('data/2016_movies'))
movies_2016['datetime'] = pd.to_datetime(movies_2016[5] + ', 2016')
movies_2015 = pd.DataFrame(read_csv('data/2015_movies'))
movies_2015['datetime'] = pd.to_datetime(movies_2015[5] + ', 2015')
movies_2014 = pd.DataFrame(read_csv('data/2014_movies'))
movies_2014['datetime'] = pd.to_datetime(movies_2014[5] + ', 2014')
movies_2013 = pd.DataFrame(read_csv('data/2013_movies'))
movies_2013[5] = movies_2013[5].apply(
    lambda x: 'Feb 28' if x == 'Feb 29' else x)
movies_2013['datetime'] = pd.to_datetime(movies_2013[5] + ', 2013')
movies_2012 = pd.DataFrame(read_csv('data/2012_movies'))
movies_2012['datetime'] = pd.to_datetime(movies_2012[5] + ', 2012')
movies_2011 = pd.DataFrame(read_csv('data/2011_movies'))
movies_2011['datetime'] = pd.to_datetime(movies_2011[5] + ', 2011')
movies_2010 = pd.DataFrame(read_csv('data/2010_movies'))
movies_2010['datetime'] = pd.to_datetime(movies_2010[5] + ', 2010')

all_movies = pd.concat((movies_2018, movies_2017, movies_2016, movies_2015, movies_2014,
                        movies_2013, movies_2012, movies_2011, movies_2010))


def CountFrequency(my_list):
    freq = {}

    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1

    return freq


# Filters distributors who have released more than 80 movies over the data set.
distributor_count = CountFrequency(all_movies[7])
# dists = list({
# k: v for (k, v) in distributor_count.items() if (v > 80) and (k != '-')})
dists = ['Walt Disney Studios Motion Pictures', 'Universal Pictures', 'Twentieth Century Fox',
         'Sony Pictures Entertainment (SPE)', 'Paramount Pictures', 'Warner Bros.']
movie_set = all_movies.loc[all_movies[7].apply(
    lambda x: x in dists), [2, 3, 5, 7]]
movie_set.columns = ['Gross', 'Theaters', 'Date', 'Distributor']
movie_set['Gross'] = movie_set['Gross'].apply(
    lambda x: int(re.sub(r'[$,]', '', x)))
movie_set['Theaters'] = movie_set['Theaters'].apply(
    lambda x: x.replace('-', '0'))
movie_set['Theaters'] = movie_set['Theaters'].apply(
    lambda x: int(x.replace(',', '')))


# %%
# Creates flags for movie by distributor.
for distributor in dists:
    movie_set[distributor.replace(
        ' ', '')] = movie_set['Distributor'].apply(lambda x: 1 if x == distributor else 0)


# %%
movie_set.corr()


# %%
plt.figure(figsize=(20, 20))

sns.heatmap(movie_set.corr(),
            cmap="seismic", annot=True, vmin=-1, vmax=1)
plt.gca().set_ylim(len(movie_set.corr())+0.5, -0.5)

# %%
sns.pairplot(movie_set, height=1.5, aspect=1)
# %%
lr = LinearRegression()

X = movie_set['Theaters'].values.reshape(-1, 1)

y = movie_set['Gross']

lr.fit(X, y)
# %%
lr.score(X, y)
# %%
# Bucket directors, studios?, actors by earnings/salaries.
# Genres are not exclusive.

# %%
movie_for_full = movie_set.copy()

del movie_for_full['Date']
del movie_for_full['Distributor']

lr_full = LinearRegression()

X = movie_for_full.loc[:, 'Theaters':'WarnerBros.']

y = movie_for_full['Gross']

lr_full.fit(X, y)

lr_full.score(X, y)
# %%
sm.add_constant(X).head()
# %%
model = sm.OLS(y, sm.add_constant(X))
fit = model.fit()
fit.summary()
# %%
plt.figure(figsize=(10, 7))
plt.scatter(fit.predict(), fit.resid)

plt.axhline(0, linestyle='--', color='gray')
plt.xlabel('Predicted Values', fontsize=18)
plt.ylabel('Residuals', fontsize=18)
# %%
lr_full = LinearRegression()
X = movie_set[['Theaters', 'WaltDisneyStudiosMotionPictures', 'UniversalPictures',
               'TwentiethCenturyFox', 'SonyPicturesEntertainment(SPE)', 'ParamountPictures', 'WarnerBros.']]
y = movie_set['Gross']
lr_full.fit(X, y)
lr_full.score(X, y)

# %%

p = PolynomialFeatures()
X_poly = p.fit_transform(X)

lr_full = LinearRegression()
lr_full.fit(X_poly, y)
lr_full.score(X_poly, y)
# %%
X.shape
# %%
X_poly.shape
# %%
