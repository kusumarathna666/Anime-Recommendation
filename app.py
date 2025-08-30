'''
On the website open recommend popular animes and New Animes

when a content is selected recommend similar anime

Will also include collaborative filtering
'''

import pickle
import streamlit as st
import requests
import numpy as np
import random

def fetch_poster(mal_id):
    api = 'c53353c21a96e75b6a191826c417a5f7'

    headers = {
    'X-MAL-CLIENT-ID': api
    }

    response = requests.request(url = f'https://api.myanimelist.net/v2/anime/{mal_id}?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics',
                    headers=headers,
                    method='get')
    return response.json()['main_picture']['medium']

def content_based_recommend(anime_name):
    index = anime[anime['name'] == anime_name].index[0]
    distances = sorted(list(enumerate(similarity_content[index])), reverse=True, key=lambda x:x[1])
    data = []
    for i in distances[1:6]:
        data.append(anime.iloc[i[0]]['name'])
    return data

def collaborative_recommend(anime_name):
    index = np.where(pt.index == anime_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score_collab[index])), key=lambda x:x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        data.append(pt.index[i[0]])
    return data

def recommend(anime_name, n_recommend=5):

    content = content_based_recommend(anime_name)
    collab = collaborative_recommend(anime_name)

    recommendations_anime = list(set(content + collab))[-n_recommend:]
    recommendations_anime.reverse()
    recommendations_pictures = []
    for i in recommendations_anime:
        mal_id = anime[anime['name'] == i]['MAL_ID'].iloc[0]
        recommendations_pictures.append(fetch_poster(mal_id))

    return recommendations_anime,recommendations_pictures

def recommend_popular(n_recommend=5):
    recommendations_anime = random.sample(list(popular_df['name']), 5)
    recommendations_pictures = []
    for i in recommendations_anime:
        mal_id = anime[anime['name'] == i]['MAL_ID'].iloc[0]
        recommendations_pictures.append(fetch_poster(mal_id))

    return recommendations_anime,recommendations_pictures

st.header('Anime Recommender System')
anime = pickle.load(open('anime.pkl','rb'))
similarity_content = pickle.load(open('similarity.pkl','rb'))

popular_df = pickle.load(open('popular_df.pkl', 'rb'))

similarity_score_collab = pickle.load(open('similarity_scores_collab.pkl', 'rb'))
pt = pickle.load(open('pt_collab.pkl', 'rb'))

movie_list = pt.index.values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5, gap='small')
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

st.subheader('Popular Recommendation')
recommended_movie_names,recommended_movie_posters = recommend_popular()
col1, col2, col3, col4, col5 = st.columns(5, gap='small')
with col1:
    st.text(recommended_movie_names[0])
    st.image(recommended_movie_posters[0])
with col2:
    st.text(recommended_movie_names[1])
    st.image(recommended_movie_posters[1])

with col3:
    st.text(recommended_movie_names[2])
    st.image(recommended_movie_posters[2])
with col4:
    st.text(recommended_movie_names[3])
    st.image(recommended_movie_posters[3])
with col5:
    st.text(recommended_movie_names[4])
    st.image(recommended_movie_posters[4])