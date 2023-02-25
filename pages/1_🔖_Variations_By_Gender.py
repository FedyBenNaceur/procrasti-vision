import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def load_data(file_path):
    return pd.read_csv(file_path)


def plot_scatter(data): 
        st.markdown("## Correlation between social media usage and grades \n - How to read the visualization: The visualization represent the grade point average (GPA) of students according to their genders and social media usage metrics. You can choose between the 4 metrics described previously. We can see what is the correlation (if there is one) between the chosen metric and the GPA of students (their academic performance).")   ## Main Title
        ##############################

        # Selector
        measurements = ['Time', 'Notifications', 'Friends', 'Groups']
        units = {'Time': 'Hour(s)', 'Notifications': 'Number', 'Friends': 'Number', 'Groups':'Number'}

        # Names of variables we will use
        x_axis = 'Mean'
        st.sidebar.header("Settings")
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
        source.rename(columns={"GPA": "Count"}, inplace=True)

        print(source)
        ### Chart of circles
        circles = alt.Chart(source).mark_circle().encode(
            x=alt.X(x_axis, title='GPA', axis=alt.Axis(orient='top')),
            y=alt.Y(y_axis, 
                    title = y_axis + '  -  ' + units[y_axis] , 
                    scale=alt.Scale(zero=False, padding=1, domain=[max(source[y_axis]), min(source[y_axis])])),
            color=alt.Color('Gender', scale=alt.Scale(domain=dom, range=rng), legend=alt.Legend(type="symbol")),
            size=alt.Size('Count')
        ).encode(tooltip=['Mean', 'Std', 'Max', 'Min', 'Count']
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
def main():
    st.set_page_config(page_title="Scatter Variations By Gender",
                  page_icon="🔖",
                  layout="wide")
    data = load_data(r'data/SM_Survey_UPSA-2020.csv')        
    plot_scatter(data)

        
if __name__ == '__main__':
    main()