import os
import streamlit as st
import numpy as np
from PIL import  Image

# Custom imports 
from multipage import MultiPage
#from pages import data_upload, machine_learning, metadata, data_visualize, redundant # import your pages here
from pages import saved_library, top_artists, recently_played
# Create an instance of the app 
app = MultiPage()

# Title of the main page
#display = Image.open('Logo.png')
#display = np.array(display)
# st.image(display, width = 400)
# st.title("Data Storyteller Application")
#col1, col2 = st.beta_columns(2)
#col1.image(display, width = 400)
st.title("Data Storyteller Application")

# Add all your application here
app.add_page("Explore Your Saved Library", saved_library.app)
app.add_page("Find Your Top Artists", top_artists.app)
app.add_page("Recently Played", recently_played.app)
# The main app
app.run()