import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

def load_data(file_path):
    with open(file_path, 'r') as file:
        return pd.DataFrame(json.load(file))

def load_volume_info():
    volume_info = [
        {"volume_id": 1, "month": 1, "month_str": "January", "year": 2010},
        {"volume_id": 2, "month": 4, "month_str": "April", "year": 2010},
        {"volume_id": 3, "month": 8, "month_str": "August", "year": 2010},
        {"volume_id": 4, "month": 1, "month_str": "January", "year": 2011},
        {"volume_id": 5, "month": 7, "month_str": "July", "year": 2011},
        {"volume_id": 6, "month": 3, "month_str": "March", "year": 2012},
        {"volume_id": 7, "month": 10, "month_str": "October", "year": 2012},
        {"volume_id": 8, "month": 5, "month_str": "May", "year": 2013},
        {"volume_id": 9, "month": 1, "month_str": "January", "year": 2014},
        {"volume_id": 10, "month": 7, "month_str": "July", "year": 2014},
        {"volume_id": 11, "month": 1, "month_str": "January", "year": 2015},
        {"volume_id": 12, "month": 5, "month_str": "May", "year": 2015},
        {"volume_id": 13, "month": 11, "month_str": "November", "year": 2015},
        {"volume_id": 14, "month": 4, "month_str": "April", "year": 2016},
        {"volume_id": 15, "month": 11, "month_str": "November", "year": 2016},
        {"volume_id": 16, "month": 3, "month_str": "March", "year": 2017},
        {"volume_id": 17, "month": 11, "month_str": "November", "year": 2017},
        {"volume_id": 18, "month": 5, "month_str": "May", "year": 2018},
        {"volume_id": 19, "month": 11, "month_str": "November", "year": 2018},
        {"volume_id": 20, "month": 4, "month_str": "April", "year": 2019},
        {"volume_id": 21, "month": 11, "month_str": "November", "year": 2019},
        {"volume_id": 22, "month": 5, "month_str": "May", "year": 2020},
        {"volume_id": 23, "month": 10, "month_str": "October", "year": 2020},
        {"volume_id": 24, "month": 4, "month_str": "April", "year": 2021},
        {"volume_id": 25, "month": 10, "month_str": "October", "year": 2021},
        {"volume_id": 26, "month": 3, "month_str": "March", "year": 2022},
        {"volume_id": 27, "month": 10, "month_str": "October", "year": 2022},
        {"volume_id": 28, "month": 4, "month_str": "April", "year": 2023},
        {"volume_id": 29, "month": 9, "month_str": "September", "year": 2023},
        {"volume_id": 30, "month": 4, "month_str": "April", "year": 2024}
    ]
    return pd.DataFrame(volume_info)

def filter_data(df, start_volume, end_volume):
    return df[(df['volume'] >= start_volume) & (df['volume'] <= end_volume)]

def display_title_and_description(start_volume, end_volume, volume_info):
    start_info = volume_info[volume_info['volume_id'] == start_volume].iloc[0]
    end_info = volume_info[volume_info['volume_id'] == end_volume].iloc[0]
    st.title('Thoughtworks Technology Radar Analysis')
    st.write(f'This app analyzes technologies from the Thoughtworks Technology Radar, focusing on volumes {start_volume} ({start_info["month_str"]} {start_info["year"]}) to {end_volume} ({end_info["month_str"]} {end_info["year"]}).')

def display_interactive_table(df):
    st.subheader(f'Technologies')
    
    filters = {
        "Quadrants": 'quadrant',
        "Rings": 'ring',
        "New Technologies": 'isNew'
    }
    
    filtered_df = df.copy()
    
    for filter_name, column in filters.items():
        options = filtered_df[column].unique()
        selected = st.sidebar.multiselect(f"Select {filter_name}", options=options, default=options)
        filtered_df = filtered_df[filtered_df[column].isin(selected)]
    
    st.dataframe(filtered_df[['name', 'ring', 'quadrant', 'isNew', 'volume']], use_container_width=True)

def display_volume_statistics(df, volume_info):
    st.subheader('Statistics by Volume')
    with st.expander(f"Volume Statistics"):
        for volume in df['volume'].unique():
            df_volume = df[df['volume'] == volume]
            volume_data = volume_info[volume_info['volume_id'] == volume].iloc[0]
            st.write(f"Volume {volume} ({volume_data['month_str']} {volume_data['year']}):")
            st.write(f"- Total technologies: {len(df_volume)}")
            st.write(f"- New technologies: {df_volume['isNew'].value_counts().get('TRUE', 0)}")

def create_chart(df, group_by, title, chart_type='bar'):
    counts = df.groupby(['volume', group_by]).size().unstack(fill_value=0)
    if chart_type == 'bar':
        fig = px.bar(counts, barmode='group', title=title,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    elif chart_type == 'stack':
        fig = px.bar(counts, barmode='stack', title=title,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig)

def create_new_vs_existing_chart(df):
    new_vs_existing = df.groupby('volume')['isNew'].value_counts().unstack(fill_value=0)
    new_vs_existing.columns = ['Existing', 'New']
    new_vs_existing.reset_index(inplace=True)
    
    fig = go.Figure()
    
    for category in ['Existing', 'New']:
        fig.add_trace(go.Scatter(
            x=new_vs_existing['volume'],
            y=new_vs_existing[category],
            mode='lines+markers',
            name=category,
            line=dict(color='#FFB3BA' if category == 'Existing' else '#BAFFC9', width=2),
            marker=dict(size=10, color='#FFB3BA' if category == 'Existing' else '#BAFFC9', symbol='circle')
        ))
    
    fig.update_layout(
        title='New vs. Existing Technologies by Volume',
        xaxis_title='Volume',
        yaxis_title='Count',
        legend_title='Technology Type'
    )
    
    st.plotly_chart(fig)

def create_cumulative_new_vs_total_chart(df):
    new_vs_total = df.groupby('volume').agg({
        'isNew': lambda x: (x == 'TRUE').sum(),
        'name': 'count'
    }).reset_index()
    
    new_vs_total.columns = ['volume', 'New', 'Total']
    new_vs_total['Cumulative New'] = new_vs_total['New'].cumsum()
    new_vs_total['Cumulative Total'] = new_vs_total['Total'].cumsum()
    
    fig = go.Figure()
    
    # Add area traces for cumulative data
    fig.add_trace(go.Scatter(
        x=new_vs_total['volume'],
        y=new_vs_total['Cumulative Total'],
        fill='tozeroy',
        name='Total',
        line=dict(color='#FFB3BA', width=0),
        fillcolor='rgba(255, 179, 186, 0.5)'
    ))
    
    fig.add_trace(go.Scatter(
        x=new_vs_total['volume'],
        y=new_vs_total['Cumulative New'],
        fill='tozeroy',
        name='New',
        line=dict(color='#BAFFC9', width=0),
        fillcolor='rgba(186, 255, 201, 0.5)'
    ))
    
    # Add line traces for non-cumulative data
    fig.add_trace(go.Scatter(
        x=new_vs_total['volume'],
        y=new_vs_total['Total'],
        mode='lines',
        name='Total (per volume)',
        line=dict(color='#FF6B6B', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=new_vs_total['volume'],
        y=new_vs_total['New'],
        mode='lines',
        name='New (per volume)',
        line=dict(color='#4ECDC4', width=2)
    ))
    
    fig.update_layout(
        title='Cumulative and Per-Volume New vs. Total Technologies',
        xaxis_title='Volume',
        yaxis_title='Count',
        legend_title='Technology Type',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig)

def display_conclusion(start_volume, end_volume, volume_info):
    start_info = volume_info[volume_info['volume_id'] == start_volume].iloc[0]
    end_info = volume_info[volume_info['volume_id'] == end_volume].iloc[0]
    st.subheader('Conclusion')
    st.write(f'This analysis provides insights into the technology trends across volumes {start_volume} ({start_info["month_str"]} {start_info["year"]}) to {end_volume} ({end_info["month_str"]} {end_info["year"]}) of the Thoughtworks Technology Radar. It highlights the distribution of technologies across different quadrants and rings, as well as the introduction of new technologies in each volume.')

def display_occurrences(df):
    st.subheader(f'List of Technology Occurrences')
    
    tech_info = df.groupby('name').agg({
        'volume': 'first',
        'ring': 'last'
    }).reset_index()
    
    occurrences = df['name'].value_counts().reset_index()
    occurrences.columns = ['Technology', 'Occurrences']
    
    tech_details = occurrences.merge(tech_info, left_on='Technology', right_on='name')
    
    default_value = 2 if len(tech_details) > 1 else 1
    
    min_occurrences = st.slider('Minimum Occurrences', 
                                min_value=1, 
                                max_value=int(tech_details['Occurrences'].max()), 
                                value=default_value)
    
    filtered_tech_details = tech_details[tech_details['Occurrences'] >= min_occurrences]
    
    display_df = filtered_tech_details[['Technology', 'Occurrences', 'volume', 'ring']]
    display_df.columns = ['Technology', 'Occurrences', 'First Occurrence Volume', 'Latest Ring']
    
    st.dataframe(display_df)

def display_author_info():
    st.sidebar.markdown("")
    st.sidebar.subheader("Author")
    st.sidebar.info(
        "This app was created by Muhammed Kılıç.\n\n"
        "Prepared for the 8th Devnot Developer Summit on October 12, 2024\n\n"
        "[summit.muhammedkilic.com](https://summit.muhammedkilic.com/)\n\n"
        "Learn more at [summit.devnot.com](https://summit.devnot.com/)\n\n"
        "Contact me:\n\n"
        "Website: [muhammedkilic.com](https://muhammedkilic.com)\n\n"
        "[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/muhammedkilic/)\n\n"
        "[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/kiliczsh)\n\n"
        "[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/kiliczsh)"
    )

def select_volume_range(volume_info):
    st.sidebar.header('Volume Range Selection')
    volume_options = [f'Volume {row["volume_id"]} ({row["month_str"]} {row["year"]})' for _, row in volume_info.iterrows()]
    start_volume = st.sidebar.selectbox('Start Volume', volume_options, index=27)
    end_volume = st.sidebar.selectbox('End Volume', volume_options, index=29)
    
    start_volume_id = int(start_volume.split()[1].split('(')[0])
    end_volume_id = int(end_volume.split()[1].split('(')[0])
    
    return start_volume_id, end_volume_id

def main():
    df = load_data('data.json')
    volume_info = load_volume_info()
    display_author_info()
    
    start_volume, end_volume = select_volume_range(volume_info)
    
    if start_volume > end_volume:
        st.error('Start volume cannot be greater than end volume. Please adjust your selection.')
        return
    
    df_filtered = filter_data(df, start_volume, end_volume)

    display_title_and_description(start_volume, end_volume, volume_info)
    display_interactive_table(df_filtered)
    display_volume_statistics(df_filtered, volume_info)
    create_chart(df_filtered, 'quadrant', 'Technologies by Quadrant and Volume')
    create_chart(df_filtered, 'ring', 'Technologies by Ring and Volume', 'stack')
    create_new_vs_existing_chart(df_filtered)
    create_cumulative_new_vs_total_chart(df_filtered)
    display_occurrences(df_filtered)
    display_conclusion(start_volume, end_volume, volume_info)

if __name__ == "__main__":
    main()
