# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 07:11:40 2024

@author: aiman
"""

import streamlit as st
import pandas as pd
import pickle
import datetime
import os
import numpy as np
import random
from st_aggrid import AgGrid

# Load the trained model outside the function
@st.cache_resource #caches the model loading, so it won't reload the file repeatedly.
def load_model():
    with open(file="final_.sav", mode="rb") as f1:
        return pickle.load(f1)

model = load_model()

# Set up the title of the web application
st.title("Welcome to Startup World")

# Sidebar header for user input
st.sidebar.header('User Input Parameters')

# Path to store user data in the CSV file for future purpose
CSV_FILE = "D://Data Science//ML Algo//ML project by me//startup_data_project//startup_user_data.csv"


# Function to get user inputs from the sidebar
def user_input_features():
    # Get the name of the startup from the user
    name = st.sidebar.text_input("Startup Name",value='Accenture',key='name')
    
    # Dynamically generate a display name for the startup
    startup_name = name if name else "the startup"
    

    # Input for the state code where the startup is located
    state_code = st.sidebar.text_input(
        f"Enter State code where {startup_name} is present", value='NY',key='state_code'
    )

    # Input for the city name in the selected state
    city = st.sidebar.text_input(
        f"Enter the City name in {state_code} (if known)", value='New York',key='city'
    )

    # Input for the zip code of the selected state
    zip_code = st.sidebar.text_input(
        f"Enter the Zip Code of {city} in {state_code} (if known)", value='10001',key='zip_code'
    )
    
    # Input for the date the startup was founded
    founded_date = st.sidebar.date_input(
        f"Founded Date of {startup_name}", 
        max_value=datetime.date.today(), 
        value=datetime.date(2003, 6, 11), 
        key="founded_date"
    )
    
    # Checkbox to indicate if the company is still active
    is_active = st.sidebar.checkbox(f"Is {startup_name} still running?", value=True)
    
    # Determine the end date
    if is_active:
        st.sidebar.write(f"Closed Date: {startup_name} is still running")
        end_date = datetime.date.today()  # Use today's date
    else:
        # Input for the closed date
        end_date = st.sidebar.date_input(
            f"Closed Date of {startup_name}", 
            min_value=founded_date, 
            max_value=datetime.date.today(), 
            key="closed_date"
        )
    
    # Store user data
    closed_date_for_user_data = np.nan if is_active else end_date

    # Calculate the age of the startup in years
    startup_age_in_years = (end_date - founded_date).days // 365
    
    # Input for the total number of funding rounds
    funding_rounds = st.sidebar.number_input(
        f'Number of funding rounds held in {startup_name}',
        min_value=1,  
        value=1,  # Default value
        step=1,  # Increment step
        key='no_of_funding_rounds'  # Unique key to identify the widget
    )

    # Input for the age of the startup at the time of the first funding
    age_range = list(range(startup_age_in_years + 1))
    
    age_first_funding_year = st.sidebar.selectbox(
    f'Age of {startup_name} at first funding (in years)', options=age_range, index=1,key='age_first_funding'
    )


    # Input for the age of the startup at the time of the last funding
    age_last_funding_year = st.sidebar.selectbox(
    f'Age of {startup_name} at last funding (in years)', options=age_range, index=1,key='age_last_funding'
    )

    # Calculate the total funding age in years
    funding_age_years = age_last_funding_year - age_first_funding_year

    # Calculate the years since the last funding
    years_since_last_funding = startup_age_in_years - age_last_funding_year
    
    # take total amount fundings raised by the startup throughout its journey in USD
    funding_total_usd=st.sidebar.number_input(
        f"Total amount of funding (in US dollars) that {startup_name} has received across all funding rounds",
        min_value=0,
        key='funding_total_usd'
    )
    # Input for the total milestones achieved by the startup
    milestones = st.sidebar.number_input(
        f'Total milestones achieved by {startup_name}',
        min_value=0,  
        value=0,  
        step=1,  
        key='milestones_count' ) 

    # Input for the age of the startup at its first milestone
    age_first_milestone_year = st.sidebar.selectbox(
    f'Age of {startup_name} at first milestone (in years)', options=age_range, index=1,key='age_fist_milestone_year'
    )

    # Input for the age of the startup at its last milestone
    age_last_milestone_year = st.sidebar.selectbox(
    f'Age of {startup_name} at last milestone (in years)', options=age_range, index=1,key='age_last_milestone_year'
    )

    # Input for the total number of relationships with other companies
    relationships = st.sidebar.number_input(
        f'Count of relationships {startup_name} has with other companies',0,  # Default value and min_value
        step=1, key='no_of_relationships' 
    )

    # take category of the startup
    category_code=st.sidebar.text_input(f"Category of {startup_name}",value='automobile',key='category')
    
    # Input to check if the startup has a venture capitalist
    has_VC = st.sidebar.checkbox(f"Does {startup_name} have a Venture Capitalist?", value=False, key="has_VC")
    has_VC = 1 if has_VC else 0  # Map the checkbox value to 0 or 1
    
    # Input to check if the startup has an angel investor
    has_angel = st.sidebar.checkbox(f"Does {startup_name} have an Angel Investor?", value=False, key="has_angel")
    has_angel = 1 if has_angel else 0  # Map the checkbox value to 0 or 1


   

    # Input for the number of teams in the startup
    num_teams = st.sidebar.number_input(
        f"Enter the number of teams in {startup_name}:",
        min_value=1,
        step=1,
        value=1,
        key="no_of_teams"
    )
    
    # Create a DataFrame for participant input
    default_data = {"Team": [f"Team {i+1}" for i in range(num_teams)], "Participants": [0] * num_teams}
    participant_df = pd.DataFrame(default_data)
    
    # Dynamically adjust the height of the AgGrid table based on the number of teams
    table_height = 50 + num_teams * 30  # Base height + additional height per row
    
    # Editable DataFrame using AgGrid
    grid_response = AgGrid(
        participant_df, 
        editable=True,
        height=table_height,  # Set dynamic height
        fit_columns_on_grid_load=True)
    
    # Extract updated data
    updated_participant_df = grid_response['data']
    
    # Calculate total and average participants
    total_participants = updated_participant_df["Participants"].sum()
    avg_participants = total_participants / num_teams if num_teams > 0 else 0
    

    # Input for the status of the startup
    status = st.sidebar.selectbox(
        f'Status of {startup_name}', ('acquired', 'closed')
    )
    status = 0 if status == 'acquired' else 1  # Map status to 0 or 1

    # Create a dictionary with all the input values
    data = {
        'startup_age_in_years': startup_age_in_years,
        'funding_rounds': funding_rounds,
        'age_last_funding_year': age_last_funding_year,
        'funding_age_years': funding_age_years,
        'years_since_last_funding': years_since_last_funding,
        'milestones': milestones,
        'age_first_milestone_year': age_first_milestone_year,
        'age_last_milestone_year': age_last_milestone_year,
        'relationships': relationships,
        'has_angel': has_angel,
        'avg_participants': avg_participants,
        'status': status
    }
    
    # storing user data 
    user_data={
        'name':[name],
        'state_code':[state_code],
        'zip_code':[zip_code],
        'city':[city],
        'founded_at':[founded_date],
        'closed_at':[closed_date_for_user_data],
        'funding_rounds':[funding_rounds],
        'age_first_funding_year':[age_first_funding_year],
        'age_last_funding_year':[age_last_funding_year],
        'funding_total_usd':[funding_total_usd],
        'milestones':[milestones],
        'age_first_milestone_year':[age_first_milestone_year],
        'age_last_milestone_year':[age_last_milestone_year],
        'relationships':[relationships],
        'category_code':[category_code],
        'has_VC':[has_VC],
        'has_angel':[has_angel],
        'avg_participants':[avg_participants],
        'status':[status]
        }
    
    # Convert the dictionary to a DataFrame and return it
    return pd.DataFrame(data, index=[0]) ,pd.DataFrame(user_data,index=[0])


# Get the user inputs
df, df2= user_input_features()


# Display the input parameters for verification
st.subheader('User Input Parameters')
st.write(df)

# Quotes for Top 500 prediction
success_quotes = [
    "Man is rewarded for his efforts, not merely his results.– Quran (53:39)",
    "Success is not just about making money but making a difference. - Iqbal Ahmed",
    "The best earnings are from honest work. - Prophet Muhammad (PBUH)",
    "Opportunities are made, they do not just lie around waiting for someone to grab them. - Sheikh Mohammed bin Rashid Al Maktoum",
    "Hard work and determination pave the way to success. - Hamza Yusuf",
    "Victory is reserved for those who are willing to pay its price.– Ali ibn Abi Talib (RA)",
]

# Quotes for Not Top 500 prediction
encouragement_quotes = [
    "Every difficulty comes with ease.– Quran (94:6)",
    "Do not fear failure. Fear being in the exact same place next year as you are today. - Mufti Menk",
    "Great things take time, keep moving forward. - Nouman Ali Khan",
    "Patience and perseverance are the keys to any success. – Imam Al-Ghazali",
    "Do not stop working hard for what you believe in, even if the road is long and the challenges are many. – Nouman Ali Khan",
    "If you fail, rise again. Falling is only a lesson in the art of walking stronger.– Imam Malik"
]


# Button to make a prediction
# Button to make a prediction
if st.button("Predict"):
    # Make predictions using the loaded model
    prediction = model.predict(df)
    prediction_proba = model.predict_proba(df)

    # Display the prediction result
    st.subheader("Prediction")
    
    if prediction == 1:
        st.success("🎉 Congratulations! Your startup ranks in the Top 500!")
        st.balloons()  # Celebration animation
        quote = random.choice(success_quotes)  # Random success quote
        st.markdown(f"💬 **_Quote of the Day:_** {quote}")
    else:
        st.error("Not quite there yet! Keep going, you're doing great! 💪")
        quote = random.choice(encouragement_quotes)  # Random motivational quote
        st.markdown(f"💬 **_Keep Going:_** {quote}")

    # Display prediction probabilities
    st.subheader("Prediction Probability")
    st.write(f"Probability of Top 500: {prediction_proba[0][1]:.2f}")
    st.write(f"Probability of Not Top 500: {prediction_proba[0][0]:.2f}")

    # Save user data to a CSV file
    def save_to_csv(data1, file_name):
        """Save user data to a CSV file."""
        try:
            if os.path.exists(file_name):
                existing_data = pd.read_csv(file_name)
                updated_data = pd.concat([existing_data, data1], ignore_index=True)
            else:
                updated_data = data1

            updated_data.to_csv(file_name, index=False)
            st.sidebar.success("Data submitted and saved successfully!")
        except PermissionError:
            st.sidebar.error("Permission denied. Close the file or check access permissions.")
        except Exception as e:
            st.sidebar.error(f"An error occurred: {e}")

    # Call the function to save data
    save_to_csv(df2, CSV_FILE)

    
    
