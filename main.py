import streamlit as st
import lyricsgenius 
from google import genai

st.title("Desi Hip-Hop Tracker")
st.write("Enter a song to understand its literal meaning (Slang + Telugu meaning).")

with st.sidebar:
    st.header("API KEYS")
    genius_token = st.text_input("Genius access token", type="password")
    gemini_key = st.text_input("Gemini api key",type="password")

song_title = st.text_input("Song name")
artist_name = st.text_input("Artist name")

if st.button("Decode lyrics"):
    if not genius_token or not gemini_key:
        st.error("Please enter valid key")
    else:
        genius =  lyricsgenius.Genius(genius_token)

        client = genai.Client(api_key=gemini_key)

    with st.status("Fetching lyrics from Genius"):
        try:
            song = genius.search_song(song_title,artist_name)
            lyrics = song.lyrics
            st.success("Lyrics Found!")
        except:
            st.error("Song not found.Check Spelling!")
            st.stop()

    with st.status("Asking AI to decode slang......"):
        prompt =f"""
        Analyse these hindi rap lyrics:
        {lyrics}

        1. Summarize the meaning in English.
        2. Translate the hook/chorus to conversational Telugu.
        3. Explain all key slang terms or metaphors used.
            """

        response = client.models.generate_content(
                model='gemini-flash-latest', 
                contents=prompt
            )
        st.write(response.text)
    with st.expander("See original hindi lyrics"):
        st.text(lyrics)


