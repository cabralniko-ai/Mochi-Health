import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/129DOutQCa3ZVk8ZAnX3dLtLzyZ_BJO8yMW7Eotzf84k/edit?usp=sharing").sheet1



# Streamlit UI
st.title("Mood Ticketing Platorm")

# Mood logging section
st.header("Enter your Mood")

mood_options = ["😊 Happy", "😠 Frustrated", "😕 Confused", "🎉 Excited"]
selected_mood = st.selectbox("Select your mood:", mood_options)
note = st.text_input("Optional note:")

if st.button("Submit Mood"):
    date = datetime.now().strftime("%Y-%m-%d")
    print('this is time stamp', date)
    sheet.append_row([date, selected_mood, note])
    st.success("Mood logged!")

st.header("Mood Summary (Today)")
# Fetch all data from sheet
data = sheet.get_all_records()
df = pd.DataFrame(data)

if not df.empty:
    df['cDate'] = pd.to_datetime(df['Date']).dt.date
    today = datetime.now().date()
    today_df = df[df['cDate'] == today]

    if not today_df.empty:
        print('test worked')
        mood_counts = today_df['mood'].value_counts().reset_index()
        mood_counts.columns = ['mood', 'count']  # rename columns to known names
        fig = px.bar(
            mood_counts,
            x='mood',
            y='count',
            color='mood',
            title=f"Mood Counts for {today}"
        )
        
        st.plotly_chart(fig)
    else:
        st.info("No moods logged today yet.")
else:
    st.info("No moods logged yet.")
