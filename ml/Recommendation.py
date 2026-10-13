
# Movie Recommendation System
# Content-Based Filtering using TF-IDF and Cosine Similarity

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Create a sample movie dataset
data = {
    'title': [
        'Avengers', 'Iron Man', 'Thor', 'Batman',
        'Superman', 'Spider-Man', 'Interstellar',
        'Inception', 'Titanic', 'The Notebook'
    ],
    'genre': [
        'Action Superhero Adventure',
        'Action Superhero Sci-Fi',
        'Action Superhero Fantasy',
        'Action Superhero Crime',
        'Action Superhero Sci-Fi',
        'Action Superhero Adventure',
        'Sci-Fi Space Drama',
        'Sci-Fi Thriller Mystery',
        'Romance Drama',
        'Romance Drama'
    ],
    'description': [
        'Heroes unite to save the world from evil forces',
        'A genius builds a powerful armored suit',
        'A superhero uses a magical hammer to fight enemies',
        'A dark hero fights crime and protects the city',
        'A powerful alien hero saves humanity',
        'A young hero gains special powers and fights crime',
        'Astronauts travel through space to save humanity',
        'A thief enters dreams to steal information',
        'A romantic couple falls in love on a ship',
        'Two people experience a deep and lasting love'
    ]
}

df = pd.DataFrame(data)

# 2. Combine genre and description
df['features'] = df['genre'] + ' ' + df['description']

# 3. Convert text into numerical vectors
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['features'])

# 4. Calculate cosine similarity
similarity_matrix = cosine_similarity(tfidf_matrix)

# 5. Define recommendation function
def recommend_movies(movie_name, top_n=5):
    matches = df.index[
        df['title'].str.lower() == movie_name.strip().lower()
    ].tolist()

    if not matches:
        print("Movie not found in the dataset.")
        return

    movie_index = matches[0]

    # Get similarity scores for the selected movie
    scores = list(enumerate(similarity_matrix[movie_index]))

    # Sort by similarity, excluding the selected movie itself
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    scores = [item for item in scores if item[0] != movie_index]

    # Display top recommendations
    print(f"\nMovies recommended for: {df.iloc[movie_index]['title']}")
    print("-" * 45)

    for index, score in scores[:top_n]:
        print(
            f"{df.iloc[index]['title']} "
            f"(Similarity: {score:.2f})"
        )

# 6. Display the dataset
print("Available Movies:")
print(df[['title', 'genre']].to_string(index=False))

# 7. Get recommendations
recommend_movies('Avengers', top_n=5)

# Try other movies:
# recommend_movies('Titanic', top_n=3)
# recommend_movies('Interstellar', top_n=4)
# recommend_movies('Batman', top_n=3)
