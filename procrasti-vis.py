import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import altair as alt

import matplotlib.colors as mcolors

@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)


def display_homepage():
    # Define the CSS styles
    css = """
    body {
        background-color: #F8F8F8;
    }

    h1 {
        color: #470FF4;
        text-align: center;
        font-size: 48px;
        margin-top: 50px;
        margin-bottom: 10px;
    }

    h2 {
        color: #6CCFF6;
        text-align: center;
        font-size: 30px;
        margin-top: 0px;
        margin-bottom: 20px;
    }

    h3 {
        color: #28262C;
        text-align: center;
        font-size: 20px;
        margin-top: 0px;
        margin-bottom: 20px;
    }

    .row::after {
        content: "";
        clear: both;
        display: table;
    }

    .left {
        width: 60%;
        float: left;
    }

    .right {
        width: 40%;
        float: right;
    }

    table {
        border-collapse: collapse;
        margin: auto;
    }

    td, th {
        border: 1px solid #ddd;
        align: center;
        padding: 8px;
    }

    th {
        background-color: #F06449;
        font-size: 30px;
        text-align: center;
        color: white;
    }
    """


    # Put an image
    # st.image("images/logo.png", width=700)

    # Use the CSS styles in the app
    st.write(f'<style>{css}</style>', unsafe_allow_html=True)

    # High titles
    st.write('<h1>Grade Boosters: What are the Hidden Social Media Factors Impacting Your Academic Success?</h1>', unsafe_allow_html=True)
    st.write('<h2>Screen Time is NOT Everything you need to keep track on!</h1>', unsafe_allow_html=True)

    # Create the two-column layout
    col1, col2 = st.columns(2)

    # [Left] Introduction
    with col1:
        st.write(f'<h3>Introduction</h3>', unsafe_allow_html=True)
        text = """
        Nowadays one strives to go faster and further, be more productive, reach higher goals. But at the same time we observe people delaying tasks, focusing on less urgent and easier ones, being easily distracted. Specially with the accessibility of Internet and medias these new habits may have an addicting effect that could lead to poor health, decreased concentration in class, bad time management, lack of appetite for learning and consequently poor academic performance. So procrastination has become an important issue in our society, and in our project we aimed to study it expressed through the social media usage and its affects on academic studies.

        The data was collected from an online survey where a random sample of $623$ students from the ***University of Professional studies,*** *Ghana in 2021*.

        The visualisations show the relationship between students academic performance expressed via `GPA` (grade point average) and **4 related social media usage metrics** (see table on the right).
        """
        st.markdown(text)
        # st.write(f'<p>{text}</p>', unsafe_allow_html=True)

    # [Right] Feature descriptions
    with col2:
        data = {
            'Features': ['Time', 'Groups', 'Friends', 'Notifications'],
            'Description': ['refers to average number of hours a student spends daily on social media', 'represents to the number of social media groups a student belongs to', 'is the number of social media friends a student has', 'the average number of times each student checks his phone notifications per day'],
        }
        df = pd.DataFrame(data)
        st.write(f'<h3>Dataset Description</h3>', unsafe_allow_html=True)
        st.table(df)

    st.write(f'<h2>Target Audiance</h2><center>Students</center>', unsafe_allow_html=True)

def main():
    # Set the background color to a light gray
    st.set_page_config(page_title="Hello",
                  page_icon="👋🏻",
                  layout="wide")
    data = load_data(r'SM_Survey_UPSA-2020.csv')

    display_homepage()
  
if __name__ == '__main__':
    main()