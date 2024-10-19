from flask import Flask, request, jsonify
from flask_cors import CORS

import kagglehub

# Download latest version
#path = kagglehub.dataset_download("tmdb/tmdb-movie-metadata")

#print("Path to dataset files:", path)

import pandas as pd
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

df = pd.read_csv('tmdb_5000_movies.csv')

def get_string_from_json(json_data):
    genres = []
    for item in json_data:
        s = ''
        for char in item['name']:
          if char != ' ':
            s += char
        genres.append(s.lower())
    return ' '.join(genres)

def genres_and_keywords_to_string(row):
  genres = json.loads(row['genres'])
  genres = get_string_from_json(genres)

  keywords = json.loads(row['keywords'])
  keywords = get_string_from_json(keywords)
  return "%s %s" % (genres, keywords)

#add the above string represenation of each movie as a column
df['string_representation'] = df.apply(genres_and_keywords_to_string, axis=1)

#instantiate a tfidf object
tfidf = TfidfVectorizer(max_features=2000)

#fit the object on the string representation
X = tfidf.fit_transform(df['string_representation'])

#map the movie index to  movie title in the df
movie_to_index = pd.Series(df.index, index=df['title'])

#using all the above codes, we can create a function which inputs the movies name and returns the most similar movies
def get_recommendations(movie_name, top_n=5):
  index = movie_to_index[movie_name]
  scores = cosine_similarity(X[index].toarray(), X).flatten()
  top_n_matches_indexes = (-scores).argsort()[1:top_n + 1]
  return df['title'].iloc[top_n_matches_indexes]





app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the React app

@app.route('/api/data', methods=['POST'])
def process_data():
    data = request.get_json()  # Parse JSON from request body
    text = data.get('text', '')

    # Create a response with some basic text operations
    response = {
        'original': text,
        'uppercase': text.upper(),
        'length': len(text)
    }

    try:
        return json.dumps(get_recommendations(text).to_list())
    except:
        return json.dumps(['Movie not found'])

    #return jsonify(get_recommendations(text))
    #return jsonify(response)  # Return JSON response

if __name__ == '__main__':
    app.run(port=5000, debug=True)
