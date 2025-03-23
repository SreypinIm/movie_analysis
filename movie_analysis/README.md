### IMDb Movie Recommendation System

### Project Overview
The IMDb Movie Recommendation System is a Python-based application that allows users to search for movies, rate them, and view the top-rated and most popular films. The system includes a user authentication module that enables users to create accounts and log in before accessing movie-related features. It processes movie data from a CSV file and provides insights through text-based search and graphical visualizations.


### Key Features
User Authentication: Users can create accounts, log in, and securely store credentials in user.csv.
Movie Search: Search movies by title, actor, year, or director.
Rating System: Users can rate movies, and the system updates the movie's average rating and popularity.
Top Movie Charts: View the top 10 most popular and top 10 highest-rated movies through pie and bar charts.


### Steps to Run the Code
Clone or Download the Repository:
git clone https://github.com/SreypinIm/movie_analysis.git
cd movie_analysis


### Ensure Required Files Exist
imdb_movie_dataset.csv (Movie dataset file)
user.csv (User account storage; automatically created if not present)


### Dependencies or Installation Instructions
pandas (for handling CSV data)
matplotlib (for generating charts)

### Install Dependencies:
pip install pandas matplotlib

### Run the Script
python main.py
