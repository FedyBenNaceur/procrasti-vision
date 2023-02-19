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


def plot_distributionsInteractive(data, gpa_threshold, x_cols, stack=True, y_col=None):
    st.write("Displaying social media usage distributions for students with GPA higher and lower than the threshold")
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
        
        if (stack==False):
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
def main():
    st.set_page_config(page_title="Distributions By Threshold",
                  page_icon="📈",
                  layout="wide")
    data = load_data(r'SM_Survey_UPSA-2020.csv')  
    # Use the native Altair theme.
    st.markdown("## Distribution according to given threshold")
    st.sidebar.header("Settings")
    gpa_threshold = st.sidebar.slider("GPA Threshold", 0.0, 4.0, 2.5)
    stack = st.checkbox("Stack Plots!", value=False, key="switch")

    x_cols = st.sidebar.multiselect("X Axes", data.columns, default=["Time", "Friends"])
    y_col = None
    plot_distributionsInteractive(data, gpa_threshold, x_cols , stack, y_col)
        
if __name__ == '__main__':
    main()