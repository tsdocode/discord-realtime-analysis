import streamlit as st
import os
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from discord_analysis.firebase.db.realtime_db import RealtimeDB
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import warnings

warnings.filterwarnings('ignore')


load_dotenv()


@st.cache(allow_output_mutation=True)
def load_db():
    db = RealtimeDB(os.getenv("FIREBASE_DB_URL"))
    return db



st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

st.title("Discord Channel Dashboard")
# Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
# after it's been refreshed 100 times.
count = st_autorefresh(interval=5000, key="fizzbuzzcounter")


def get_data():
    db = load_db()
    messages = db.get("server/message_log")

    text = ""

    messages = [messages[i] for i in messages]
    text = " ".join([i["content"] for i in messages])
    messages = pd.DataFrame.from_records(messages)
    messages['time'] = pd.to_datetime(messages['time'])
    messages.set_index('time', inplace=True)
    

    channels = db.get("server/channels")
    members =  db.get("server/members")

    return members, channels, messages, text



def main():


    members, channels, df, text = get_data()

    # create three columns
    m1, m2, m3 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    m1.metric(
        label="Number of members",
        value=members["number_of_members"],
        delta=round(members["number_of_members"]) - 1,
    )

    m2.metric(
        label="Number of channels",
        value=channels["number_of_channels"],
    )

    m3.metric(
        label="Number of messages",
        value=len(df),
    )

    m4, m5 = st.columns(2)


    with m4:
        count_by_date = df.groupby(pd.Grouper(freq='D')).size()

        st.markdown("### Message by date")
        fig2 = px.histogram(data_frame=count_by_date, x=count_by_date.index, y=count_by_date)
        st.plotly_chart(fig2, width=1000)
    with m5:
        st.markdown("### Wordcloud")

        st.markdown("### ")
        st.markdown("### ")
        st.markdown("### ")
        st.markdown("### ")
        st.markdown("### ")

        
        fig, ax = plt.subplots(figsize=(10, 10))
        wordcloud = WordCloud(background_color='white').generate(text)
        ax.imshow(wordcloud)
        ax.axis("off")
        # plt.show()
        m5.pyplot(fig)
        



    
    count_by_sentiment = df.groupby(['sentiment']).size()

    st.markdown("### Sentiment percent")
    fig2 = px.pie(data_frame=count_by_sentiment, values=count_by_sentiment, names=count_by_sentiment.index)
    st.plotly_chart(fig2, width=1000)

    st.markdown("### Message log")

    st.dataframe(df.sort_values(by='time', ascending=False), width=1200)


if __name__ == '__main__':
    main()