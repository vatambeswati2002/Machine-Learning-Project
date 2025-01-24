import streamlit as st
import pandas as pd
import pickle

st.title("Startup Performance Dashboard")

st.sidebar.header('User Input Parameters')

def user_input_features():
    lf = st.sidebar.selectbox('age_last_funding_year',(3,  9,  1,  5,  4,  6, 11,  2,  8,  7,  0, 10, 20, -1, 16, 12, 14,
       -9, 21, 13))
    fm = st.sidebar.selectbox('age_first_milestone_year',(4,   7,   1,   6,   0,   5,   3,   8,   2,  10,  -1,   9, -14,
        11,  -2,  12,  16,  -6,  -3,  13,  24,  15,  -7))
    lm = st.sidebar.selectbox('age_last_milestone_year',(6,  7,  2,  0,  5,  9, 10,  4,  8, 12,  3,  1, -1, 11, 13, 14, 18,
       -3, 24, 15, -7))
    re = st.sidebar.selectbox('relationships',(3,  9,  5,  2,  6, 25, 13, 14, 22,  8,  0, 15, 12,  7, 10,  1,  4,
       37, 18, 26, 11, 17, 24, 16, 21, 27, 30, 33, 32, 23, 57, 20, 35, 19,
       45, 31, 29, 63, 42, 28, 38))
    
    fr = st.sidebar.selectbox('funding_rounds',(3,  4,  1,  2,  5,  7,  6, 10,  8))
    
    fusd = st.slider('funding_total_usd',min_value=1.100000e+04	,max_value=5.700000e+09,step=0.5)
    ml = st.sidebar.selectbox('milestones',(3, 1, 2, 4, 0, 5, 6, 8))
    os = st.sidebar.selectbox('is_otherstate',(0,1))
    
    a = st.sidebar.selectbox('has_roundA',(0,1))
    b = st.sidebar.selectbox('has_roundB',(0,1))
    c = st.sidebar.selectbox('has_roundC',(0,1))
    d = st.sidebar.selectbox( 'has_roundD',(0,1))
    
    avg = st.sidebar.selectbox('avg_participants',(1,  4,  3,  2,  5,  9,  6,  7, 10,  8, 12, 11, 16))
    top = st.sidebar.selectbox('is_top500',(0,1))
    year = st.sidebar.selectbox('closed_at_year',(2024, 2012, 2011, 2013, 2010, 2008, 2009, 2001, 2005, 2007))
    month = st.sidebar.selectbox('closed_at_month',(11,  1,  2, 10,  7,  4,  3,  8,  6,  9, 12,  5))
    at_year = st.slider('first_funding_at_year',min_value=2000,max_value=2013,step=1)
    
    
    
    
    data = {'age_last_funding_year':lf,
            'age_first_milestone_year':fm,
            'age_last_milestone_year':lm,
            'relationships':re,
            
            'funding_rounds':fr,
            
            'funding_total_usd':fusd,
            'milestones':ml,
            'is_otherstate':os,
            
            'has_roundA':a,
            'has_roundB':b,
            'has_roundC':c,
            'has_roundD':d,
            
            'avg_participants':avg,
            'is_top500':top,
            'closed_at_year': year,
            'closed_at_month':month,
            'first_funding_at_year':at_year
            
            
            }
    
    features = pd.DataFrame(data,index=[0])
    return features

df = user_input_features()
st.subheader('User Input Parameters')
st.write(df)

with open(file='final_model.sav',mode="rb")as f1:
    model=pickle.load(f1)
    
prediction = model.predict(df) 

st.subheader('Predicted Result')  

st.write(prediction[0]) 