# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 18:00:39 2024

@author: girir
"""

import streamlit as st
import pandas as pd
import pickle

st.title("Startup Performance")

st.sidebar.header('User Input Parameters')

def user_input_features():
    # Slider for values with a range (min, max, step)
    lf = st.sidebar.slider('Age of Last Funding Year', min_value=-10, max_value=21, step=1)
    fm = st.sidebar.slider('Age of First Milestone Year', min_value=-14, max_value=24, step=1)
    lm = st.sidebar.slider('Age of Last Milestone Year', min_value=-7, max_value=24, step=1)
    re = st.sidebar.slider('Number of Relationships', min_value=0, max_value=63, step=1)
    
    fr = st.sidebar.slider('Funding Rounds', min_value=1, max_value=10, step=1)
    
    fusd = st.sidebar.slider('Funding Total USD', min_value=1.100000e+04, max_value=5.700000e+09, step=0.5)
    ml = st.sidebar.slider('Number of Milestones', min_value=0, max_value=8, step=1)
    os = st.sidebar.selectbox('Is Other State?', [0, 1])
    
    a = st.sidebar.selectbox('Has Round A?', [0, 1])
    b = st.sidebar.selectbox('Has Round B?', [0, 1])
    c = st.sidebar.selectbox('Has Round C?', [0, 1])
    d = st.sidebar.selectbox('Has Round D?', [0, 1])
    
    # Using slider for avg_participants with a range
    avg = st.sidebar.slider('Average Participants', min_value=1, max_value=16, step=1)
    top = st.sidebar.selectbox('Is Top 500?', [0, 1])
    
    year = st.sidebar.selectbox('Closed At Year', [2024, 2012, 2011, 2013, 2010, 2008, 2009, 2001, 2005, 2007])
    month = st.sidebar.selectbox('Closed At Month', [11, 1, 2, 10, 7, 4, 3, 8, 6, 9, 12, 5])
    
    at_year = st.sidebar.slider('First Funding At Year', min_value=2000, max_value=2013, step=1)
    
    data = {'age_last_funding_year': lf,
            'age_first_milestone_year': fm,
            'age_last_milestone_year': lm,
            'relationships': re,
            'funding_rounds': fr,
            'funding_total_usd': fusd,
            'milestones': ml,
            'is_otherstate': os,
            'has_roundA': a,
            'has_roundB': b,
            'has_roundC': c,
            'has_roundD': d,
            'avg_participants': avg,
            'is_top500': top,
            'closed_at_year': year,
            'closed_at_month': month,
            'first_funding_at_year': at_year
            }
    
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()
st.subheader('User Input Parameters')
st.write(df)

# Load model and predict
with open(file='final_model.sav', mode="rb") as f1:
    model = pickle.load(f1)

prediction = model.predict(df)

st.subheader('Predicted Result')
st.write(prediction[0])