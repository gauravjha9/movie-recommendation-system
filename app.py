from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# Load data
movies = pickle.load(open('./model/movies.pkl', 'rb'))
similarity = pickle.load(open('./model/similarity.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html', movie_list=movies['title'].values)


@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.form['movie']

    # Check if the movie exists in the list
    if movie not in movies['title'].values:
        # If movie not found, return a message and the original movie list
        return render_template(
            'index.html',
            movie_list=movies['title'].values,
            recommendations=None,
            selected_movie=movie,
            error_message="Movie not found. Please try again."
        )
    
    # Proceed with recommendation logic if movie is found
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = [movies.iloc[i[0]].title for i in movie_list]

    return render_template(
        'index.html',
        movie_list=movies['title'].values,
        recommendations=recommended_movies,
        selected_movie=movie
    )



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
