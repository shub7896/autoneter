import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster_and_link(music_title):
    try:
        API_KEY = "aedd7d6e8bdb5297123ae81e2c77c321"
        response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=track.search&track={music_title}&api_key={API_KEY}&format=json")
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        tracks = data.get('results', {}).get('trackmatches', {}).get('track', [])
        if tracks:
            # Assuming the first track found is the one we want
            poster_url = tracks[0].get('image', [])[2].get('#text', '')
            track_url = tracks[0].get('url', '')
            return poster_url, track_url
        else:
            st.error("No results found for the music title.")
            return None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster and track link: {e}")
        return None, None
    except ValueError as ve:
        st.error(f"Error parsing JSON response: {ve}")
        return None, None

def recommend(musics):
    try:
        music_index = music[music['title'] == musics].index[0]
        distances = similarity[music_index]
        music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_music = []
        recommended_music_poster = []
        recommended_music_links = []
        for i in music_list:
            music_title = music.iloc[i[0]].title
            poster_link, track_link = fetch_poster_and_link(music_title)
            if poster_link:
                recommended_music.append(music_title)
                recommended_music_poster.append(poster_link)
                recommended_music_links.append(track_link)
        return recommended_music, recommended_music_poster, recommended_music_links
    except IndexError:
        st.error("Music not found or insufficient data for recommendation.")
        return [], [], []


music_dict = pickle.load(open(r'C:\Users\maury\Music\music\music_rec_new\musicrec.pkl', 'rb'))
music = pd.DataFrame(music_dict)


similarity = pickle.load(open(r'C:\Users\maury\Music\music\music_rec_new\similarities.pkl', 'rb'))



st.title('Music Recommender Lastfm Hindi')

selected_music_name = st.selectbox('Select a music you like', music['title'].values)

if st.button('Recommend'):
    names, posters, links = recommend(selected_music_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    
    for name, poster, link in zip(names, posters, links):
        with col1:
            st.text(name)
            st.markdown(f"[![Poster]({poster})]({link})")

