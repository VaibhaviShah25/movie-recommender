import streamlit as st
import pandas as pd
import pickle
import requests
import base64

# ====== FUNCTIONS ======
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f055139c681552c3e68d8301ffa14699&language=en-US"
    data = requests.get(url).json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded

# ====== LOAD DATA ======
movies_dict = pickle.load(open("movies_dict1.pkl","rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

# ====== STREAMLIT APP ======
st.title('Movie Recommendation System')

# ====== SPIDERMAN IMAGE (CHANGE PATH IF NEEDED) ======
img_base64 = get_base64_image("spiderman2.jpg")
img_base64_2 = get_base64_image("spiderman3.jpg")

# ====== CUSTOM CSS ======
st.markdown(f"""
    <style>
    /* Main title */
    .css-10trblm {{
        font-size: 50px !important;
        font-weight: 900;
        text-align: center;
        color: #E50914; /* Netflix red */
    }}

    /* Dropdown label */
    label {{
        font-size: 20px !important;
        font-weight: bold;
        color: white;
    }}

    /* Movie name below poster */
    .movie-title {{
        font-size: 18px !important;
        font-weight: bold;
        text-align: center;
        margin-top: 5px;
    }}

    /* Button styling */
    .stButton>button {{
        background-color: #E50914;
        color: white;
        font-size: 18px;
        border-radius: 8px;
        height: 45px;
        width: 150px;
    }}

    .stApp {{
        background: 
            url("data:image/png;base64,{img_base64}") no-repeat top right,
            url("data:image/png;base64,{img_base64_2}") no-repeat bottom left;
        background-size: 300px, 200px; /* top-right bigger, bottom-left smaller */
        background-color: #000000;
        opacity: 0.9; /* slightly transparent */
    }}
    </style>
""", unsafe_allow_html=True)

# ====== UI ======
selected_movie_name = st.selectbox(
    "What's your favourite movie ? ", movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.markdown(f"<p class='movie-title'>{names[0]}</p>", unsafe_allow_html=True)
    with col2:
        st.image(posters[1])
        st.markdown(f"<p class='movie-title'>{names[1]}</p>", unsafe_allow_html=True)
    with col3:
        st.image(posters[2])
        st.markdown(f"<p class='movie-title'>{names[2]}</p>", unsafe_allow_html=True)
    with col4:
        st.image(posters[3])
        st.markdown(f"<p class='movie-title'>{names[3]}</p>", unsafe_allow_html=True)
    with col5:
        st.image(posters[4])
        st.markdown(f"<p class='movie-title'>{names[4]}</p>", unsafe_allow_html=True)
