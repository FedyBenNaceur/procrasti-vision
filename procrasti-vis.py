import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

import seaborn as sns

@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

def plot_distributions(data, gpa_threshold, x_cols, y_col=None):
    sns.set_style("darkgrid")

    high_gpa = data[data["GPA"] >= gpa_threshold]
    low_gpa = data[data["GPA"] < gpa_threshold]

    n = len(x_cols)
    f, ax = plt.subplots(2, n, figsize=(n*5, 10))

    for i, x_col in enumerate(x_cols):
        sns.kdeplot(high_gpa[x_col], ax=ax[0][i], color="g")
        ax[0][i].axvline(high_gpa[x_col].mean(), color="g", linestyle="dashed", linewidth=2)
        ax[0][i].set_title("High GPA Students")
        ax[0][i].set_xlabel(x_col)
        ax[0][i].set_ylabel("Density")

        sns.kdeplot(low_gpa[x_col], ax=ax[1][i], color="r")
        ax[1][i].axvline(low_gpa[x_col].mean(), color="r", linestyle="dashed", linewidth=2)
        ax[1][i].set_title("Low GPA Students")
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
    ax[0].set_title("High GPA Students")

    low_gpa_counts.plot.pie(ax=ax[1], autopct="%.1f%%")
    ax[1].set_title("Low GPA Students")

    return f

def main():
    st.set_page_config(page_title="Procrasti-vision",
                  page_icon=":guardsman:",
                  layout="wide")
    data = load_data(r'SM_Survey_UPSA-2020.csv')
    selected_tab = st.sidebar.radio("Plots", ["Distribution plots", "Gender pie plots"])
    st.sidebar.header("Settings")
    gpa_threshold = st.sidebar.slider("GPA Threshold", 0.0, 4.0, 2.5)
    if selected_tab == "Distribution plots":

        x_cols = st.sidebar.multiselect("X Axes", data.columns, default=["Time", "Friends"])
        y_col = None
        st.write("Displaying social media usage distributions for students with GPA higher and lower than the threshold")
        f = plot_distributions(data, gpa_threshold, x_cols, y_col)
        st.pyplot(f)
    elif selected_tab == "Gender pie plots":
        g = plot_gender_distribution(data, gpa_threshold)
        st.pyplot(g)

if __name__ == '__main__':
    main()