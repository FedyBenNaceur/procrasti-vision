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
         # Calculate the mean values for each dataset
        above_mean = high_gpa[x_col].mean()
        below_mean = low_gpa[x_col].mean()

        sns.kdeplot(high_gpa[x_col], ax=ax[0][i], color="g")
        ax[0][i].axvline(above_meanabove_mean, color="g", linestyle="dashed", linewidth=2)
        ax[0][i].set_title("Students with GPA over " + str(gpa_threshold))
        ax[0][i].set_xlabel(x_col)
        ax[0][i].set_ylabel("Density")

        sns.kdeplot(low_gpa[x_col], ax=ax[1][i], color="r")
        ax[1][i].axvline(below_mean, color="r", linestyle="dashed", linewidth=2)
        ax[1][i].set_title("Students with GPA under " + str(gpa_threshold))
        ax[1][i].set_xlabel(x_col)
        ax[1][i].set_ylabel("Density")

    return f

def plot_distributionsInteractive(data, gpa_threshold, x_cols, stuck=True, y_col=None):
    st.markdown("How to read the visualisation : The plots shown below are kernel density plots, the line in the middle indicated the mean value for the corresponding group of people. Plots in green correspond to the group of people having a GPA over a certain threshold that can be modified using the slider in the sidebar. A selector is also available to choose features of the dataset to display.")
    
    # Add a new column indicating whether the value is above or below the threshold
    data_copied = data.copy()
    data_copied['group'] = ['above' if x > gpa_threshold else 'below' for x in data_copied['GPA']]


    # For every selected column
    for i, x_col in enumerate(x_cols):
        # Calculate the mean values for each dataset (above/under)
        above_threshold = data_copied[data_copied['group'] == 'above']
        below_threshold = data_copied[data_copied['group'] == 'below']

        above_mean = above_threshold[x_col].mean()
        below_mean = below_threshold[x_col].mean()
        
        if (stuck==False):
            # Define the density plots using Density Transformers
            left_density = alt.Chart(above_threshold).transform_density(
                x_col,
                as_=[x_col, 'density']
            ).mark_area(opacity=0.5, color='#98df8a').encode(
                x=x_col+':Q',
                y='density:Q',
                tooltip='density:Q'
            )

            right_density = alt.Chart(below_threshold).transform_density(
                x_col,
                as_=[x_col, 'density']
            ).mark_area(opacity=0.5, color='#ffbb78').encode(
                x=x_col+':Q',
                y='density:Q',
                tooltip='density:Q'
            )

            # Add vertical lines for the mean values to each density plot
            left_mean = alt.Chart(pd.DataFrame({'mean': [above_mean]})).mark_rule(color='red').encode(
                x='mean:Q'
            )

            right_mean = alt.Chart(pd.DataFrame({'mean': [below_mean]})).mark_rule(color='red').encode(
                x='mean:Q'
            )

            # Combine the two density plots and mean lines side-by-side
            densities = alt.hconcat(
                left_density + left_mean,
                right_density + right_mean,
                spacing=10
            )
            # Render the density plots using Streamlit
            st.altair_chart(densities, use_container_width=True)
        else:
            # Define the density plot using Density Transformers
            density = alt.Chart(data_copied).transform_density(
                x_col,
                groupby=['group'],
                as_=[x_col, 'density']
            ).mark_area(opacity=0.5).encode(
                x=alt.X(x_col+':Q', scale=alt.Scale(zero=False, nice=False)),
                y=alt.Y('density:Q', scale=alt.Scale(zero=False, nice=False)),
                color=alt.Color('group:N', scale=alt.Scale(domain=['above', 'below'], range=['#98df8a', '#ffbb78'])),
                tooltip='density:Q'
            )

            # Add vertical lines for the mean values to the density plot
            above_mean_line = alt.Chart(pd.DataFrame({'mean': [above_mean], 'group': ['above']})).mark_rule(color='red').encode(
                x=alt.X('mean:Q'),
                color=alt.Color('group:N', scale=alt.Scale(domain=['above', 'below'], range=['#98df8a', '#ffbb78'])),
            )

            below_mean_line = alt.Chart(pd.DataFrame({'mean': [below_mean], 'group': ['below']})).mark_rule(color='red').encode(
                x=alt.X('mean:Q'),
                color=alt.Color('group:N', scale=alt.Scale(domain=['above', 'below'], range=['#98df8a', '#ffbb78'])),
            )

            # Combine the density plot and mean lines into a single plot
            plot = (density + above_mean_line + below_mean_line).properties(
                width=300,
                height=400,
                title='Density plot of col'
            )
            # Render the plot using Streamlit
            st.altair_chart(plot, use_container_width=True) 

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
        units = {'Time': 'Hour(s)', 'Notifications': 'Number', 'Friends': 'Number', 'Groups':'Number'}

        # Names of variables we will use
        x_axis = 'Mean'
        y_axis = st.sidebar.selectbox("Y-Axis", measurements, index=measurements.index('Time'))

        # Gender colors
        dom = ['Men', 'Women']
        rng = ['lightblue', 'hotpink']

        ### Get counts
        counts = data.groupby([y_axis, 'Gender']).count()
        # Drop gender = 3 (multi index dataframe)
        counts = counts.drop(index=3, level=1)
        # Transformes indices to columns
        counts = counts.reset_index(names=[y_axis, 'Gender'])

        ### Get other statistics
        # Group by measure given and gender 
        statistics = data.groupby([y_axis, 'Gender']).agg(Mean=('GPA', np.mean), 
                                                 Sum=('GPA', np.sum), 
                                                 Std=('GPA', np.std),
                                                 Max=('GPA', np.max),
                                                 Min=('GPA', np.min))
        statistics = statistics.drop(index=3, level=1).reset_index(names=[y_axis, 'Gender']).drop(columns=['Gender', y_axis])

        source = pd.concat([counts, statistics], axis=1)

        source.replace({'Gender': 1}, 'Men', inplace=True)
        source.replace({'Gender': 2}, 'Women', inplace=True)

        print(source)
        ### Chart of circles
        circles = alt.Chart(source).mark_circle(size=300).encode(
            x=alt.X(x_axis, title='GPA', axis=alt.Axis(orient='top')),
            y=alt.Y(y_axis, 
                    title = y_axis + '  -  ' + units[y_axis] , 
                    scale=alt.Scale(zero=False, padding=1, domain=[max(source[y_axis]), min(source[y_axis])])),
            color=alt.Color('Gender', scale=alt.Scale(domain=dom, range=rng), legend=alt.Legend(type="symbol"))
        ).encode(tooltip=['Mean', 'Std', 'Max', 'Min']
        ).interactive()

        ### Chart of lines
        gpa_mean = source.groupby(by=[y_axis]).mean()


        source_men = source.copy()
        source_woman = source.copy()

        for index, row in source_men.iterrows():
            if row['Gender'] == 'Women': # Replace values of women by the mean
                source_men.at[index, x_axis] = gpa_mean.loc[int(row[y_axis])][x_axis] 
            if row['Gender'] == 'Men':  # Replace values of men by the mean
                source_woman.at[index, x_axis] = gpa_mean.loc[int(row[y_axis])][x_axis] 
    
        # Blue lines
        lines_men = alt.Chart(source_men).mark_line().encode(
            x=x_axis,
            y=y_axis,
            detail=y_axis,
            color=alt.value('lightblue')
        )
        # Pink lines
        lines_women = alt.Chart(source_woman).mark_line().encode(
            x=x_axis,
            y=y_axis,
            detail=y_axis,
            color=alt.value('hotpink')
        )

        ### Mean GPA
        gpa = alt.Chart(gpa_mean.reset_index()).mark_circle().encode(
            x=x_axis,
            y=y_axis,
            color=alt.value('purple')
        ).encode(tooltip=['Mean']
        ).interactive()

        # Plot charts
        st.altair_chart(circles + lines_men + lines_women + gpa, theme="streamlit", use_container_width=True)

def aleksandra_plot():
    df = pd.read_csv('SM_Survey_UPSA-2020_clean.csv')
    st.header("Academic performance, GPA, and 4 related social media usage metrics :tada:")
    st.markdown("- How the user can see the comparison of GPA and 4 related social media usage metrics: Time, Groups, Friends, Notifications by Gender and different Age groups. \n \t For example, one can see that the more students spend time browsing media - the smaller GPA they have.\n \t In addition, in the first part we can observe the differences for males and females, and below we can see the differences for the three age groups.")
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
    # Set the background color to a light gray
    st.set_page_config(page_title="Procrasti-vision",
                  page_icon=":guardsman:",
                  layout="wide")
    data = load_data(r'SM_Survey_UPSA-2020.csv')
    # selected_tab = st.sidebar.radio("Menu", ["Description","Distribution plots", "Gender pie plots", "Scatter plot variation", ])
    selected_tab = st.sidebar.radio("Menu", ["Description","Distribution plots", "Scatter plot variation", "Evolution Plots"])
   
    if selected_tab == "Distribution plots":
        st.sidebar.header("Settings")
        gpa_threshold = st.sidebar.slider("GPA Threshold", 0.0, 4.0, 2.5)
        stuck = st.checkbox("Stuck Plots!", value=False, key="switch")
        x_cols = st.sidebar.multiselect("X Axes", data.columns, default=["Time", "Friends"])
        y_col = None
        st.write("Displaying social media usage distributions for students with GPA higher and lower than the threshold")
        plot_distributionsInteractive(data, gpa_threshold, x_cols , stuck, y_col)
        
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