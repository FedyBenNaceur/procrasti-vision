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

def plot_distributions(data, gpa_threshold, x_cols, y_col=None):
    st.markdown("How to read the visualisation : The plots shown below are kernel density plots, the line in the middle indicated the mean value for the corresponding group of people. Plots in green correspond to the group of people having a GPA over a certain threshold that can be modified using the slider in the sidebar. A selector is also available to choose features of the dataset to display.")
    sns.set_style("darkgrid")

    high_gpa = data[data["GPA"] >= gpa_threshold]
    low_gpa = data[data["GPA"] < gpa_threshold]

    n = len(x_cols)
    f, ax = plt.subplots(2, n, figsize=(n*5, 10))

    for i, x_col in enumerate(x_cols):
        sns.kdeplot(high_gpa[x_col], ax=ax[0][i], color="g")
        ax[0][i].axvline(high_gpa[x_col].mean(), color="g", linestyle="dashed", linewidth=2)
        ax[0][i].set_title("Students with GPA over " + str(gpa_threshold))
        ax[0][i].set_xlabel(x_col)
        ax[0][i].set_ylabel("Density")

        sns.kdeplot(low_gpa[x_col], ax=ax[1][i], color="r")
        ax[1][i].axvline(low_gpa[x_col].mean(), color="r", linestyle="dashed", linewidth=2)
        ax[1][i].set_title("Students with GPA under " + str(gpa_threshold))
        ax[1][i].set_xlabel(x_col)
        ax[1][i].set_ylabel("Density")

    return f


def plot_gender_distribution(data, gpa_threshold):
    high_gpa = data[data["GPA"] >= gpa_threshold]
    low_gpa = data[data["GPA"] < gpa_threshold]

    high_gpa_counts = high_gpa["Gender"].value_counts()
    low_gpa_counts = low_gpa["Gender"].value_counts()

    f, ax = plt.subplots(1, 2, figsize=(10, 5))

    high_gpa_counts.plot.pie(ax=ax[0], autopct="%.1f%%")
    ax[0].set_title("Students with GPA over " + str(gpa_threshold))

    low_gpa_counts.plot.pie(ax=ax[1], autopct="%.1f%%")
    ax[1].set_title("Students with GPA under " + str(gpa_threshold))

    return f

def plot_Lili(data): 
        st.markdown("## Correlation between social media usage and grades \n - How to read the visualization: The visualization represent the grade point average (GPA) of students according to their genders and social media usage metrics. You can choose between the 4 metrics described previously. We can see what is the correlation (if there is one) between the chosen metric and the GPA of students (their academic performance).")   ## Main Title
        ##############################

        # Selector
        measurements = ['Time', 'Notifications', 'Friends', 'Groups']

        # Names of variables we will use
        x_axis = 'GPA'
        y_axis = st.sidebar.selectbox("Y-Axis", measurements, index=measurements.index('Time'))

        # Group by measure given and gender
        sm_grouped = data.groupby([y_axis, 'Gender']).mean()
        # Drop gender = 3 (multi index dataframe)
        sm_grouped = sm_grouped.drop(index=3, level=1).head(15)
        # Transformes indices to columns
        source = sm_grouped.reset_index(names=[y_axis, 'Gender'])

        # Gender colors
        dom = [1, 2]
        rng = ['lightblue', 'hotpink']

        # Chart of circles
        circles = alt.Chart(source).mark_circle(size=200).encode(
            x=alt.X(x_axis, axis=alt.Axis(orient='top')),
            y=alt.Y(y_axis, scale=alt.Scale(zero=False, padding=1, domain=[min(source[y_axis]),max(source[y_axis])])),
            color=alt.Color('Gender', scale=alt.Scale(domain=dom, range=rng))
        ).interactive()

        # Chart of lines
        lines = alt.Chart(source).mark_line().encode(
            x=x_axis,
            y=y_axis,
            detail=y_axis
        )
        # Plot both charts
        st.altair_chart(circles + lines, theme="streamlit", use_container_width=True)

def aleksandra_plot():
    df = pd.read_csv('SM_Survey_UPSA-2020_clean.csv')
    st.header("Academic performance, GPA, and 4 related social media usage metrics :tada:")
    st.subheader("By Genders")
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(ncols=2,nrows=2, figsize=(10, 6)) #, figsize=(10, 10)
 
    sns.lineplot(ax=ax1, data=df, x="Time", y="GPA", hue="Gender",style="Gender")
    sns.lineplot(ax=ax2, data=df, x="Groups", y="GPA", hue="Gender",style="Gender")
    ax1.set_title("Time vs GPA")
    ax1.set_xlim(1,5)
    ax1.set_ylim(1,4)
    ax1.legend(loc=3, prop={'size': 6})
    ax2.set_title("Groups vs GPA")
    ax2.set_xlim(0,6)
    ax2.set_ylim(1,4)
    ax2.legend(loc=3, prop={'size': 6})

    sns.lineplot(ax=ax3, data=df, x="Friends", y="GPA", hue="Gender",style="Gender")
    sns.lineplot(ax=ax4, data=df, x="Notifications", y="GPA", hue="Gender",style="Gender")
    ax3.set_title("Friends vs GPA")
    ax3.set_xlim(1000,4000)
    ax3.set_ylim(1,4)
    ax3.legend(loc=3, prop={'size': 6})
    ax4.set_xlim(5,50)
    ax4.set_ylim(1,4)
    ax4.legend(loc=3, prop={'size': 6})
    ax4.set_title("Notifications vs GPA")

    fig.set_tight_layout(True)
    st.pyplot(fig)

    st.subheader("By Age groups")

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(ncols=2,nrows=2, figsize=(10, 6)) #, figsize=(10, 10)
    
    sns.lineplot(ax=ax1, data=df, x="Time", y="GPA", hue="Age Group", style="Age Group")
    sns.lineplot(ax=ax2, data=df, x="Groups", y="GPA", hue="Age Group",style="Age Group")
    ax1.set_title("Time vs GPA")
    ax1.set_xlim(1,5)
    ax1.set_ylim(1,4)
    ax1.legend(loc=3, prop={'size': 6})
    ax2.set_title("Groups vs GPA")
    ax2.set_xlim(0,6)
    ax2.set_ylim(1,4)
    ax2.legend(loc=3, prop={'size': 6})

    sns.lineplot(ax=ax3, data=df, x="Friends", y="GPA", hue="Age Group",style="Age Group")
    sns.lineplot(ax=ax4, data=df, x="Notifications", y="GPA", hue="Age Group",style="Age Group")
    ax3.set_title("Friends vs GPA")
    ax3.set_xlim(1000,4000)
    ax3.set_ylim(1,4)
    ax3.legend(loc=3, prop={'size': 6})
    ax4.set_xlim(5,50)
    ax4.set_ylim(1,4)
    ax4.legend(loc=3, prop={'size': 6})
    ax4.set_title("Notifications vs GPA")

    fig.set_tight_layout(True)
    return fig

def main():
    st.set_page_config(page_title="Procrasti-vision",
                  page_icon=":guardsman:",
                  layout="wide")
    data = load_data(r'SM_Survey_UPSA-2020.csv')
    # selected_tab = st.sidebar.radio("Menu", ["Description","Distribution plots", "Gender pie plots", "Scatter plot variation", ])
    selected_tab = st.sidebar.radio("Menu", ["Description","Distribution plots", "Scatter plot variation", "Evolution Plots"])
   
    if selected_tab == "Distribution plots":
        st.sidebar.header("Settings")
        gpa_threshold = st.sidebar.slider("GPA Threshold", 0.0, 4.0, 2.5)

        x_cols = st.sidebar.multiselect("X Axes", data.columns, default=["Time", "Friends"])
        y_col = None
        st.write("Displaying social media usage distributions for students with GPA higher and lower than the threshold")
        f = plot_distributions(data, gpa_threshold, x_cols, y_col)
        st.pyplot(f)
    # elif selected_tab == "Gender pie plots":
    #     st.sidebar.header("Settings")
    #     gpa_threshold = st.sidebar.slider("GPA Threshold", 0.0, 4.0, 2.5)
    #     g = plot_gender_distribution(data, gpa_threshold)
    #     st.pyplot(g)
    elif selected_tab == "Scatter plot variation":
        st.sidebar.header("Settings")
        plot_Lili(data)
    elif selected_tab == 'Evolution Plots':
        f = aleksandra_plot()
        st.pyplot(f)

    elif selected_tab == 'Description':

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