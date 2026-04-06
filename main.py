import streamlit as st
import lyricsgenius 
from google import genai

st.set_page_config(page_title="AlgoRhythm" , page_icon="🎧", layout="wide" , initial_sidebar_state="collapsed")

def load_css(style_css):
    try:
        with open(style_css) as f:
            st.markdown(f"<style>{f.read()}</Style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("style.css not found. The app will look plain!")

load_css("style_css")

try:
    genius_token = st.secrets["genius_token"]
    gemini_key = st.secrets["gemini_key"]
except FileNotFoundError:
    st.error("⚠️ Config Error: .streamlit/secrets.toml not found. Please create it!")
    st.stop()
except KeyError as e:
    st.error(f"⚠️ Config Error: Missing key {e} in secrets.toml")
    st.stop()

genius = lyricsgenius.Genius(genius_token)
client = genai.Client(api_key = gemini_key)

@st.cache_data
def get_lyrics(song,artist):
    """
    Fetches lyrics from Genius API. 
    Returns: (lyrics, real_title) or (None, error_message)Docstring for get_lyrics
    
    """
    try:
        song_obj = genius.search_song(song, artist)

        if song_obj:
            return song_obj.lyrics, song_obj.title
        return None, "Track not ofund on Genius Database."
    except Exception as e:
        return None , f"Connection Error: {e}"
    
def get_ai_analysis(lyrics, song_name, artist, language):
    """
    Sends lyrics to Gemini for a Deep Cultural & Hype Analysis.
    """
    prompt = f"""
    You are the ultimate music linguist, historian, and pop-culture insider.
    
    Context:
    - Song: {song_name}
    - Artist: {artist}
    - User's Target Language: {language}
    
    Lyrics (Snippet):
    {lyrics[:3000]} 
    
    Task: Provide a deep, magazine-style analysis of this track. Use clear, engaging language. Format the output exactly with these bold headings:
    
    ### 🧠 The Mentality & Meaning
    - Explain the exact reason these lyrics were written. 
    - What was the artist's headspace, mentality, or emotional state while making this?
    - Translate the core message and the Hook/Chorus into conversational {language}.
    
    ### 📜 History & Context
    - What is the backstory of this song? 
    - Who are they dissing, loving, or referencing? Explain the historical or personal context behind the track.
    
    ### 📖 Slang & Decoder
    - Break down 3-5 specific slang words, double-entendres, or cultural references used in the lyrics.
    - Explain what they actually mean in the context of this specific genre.
    
    ### 🔥 The Hype (Current Trends)
    - Act like a Reddit/Twitter music insider. What is the current internet consensus and hype around {artist} right now?
    - Mention recent viral moments, new album drops (e.g., if it's Kanye, mention 'Bully' or recent news), controversies, or why the internet is talking about them *right now*. Keep the energy high!
    """
    
    try:
        # Note: Gemini 1.5/2.0 Flash is very up-to-date on internet culture,
        # so asking it for "The Hype" will actually pull recent facts!
        response = client.models.generate_content(
            model='gemini-flash-latest', 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI Error: {e}. (You might be hitting the free quota limits)."
    
st.markdown("<h1>🔥 ALGO<span style='color:white'>RHYTHM</span></h1>", unsafe_allow_html=True)
st.markdown("*The Code Behind the Culture.*")

st.markdown("___")

col1, col2, col3 = st.columns([3, 3, 2])
with col1:
    song_title = st.text_input("TRACK", placeholder="e.g. Namastute")
with col2:
    artist_name = st.text_input("ARTIST", placeholder="e.g. Seedhe Maut")
with col3:
    target_lang = st.selectbox("TRANSLATE TO", ["Telugu", "English", "Hindi", "Tamil", "Kannada"])


if st.button("Decode lyrics"):
    if not song_title or not artist_name:
        st.warning("⚠️ PLEASE ENTER BOTH TRACK AND ARTIST NAME.")
    else:
        status_text = st.empty()
        status_text.markdown("Connecting to the database")

        lyrics , result_title = get_lyrics(song_title, artist_name)

        if not lyrics:
            status_text.error(result_title)
            st.stop()

        status_text.empty()

        st.markdown(f"<h3>// {result_title}</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="lyrics-box">
        {lyrics}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<h3>// DECODED ({target_lang.upper()})</h3>", unsafe_allow_html=True)

        with st.spinner("Compiling Slang Dictionary..."):
            analysis = get_ai_analysis(lyrics, result_title, artist_name, target_lang)
            
            st.markdown(f"""
            <div class="analysis-box">
            {analysis}
            </div>
            """, unsafe_allow_html=True)



