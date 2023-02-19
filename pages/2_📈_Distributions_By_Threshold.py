import streamlit as st
import pandas as pd
import altair as alt

@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)


def plot_distributionsInteractive(data, threshold, selected_features):
    st.markdown("How to read the visualisation : The points on the chart represent students, green points are points whom GPA is above the threshold set by the user, red points are points whom GPA is under the threshold. You can select the features to display on the X axis in the sidebar where you will also be capable of modifying the threshold")
    
    charts = []
    for i, feature in enumerate(selected_features):
        # Create a dataframe for the current feature
        feature_data = data[[feature, 'GPA']].copy()
        
        # Create a column to distinguish between over and under threshold data points
        feature_data['Threshold'] = feature_data['GPA'] >= threshold

        # Create a chart showing all data points with color determined by threshold
        chart = alt.Chart(feature_data).mark_circle().encode(
            x=alt.X(feature, title=feature, scale=alt.Scale(zero=False)),
            y=alt.Y('GPA', title='GPA', scale=alt.Scale(zero=False)),
            color=alt.Color('Threshold:N', scale=alt.Scale(domain=[True, False], range=['green', 'red'])),
            tooltip=feature_data.columns.tolist()
        ).properties(
            width=600,
            height=600
        ).interactive()

        # Add the chart to the list of charts
        charts.append(chart)

    # Combine the charts into a vertical grid layout with two columns
    num_charts = len(charts)
    num_rows = (num_charts + 1) // 2
    grid = []
    for i in range(num_rows):
        row = charts[i*2:(i+1)*2]
        grid.append(alt.hconcat(*row))
    combined_chart = alt.vconcat(*grid)

    # Apply the 'fivethirtyeight' theme
    alt.themes.enable('fivethirtyeight')

    container = st.container()


    # Display the combined chart

    container.altair_chart(combined_chart, use_container_width=True)

    col1, col2 = container.columns(2)
    col1.write('**Students over the GPA threshold**')
    col1.dataframe(data[data['GPA'] >= threshold])
    col2.write('**Students under the GPA threshold**')
    col2.dataframe(data[data['GPA'] < threshold])

    footer_container = st.container()

    # Add CSS to the footer to make it fixed to the bottom right corner
    st.write(
        '<style>.footer {position: fixed; left: auto; right: 0; bottom: 0; width: 100%; text-align: right; background-color: lightgray;}</style>',
        unsafe_allow_html=True
    )

    # Apply the 'footer' class to the footer container
    footer_container.markdown(
        '<div class="footer" style="color: black;">GPA : GRADE POINT AVERAGE, grading system used in some anglophone countries ex : USA, Ghana ..  </div>',
        unsafe_allow_html=True
    ) 
    
def main():
    st.set_page_config(page_title ="Differences between students with high and low grades",
                  page_icon="📈",
                  layout="wide")
    data = load_data(r'SM_Survey_UPSA-2020.csv')  
    feature_columns = list(data.columns)
    st.sidebar.header("Settings")
    selected_features = st.sidebar.multiselect('Select features to display', feature_columns, default=['Time', 'Groups'])
    threshold = st.sidebar.slider('GPA threshold', min_value=data['GPA'].min(), max_value=data['GPA'].max(), value=2.0, step=0.1)

    plot_distributionsInteractive(data, threshold, selected_features)
        
if __name__ == '__main__':
    main()