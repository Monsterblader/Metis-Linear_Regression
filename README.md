# Predicting Movie Grosses Using Linear Regression

### Overview

As theaters were shut down for a significant period of time during 2020, I was curious to see if I could develop a model to predict how some movies released during the shut down would have earned had circumstances been normal.

### Features and Target Variables

My target variable:
- total domestic gross.

I used the following features:
- continuous:
  - the movie's budget;
  - the average users' rating;
  - the critics' Metascore;
  - the number of theaters in which the movie was released.

- categorical:
  - MPAA rating;
  - distribution studio;
  - month of release;
  - genre

- derived:
  - director - average user rating of all director's movies;
  - square of the number of theaters - the gross receipts seemed to have a quadratic relationship with the number of theaters in which it was displayed.

*Comments on features:*
*I ended up with a lot of dummy variables and few continuous ones.  This was problematic as the paucity of inputs left me with few parameters to shape a predictor.  I was interested to see if and how so many dummy variables could shape a model, but as we have not yet covered that topic, I only really had a lot of over-fit and not enough tools to integrate dummy variables.*

### Sources

- TheMovieDB.org;
- BoxOfficeMojo.com;
- IMDB.com.

*Comments on sources:*
*TheMovieDB.org had inconsistent layouts and didn't always have data, so I spent a disproportionate amount of time scraping the site, only to end up with almost nothing that I could use.  While I could restart with a different website, I could not reset my clock, and that deficiency affected my project.*

### Tools

- Python 
- BeautifulSoup
- Sklearn
