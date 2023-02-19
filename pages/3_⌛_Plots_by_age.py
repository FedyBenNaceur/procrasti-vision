import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




def lineplot():
    df = pd.read_csv('SM_Survey_UPSA-2020_clean.csv')

    st.markdown("## Relation between social media usage and grades by Age groups \n - How to read the visualization: The visualization represents the grade point average (GPA) of students according to 3 age groups and social media usage metrics. We can see what is the mostly negative correlations between the chosen metric and the GPA of students for all groups.")   ## Main Title
        ##############################



    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(ncols=2,nrows=2, figsize=(10, 6)) #, figsize=(10, 10)
    
    sns.lineplot(ax=ax1, data=df, x="Time", y="GPA", hue="Age Group", style="Age Group", ci=None)
    sns.lineplot(ax=ax2, data=df, x="Groups", y="GPA", hue="Age Group",style="Age Group", ci=None)
    ax1.set_title("Time vs GPA")
    ax1.set_xlim(1,5)
    ax1.set_ylim(1,4)
    ax1.legend(loc=3, prop={'size': 6})
    ax2.set_title("Groups vs GPA")
    ax2.set_xlim(0,6)
    ax2.set_ylim(1,4)
    ax2.legend(loc=3, prop={'size': 6})

    sns.lineplot(ax=ax3, data=df, x="Friends", y="GPA", hue="Age Group",style="Age Group", ci=None)
    sns.lineplot(ax=ax4, data=df, x="Notifications", y="GPA", hue="Age Group",style="Age Group", ci=None)
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
    st.set_page_config(page_title="Line plots by Age groups",
                  page_icon="⌛",
                  layout="wide")
   
    lineplot()

        
if __name__ == '__main__':
    main()