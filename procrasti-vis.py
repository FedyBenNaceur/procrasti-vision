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

def main():
    # Set the background color to a light gray
    st.set_page_config(page_title="Hello",
                  page_icon="👋🏻",
                  layout="wide")
    data = load_data(r'SM_Survey_UPSA-2020.csv')

    st.markdown("""
        ## Procrastination through the lenses of social media usage and students’ academic performance.

        Nowadays one strives to go faster and further, be more productive, reach higher goals. But at the same time we observe people delaying tasks, focusing on less urgent and easier ones, being easily distracted. Specially with the accessibility of Internet and medias these new habits may have an addicting effect that could lead to poor health, decreased concentration in class, bad time management, lack of appetite for learning and consequently poor academic performance. So procrastination has become an important issue in our society, and in our project we aimed to study it expressed through the social media usage and its affects on academic studies.
        

        The **data** was collected from an online survey where a random sample of 623  students from the University of Professional studies, Ghana in 2021.

        The visualisations show the relationship between students academic performance expressed via `GPA` (grade point average) and 4 related `social media usage metrics`: 
        - **Time** refers to average number of hours a student spends daily on social media,
        - **Groups** represents to the number of social media groups a student belongs to,
        - **Freinds** is the number of social media friends a student has,
        - **Notifications** - the average number of times each student checks his phone notifications per day.
        

        **WHO** the visualization is for: parents, teachers and students.

        **WHY** the audience should care about it: while striving for performance one needs to decrease the potential non productive time.

        """)
  
if __name__ == '__main__':
    main()