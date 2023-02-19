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
        ## What is the **correlation/relationship** between social media usage and students’ academic performance ?

        This visualisation shows the relationship between students academic performance expressed via `GPA` (grade point average) and 4 related `social media usage metrics`: 
        - **Time** refers to average number of hours a student spends daily on social media,
        - **Groups** represents to the number of social media groups a student belongs to,
        - **Freinds** is the number of social media friends a student has,
        - **Notifications** - the average number of times each student checks his phone notifications per day.

        **WHAT** the visualizations show;
        It is the result of an online survey where a random sample of 623 students was asked to self-reflect about
        their usage of social media, so Mohammed Nurudeen and his team could measure the effect of social media on
        academic performance. This application of social media may have some benefits for students’ academic performance.
        Nonetheless, social media may have an addicting effect that could lead to several things including
        poor health, poor concentration in class, poor time management, lack of appetite for learning, procrastination
        and consequently poor academic performance.

        **WHO** the visualization is for: parents, teachers and students.

        **WHY** we the audience should care about it: while striving for performance one needs to decrease the potential non productive time.

        """)
  
if __name__ == '__main__':
    main()