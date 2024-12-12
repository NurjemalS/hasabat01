import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import squarify
import seaborn as sns
from hunar_ugurlar_app import main as humarmen_main
# from squarify import normalize_sizes, squarify

# import numpy as np


page_title = "Türkmenistanda ýokary bilimi ösdürmegiň Strategiýasyny taýýarlamak üçin MAGLUMATLAR"

st.set_page_config(page_title=page_title, layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 300px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width: 300px;
        margin-left: -400px;
    }
     
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    .metric-container {
        font-size: 30px !important;  /* Adjust the font size as needed */
        font-weight: bold !important; /* Optional: Make it bold */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("Nawigasiýa")

		
page = st.sidebar.radio("Kategoriýa saýlaň", [
    "Hünärler",
    "Hümarmen ugurlar",
    "Bakalawr ugurlar",
    "Magistr ugurlar",
    "Alymlyk derejeler",
    "Halkara indedeksli zurnallar",
    "Maddy enjamlaýyn üpjünçilik"
])

if page == "Hünärler":
    st.header(page_title)

    df_hunarler = pd.read_csv('structured_data.csv')
    # st.write(df_hunarler)
    # print(df_hunarler.dtypes)

    df_hunarler['Talyp sany'] = pd.to_numeric(df_hunarler['Talyp sany'], errors='coerce')  # Convert to numeric, coercing invalid values to NaN
    df_hunarler = df_hunarler[df_hunarler['Talyp sany'].notnull()] 
    df_hunarler['Talyp sany'] = df_hunarler['Talyp sany'].astype(int)  # Convert to integer

    # st.dataframe(df)
    # Multiselect for filtering universities
    universities = df_hunarler['University'].unique().tolist()
    universities.sort()  # Sort alphabetically
    universities.insert(0, "Ählisi")  # Add "All" option at the top

    selected_universities = st.multiselect(
        "Uniwersitet saýlaň:",
        options=universities,
        default="Ählisi"
    )

    # Filter the DataFrame based on selection
    if "Ählisi" in selected_universities:
        filtered_df = df_hunarler  # No filtering
    else:
        filtered_df = df_hunarler[df_hunarler['University'].isin(selected_universities)]

    # Line chart: Trends over time by Year and Program
    st.subheader("Setir çyzgysy: Hünärler boýunça talyplaryň sany")
    line_chart_data = filtered_df.groupby(['Year', 'Hünärler'])['Talyp sany'].sum().unstack()
    st.line_chart(line_chart_data)

    # Dropdown for filtering year with an "All" option
    years = df_hunarler['Year'].unique().tolist()
    years.sort()  # Sort by year
    years.insert(0, "Ählisi")  # Add "All" option at the top

    selected_year = st.selectbox(
        "Ýyl saýlaň:",
        options=years,
        index=0
    )

    # Filter DataFrame based on year selection
    if selected_year != "Ählisi":
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
        pie_data = filtered_df[filtered_df['Year'] == selected_year].groupby('Hünärler')['Talyp sany'].sum()
    else:
        pie_data = filtered_df.groupby('Hünärler')['Talyp sany'].sum()
        

   
    st.subheader("Hünärler boýunça hünärleriň paýlanyşy")
    stacked_data = filtered_df.groupby(['Year', 'Hünärler'])['Talyp sany'].sum().unstack()
    stacked_data = stacked_data.fillna(0)
    stacked_data = stacked_data.apply(pd.to_numeric, errors='coerce')
    print(stacked_data)
    print(stacked_data.dtypes)


        # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    stacked_data.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Ýyl boýunça hünärleriň paýlanyşy")
    ax.set_ylabel("Talyp sany")
    ax.set_xlabel("")
    st.pyplot(fig)


    # Bar chart: Summarize student counts by Program for selected year(s)
    st.subheader("Hünär boýunça jemi talyp sany")
    bar_chart_data = filtered_df.groupby('Hünärler')['Talyp sany'].sum()
    st.bar_chart(bar_chart_data)

    st.subheader("Belli bir ýyl üçin hünär paýlanyşy")

    col1, col2, col3 = st.columns(3)
    with col2:
        if pie_data.sum() == 0:
            # st.subheader("Belli bir ýyl üçin hünär paýlanyşy")
            # st.dataframe(pie_data.reset_index().rename(columns={"index": "Program", 0: "Talyp sany"}))
            st.warning("Bu ýýylda hiç hili hünär yok.")
        else:
            # Plot the pie chart

            fig, ax = plt.subplots(figsize=(8, 6))
            pie_data.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90, colors=["#90ee90", "#87cefa", "#f59393"])
            ax.set_ylabel("")  # Remove y-axis label
            ax.set_title("Belli bir ýyl üçin hünär paýlanyşy", fontsize=14)

            # Streamlit display
            st.pyplot(fig)

    

    # Subheader for Streamlit
    st.subheader("Uniwersitet we ýyl boýunça ýazylmak (enrollment)")

    # Pivot the data for heatmap
    heatmap_data = filtered_df.pivot_table(
        index='University', columns='Year', values='Talyp sany', aggfunc='sum'
    ).fillna(0)

    # Plotting with adjustments
    fig, ax = plt.subplots(figsize=(15, 10))  # Increase figure size for readability
    sns.heatmap(
        heatmap_data,
        cmap="YlGnBu",  # Keep a readable color palette
        annot=False,  # Remove text annotations for better readability
        linewidths=0.5,  # Add gridlines
        cbar_kws={"shrink": 0.8}  # Shrink colorbar for better alignment
    )

    # Improve axis label readability
    ax.set_title("Uniwersitet we ýyl boýunça ýazylmak (enrollment)", fontsize=16, pad=20)
    ax.set_xlabel("Ýyl", fontsize=12)
    ax.set_ylabel("Uniwersitet", fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=10)  # Rotate x-axis labels
    ax.tick_params(axis='y', labelsize=10)  # Adjust y-axis label size

    # Display the heatmap
    st.pyplot(fig)


    st.subheader("Correlation Heatmap")
    corr_data = filtered_df[['Talyp sany']].copy()
    corr_data['Year'] = filtered_df['Year'].astype(str).str[:4].astype(int)  # Convert 'Year' to numeric start year
    correlation = corr_data.corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Correlation Matrix")
    st.pyplot(fig)

if page == "Hümarmen ugurlar":
    st.title("Hümarmen ugurlar seljermesi")
    humarmen_main()  # Call the main function from humarmen_ugurlar.py













