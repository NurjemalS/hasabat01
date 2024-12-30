import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px  # Ensure this import is included
from math import pi
import plotly.graph_objects as go



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
plt.rcParams["font.family"] = "Times New Roman"

st.sidebar.title("Nawigasiýa")

		
page = st.sidebar.radio("Kategoriýa saýlaň", [
    "Quota", 
    # "Hünärler",
    # "Hümarmen ugurlar",
    # "Bakalawr ugurlar",
    # "Magistr ugurlar",
    "Alymlyk derejeler",
    "Halkara indedeksli zurnallar",
    "Maddy enjamlaýyn üpjünçilik",
    # "Şahamçalar",
    "Hyzmatdaşlyklar"
])

def ugurlar(file_path):
    # humarmen_main()  # Call the main function from humarmen_ugurlar.py
     # Set global font to Times New Roman
    plt.rcParams["font.family"] = "Times New Roman"


        # Load the restructured data
    # file_path = "restructured_data_2.csv"  # Update with your actual path
    df = pd.read_csv(file_path)
    df.fillna(0, inplace=True)

        # Sidebar Filters
    # years = sorted(df['Year'].unique())
    # universities = sorted(df['Uviversity'].unique())

    years = ["Ählisi"] + sorted(df['Year'].unique())
    universities = ["Ählisi"] + sorted(df['Uviversity'].unique())

    selected_years = st.multiselect("Ýyl saýlaň", years, default='Ählisi')
    selected_universities = st.multiselect("Uniwersitet saýlaň", universities, default='Ählisi')
    # selected_faculties = st.multiselect("Select Faculty/Faculties", faculties, default=faculties)      bring it backkkkkkkkkkkkkkkkk

        # Filter data based on selection
    filtered_df = df[
        ((df['Year'].isin(selected_years)) | ("Ählisi" in selected_years)) &
        ((df['Uviversity'].isin(selected_universities)) | ("Ählisi" in selected_universities))
    ]

        # Display filtered data
    # st.write("### Filtered Data")
    # st.dataframe(filtered_df)

        # 1. Enrollment Trends Over Years
    st.write("### Ýyllaryň dowamynda umumy hasaba alyş tendendi")
    enrollment_trend = filtered_df.groupby('Year')[['Tölegli talyp sany', 'BŽ talyp sany']].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=enrollment_trend, x='Year', y='Tölegli talyp sany', marker='o', label='Tölegli talyplar', ax=ax)
    sns.lineplot(data=enrollment_trend, x='Year', y='BŽ talyp sany', marker='o', label='BŽ talyplar', ax=ax)
    ax.set_title("Ýyl boýunça umumy hasaba alyş tendendi", fontsize=18, weight='bold')
    ax.set_xlabel("Ýyl", fontsize=14)
    ax.set_ylabel("Talyp sany", fontsize=14)
    ax.legend(fontsize=12)
    st.pyplot(fig)

        # 2. University-Wise Enrollment
    st.write("### Uniwersitet ara hasaba alyş")
    university_totals = filtered_df.groupby('Uviversity')[['Tölegli talyp sany', 'BŽ talyp sany']].sum()
    if not university_totals.empty and university_totals.sum().sum() > 0:
        fig, ax = plt.subplots(figsize=(12, 8))
        university_totals.plot(kind='bar', stacked=True, ax=ax, color=["#87cefa", "#f59393"])
        ax.set_title("Uniwersitet ara hasaba alyş", fontsize=18, weight='bold')
        ax.set_xlabel("Uniwersitet", fontsize=14)
        ax.set_ylabel("Talyp sany", fontsize=14)
        st.pyplot(fig)
    else:
        st.warning("Bu uniwersitetde hiç hili  ugur yok.")

        # 3. Faculty Analysis
    st.write("### Ugurlar boýunça hasaba alyş")
    faculty_totals = filtered_df.groupby('Hünärler')[['Tölegli talyp sany', 'BŽ talyp sany']].sum()
    if not faculty_totals.empty and faculty_totals.sum().sum() > 0:
        faculty_totals = faculty_totals[faculty_totals.sum(axis=1) > 0]  # Remove faculties with zero students
        fig, ax = plt.subplots(figsize=(12, 8))
        faculty_totals.plot(kind='bar', stacked=True, ax=ax, color=["#90ee90", "#f2f277"])
        ax.set_title("Ugurlar boýunça hasaba alyş", fontsize=18, weight='bold')
        ax.set_xlabel("Ugurlar", fontsize=14)
        ax.set_ylabel("Talyp sany", fontsize=14)
        st.pyplot(fig)
    else:
        st.warning("Bu uniwersitetde hiç hili  ugur yok.")


    # 5. Yearly Enrollment Summary
    st.write("### Ýyl boýunça hasaba alyş")
    yearly_totals = filtered_df.groupby('Year')[['Tölegli talyp sany', 'BŽ talyp sany']].sum()
    if not yearly_totals.empty and yearly_totals.sum().sum() > 0:
            st.bar_chart(yearly_totals)
    else:
        st.warning("Bu uniwersitetde hiç hili  ugur yok.")


    ol1, col2, col3 = st.columns(3)

    with col2:
        st.write("### Tölegli talyplar we BŽ talyplar göterim gatnaşygy")

        total_students = filtered_df[['Tölegli talyp sany', 'BŽ talyp sany']].sum().sum()
        paid_percentage = (filtered_df['Tölegli talyp sany'].sum() / total_students) * 100
        unpaid_percentage = (filtered_df['BŽ talyp sany'].sum() / total_students) * 100

        if total_students.sum().sum() > 0:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(
                [paid_percentage, unpaid_percentage],
                labels=["Tölegli talyp sany", "BŽ talyp sany"],
                autopct='%1.1f%%',
                colors=["#87cefa", "#f59393"],
                startangle=90,
                textprops={"fontsize": 18}
            )
            ax.set_title("Tölegli talyplar we BŽ talyplar göterim gatnaşygy", fontsize=16, weight='bold')
            st.pyplot(fig)
        else:
            st.warning("Bu uniwersitetde hiç hili  ugur yok.")



# ???????????????????????????????
    st.write("### Ýyl-ýyla hasaba alyşynyň göterim üýtgeýşi")
    enrollment_trend['Total Students'] = enrollment_trend['Tölegli talyp sany'] + enrollment_trend['BŽ talyp sany']
    if 'Total Students' in enrollment_trend.columns and (enrollment_trend['Total Students'] > 0).any():

        enrollment_trend['YoY Change (%)'] = enrollment_trend['Total Students'].pct_change() * 100

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x='Year', y='YoY Change (%)', data=enrollment_trend, palette="viridis", ax=ax
        )
        ax.axhline(0, color="gray", linestyle="--", linewidth=1)
        ax.set_title("Ýyl-ýyla hasaba alyşynyň göterim üýtgeýşi", fontsize=16, weight='bold')
        ax.set_xlabel("Ýyl", fontsize=14)
        ax.set_ylabel(" Göterim üýtgeýşi (%)", fontsize=14)
        st.pyplot(fig)
    else:
        st.warning("Bu uniwersitetde hiç hili  ugur yok.")

# ????????????
    st.write("### Ugurlar boýunça ýokary 10 sany görkeziji")
    faculty_totals['Total Students'] = faculty_totals['Tölegli talyp sany'] + faculty_totals['BŽ talyp sany']
    if 'Total Students' in faculty_totals.columns and (faculty_totals['Total Students'] > 0).any():

        top_faculties = faculty_totals.sort_values('Total Students', ascending=False).head(10)

        fig, ax = plt.subplots(figsize=(10, 8))
        top_faculties['Total Students'].plot(kind='barh', color="#90ee90", ax=ax)
        ax.set_title("Ugurlary boýunça ýokary 10 sany görkeziji", fontsize=16, weight='bold')
        ax.set_xlabel("Talyplar", fontsize=14)
        ax.set_ylabel("Ugurlar", fontsize=14)
        ax.invert_yaxis()
        st.pyplot(fig)
    else:
        st.warning("Bu uniwersitetde hiç hili  ugur yok.")


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
    ugurlar("restructured_data_2.csv")
    

if page == "Bakalawr ugurlar":
    st.title("Bakalawr ugurlar seljermesi")
    ugurlar("restructured_data_3.csv")


if page == "Magistr ugurlar":
    st.title("Magistr ugurlar seljermesi")
    ugurlar("restructured_data_4.csv")

if page == "Hyzmatdaşlyklar":

    country_metadata = pd.DataFrame({
            "Country Code": ["ABS", "KOR", "JPN", "PAK", "MYS", "AUT", "ROU", "AZE", "KAZ", "RUS", "CHN", "ITA", "ARE", "UZB", "BLR", "DEU", "KGZ", "GEO", "IRN", "HUN", "SGP", "TUR", "UKR", "ARM", "CRO", "SUI", "AFG", "IND", "PLE", "KSA", "QAT", "KUW", "ARG", "TUN", "MAR", "FRA", "BAH", "TJK", "SRB" ],
            "Latitude": [37.0902, 35.9078, 36.2048, 30.3753, 4.210484, 47.516231, 45.943161, 40.143105, 48.019573, 61.52401, 35.86166, 41.87194, 23.424076, 41.377491, 53.709807, 51.165691, 41.20438, 42.315407, 32.427908, 47.162494, 1.352083, 38.963745, 48.379433, 40.069099, 45.1, 46.818188, 33.93911, 20.593684, 31.952162, 23.885942, 25.354826, 29.31166,-38.416097, 33.886917, 	31.791702, 46.227638, 25.930414, 38.861034, 44.016521 ],
            "Longitude": [-95.7129, 127.7669, 138.2529, 69.3451, 101.975769, 14.550072, 24.96676, 47.576927, 66.923684, 105.318756, 104.195397, 12.56738, 53.847818, 64.585262, 27.953389, 10.451526, 74.766098, 43.356892, 53.688046, 19.503304, 103.819836, 35.243322, 31.16558, 45.038189, 15.2, 8.227512,67.709953, 78.96288, 35.233154, 45.079162, 51.183884, 47.481766, -63.616672, 9.537499,-7.09262, 2.213749, 50.637772, 71.276093, 21.005859 ],
        })

    university_map = {
        "ABS": [
            {"code": "A1", "name": "Raýat döwlet uniwersiteti"},
            {"code": "A2", "name": "Kent döwlet uniwersiteti"}
        ],
        "KOR": [
            {"code": "K1", "name": "Sonýungwan uniwersiteti"},
            {"code": "K2", "name": "Hanýang uniwersiteti"},
            {"code": "K3", "name": "Inha uniwersiteti"},
            {"code": "K4", "name": "Koreýa uniwersitetiniň Lukmançylyk kolleji"},
            {"code": "K5", "name": "Hankuk daşary ýurt dilleri uniwersiteti"},
            {"code": "K6", "name": "Seul Milli ylym we tehnologiýa uniwersiteti"},
            {"code": "K7", "name": "Koreýa Milli sungat uniwersiteti"},
            {"code": "K8", "name": "Koreýa Respublikasynyň Daşary işler ministrliginiň Koreýa Milli diplomatik akademiýasy"},
            {"code": "K9", "name": "Seul milli uniwersiteti"}
        ],
        "JPN": [
            {"code": "J1", "name": "Tokionyň daşary ýurt dilleri uniwersiteti"},
            {"code": "J2", "name": "Sukuba uniwersiteti"},
            {"code": "J3", "name": "Ýapon-Türkmen assosiasiýasy"},
            {"code": "J4", "name": "Kawasaki senagat ösüş institutynyň Nanomedisina innowasiýa merkezi"},
            {"code": "J5", "name": "Ýaponiýanyň Soka uniwersiteti"}
        ],
        "PAK": [
            {"code": "P1", "name": "Parahatçylyk we diplomatik bilimleri instituty"},
            {"code": "P2", "name": "Islamabat COMSATS Uniwersiteti"},
            {"code": "P3", "name": "Pakistan Yslam Respublikasynyň Daşary işler ministrliginiň Diplomatik gullugy akademiýasy"},
            {"code": "P4", "name": "Häzirki zaman dilleri Milli uniwersiteti"}
        ],
        "MYS": [
            {"code": "M1", "name": "Dolandyryş we ylym uniwersiteti"},
            {"code": "M2", "name": "“PETRONAS Çarigali (Türkmenistan) Sdn Bhd” kompaniýasy we “PETRONAS” kompaniýasynyň Tehnologik uniwersiteti"},
            {"code": "M3", "name": "Tenaga milli uniwersiteti"},
            {"code": "M4", "name": "Malaýziýanyň KDU uniwersitetiniň kolleji"}
        ],
        "AUT": [
            {"code": "AU1", "name": "IMC amaly ylymlar uniwersiteti"},
            {"code": "AU2", "name": "Leoben dag-magdan uniwersiteti"},
            {"code": "AU3", "name": "Graz tehnologiýalar uniwersiteti"},
            {"code": "AU4", "name": "Insbruk şäheriniň menejment merkezi"}
        ],
        "ROU": [
            {"code": "R1", "name": "Alba Ýuliýa şäherindäki “1 Decembrie 1918” uniwersiteti"},
            {"code": "R2", "name": "Piteşti uniwersiteti"},
            {"code": "R3", "name": "Arad şäheriniň “Vasile Goldis” günbatar uniwersiteti"},
            {"code": "R4", "name": "Ploýeşti şäheriniň Nebit-gaz uniwersiteti"},
            {"code": "R5", "name": "Buharestiň Raýat gurluşygy tehniki uniwersiteti"},
            {"code": "R6", "name": "Buharest şäherindäki Politehniki uniwersiteti"},
            {"code": "R7", "name": "Buharest Oba hojalyk ylymlary we weterinar lukmançylygy uniwersiteti"},
            {"code": "R8", "name": "«Ion Ionescu de la Brad» Ýassy Oba hojalyk ylymlary we weterinar lukmançylygy uniwersiteti"},
            {"code": "R9", "name": "Braşow şäherindaki Transilwaniýa uniwersiteti"},
            {"code": "R10", "name": "Buharestiň ykdysady bilimler uniwersiteti"},
            {"code": "R11", "name": "Buharestiň ykdysady bilimler uniwersiteti"},
            {"code": "R12", "name": "Buharestiň milli bedenterbiýe we sport uniwersiteti"},
            {"code": "R13", "name": "Romania unknown13 university"},
            {"code": "R14", "name": "Romania unknown14 university"}
        ],
        "AZE": [
            {"code": "AZ1", "name": "Azerbaýjan Respublikasynyň Daşary işler ministrliginiň ýanyndaky “ADA” uniwersiteti"},
            {"code": "AZ2", "name": "Baku döwlet uniwersiteti"}
        ],
        "KAZ": [
            {"code": "KA1", "name": "Awtonom bilim edarasy “Nazarbaýew uniwersiteti”"},
            {"code": "KA2", "name": "Abylaý han adyndaky Gazak halkara gatnaşyklar we dünýä dilleri uniwersiteti"},
            {"code": "KA3", "name": "«Al-Farabi adyndaky gazak milli uniwersiteti»"},
            {"code": "KA4", "name": "Gazagystan Respublikasynyň Daşary işleri ministrliginiň Daşarysyýasy barlaglar boýunça instituty"},
            {"code": "KA5", "name": "Gazagystan Respublikasynyň Prezidentiniň ýanyndaky Döwlet dolandyryş akademiýasy"},
            {"code": "KA6", "name": "Bedenterbiýe we sport uniwersitetleriniň halkara birleşigi"},
            {"code": "KA7", "name": "L.N.Gumilýow adyndaky Ýewraziýa milli uniwersiteti"}
        ],
        "RUS": [
            {"code": "RU1", "name": "“W.N. Tatişew adyndaky Astrahan döwlet uniwersiteti” federal döwlet býujet ýokary bilim edarasy"},
            {"code": "RU2", "name": "I.M.Gubkin adyndaky Russiýa döwlet nebit we gaz uniwersiteti"},
            {"code": "RU3", "name": "D.I.Mendeleýew adyndaky himiýa tehnologiýa uniwersiteti"},
            {"code": "RU4", "name": "Kazanyň Milli barlag tehnologiýalar uniwersiteti"},
            {"code": "RU5", "name": "Russiýa Federasiýasynyň Saglygy goraýyş ministrliginiň ýokary bilimiň Federal döwlet býujet bilim beriş edarasy “Astrahan döwlet lukmançylyk uniwersiteti”"},
            {"code": "RU6", "name": "Russiýa Federasiýasynyň Saglygy goraýyş ministrliginiň Federal Döwlet býutjet edarasy “Gelmgols adyndaky göz keselleriniň milli lukmançylyk barlag merkezi”"},
            {"code": "RU7", "name": "Kazan (Priwolžskiý) Federal uniwersiteti"},
            {"code": "RU8", "name": "Ýokary bilim federal döwlet býujet bilim edarasynyň „Naberežnyýe Çelny döwlet mugallymçylyk uniwersiteti”"},
            {"code": "RU9", "name": "Tatarystan Respublikasynyň A.N. Tupolýew adyndaky Kazan milli barlag tehniki uniwersiteti"},
            {"code": "RU10", "name": "Wolganyň döwlet suw ulaglary uniwersiteti"},
            {"code": "RU11", "name": "Wolgograd döwlet durmuş-mugallymçylyk uniwersiteti"},
            {"code": "RU12", "name": "W.N.Tatişew adyndaky Astrahan döwlet uniwersiteti"},
            {"code": "RU13", "name": "Kazan döwlet energetika uniwersiteti"},
            {"code": "RU14", "name": "Moskwa döwlet geodeziýa we kartografiýa uniwersiteti"},
            {"code": "RU15", "name": "Powolžýe döwlet bedenterbiýe, sport we syýahatçylyk uniwersiteti"},
            {"code": "RU16", "name": "Russiýa Federasiýasynyň Daşary işler ministrliginiň Moskwanyň Halkara gatnaşyklary döwlet instituty (uniwersiteti)"},
            {"code": "RU17", "name": "M.W.Lomonosow adyndaky Moskwa döwlet uniwersiteti"}
        ],
        "CHN": [
            {"code": "C1", "name": "Hytaý dil bilimi we hyzmatdaşlyk merkezi"},
            {"code": "C2", "name": "Sian nebit uniwersiteti, Hebeý nebit hünär-tehniki uniwersiteti, Hytaýyň Milli Nebitgaz Korporasiýasy we Hytaýyň bilim ulgamynda halkara alyş-çalyş assosiasiýasy"},
            {"code": "C3", "name": "Hytaýyň nebit uniwersiteti"},
            {"code": "C4", "name": "Hytaýyň Milli Nebitgaz Korporasiýasy"},
            {"code": "C5", "name": "Pekiniň hytaý lukmançylygy uniwersiteti"},
            {"code": "C6", "name": "Demirgazyk-Günbatar oba-hojalyk we tokaýçyyk uniwersitet"},
            {"code": "C7", "name": "Sinzýan uniwersiteti"},
            {"code": "C8", "name": "Pekiniň daşary ýurt dilleri uniwersiteti"}
        ],
        "ITA": [
            {"code": "I1", "name": "Wenesiýanyň Ka’Foskari uniwersiteti"},
            {"code": "I2", "name": "Milanyň Politehniki uniwersiteti"},
            {"code": "I3", "name": "Wenesiýanyň Ka'Foskari uniwersiteti"},
            {"code": "I4", "name": "Turiniň Politehniki uniwersiteti"},
            {"code": "I5", "name": "Italiýa Respublikasynyň Frozinone şäheriniň şekillendiriş sungaty akademiýasy"},
            {"code": "I6", "name": "Milan Politehniki uniwersiteti"},
            {"code": "I7", "name": "Italýan diplomatik akademiýasy"},
            {"code": "I8", "name": "Perujanyň daşary ýurtlylar üçin uniwersiteti"}
        ],
        "ARE": [
            {"code": "AR1", "name": "“Dragon Oýl (Türkmenistan) Ltd.” kompaniýasy"},
            {"code": "AR2", "name": "Anwar Gargaş adyndaky Diplomatik Akademiýasy"}
        ],
        "UZB": [
            {"code": "U1", "name": "Daşkent döwlet tehniki uniwersiteti"},
            {"code": "U2", "name": "Daşkent maliýe instituty"},
            {"code": "U3", "name": "Daşkent döwlet ykdysady uniwersiteti"},
            {"code": "U4", "name": "Özbek döwlet dünýä dilleri uniwersiteti"},
            {"code": "U5", "name": "Buhara Inženerçilik we tehnologiýalar instituty"},
            {"code": "U6", "name": "Özbegistan Respublikasynyň Daşkent binagärlik-gurluşyk instituty"},
            {"code": "U7", "name": "Daşkent döwlet agrar uniwersiteti"},
            {"code": "U8", "name": "Daşkent irrigasiýa we oba hojalygyň mehanizasiýasy instituty"},
            {"code": "U9", "name": "Yslam Karimow adyndaky Daşkentiň döwlet tehniki uniwersiteti"},
            {"code": "U10", "name": "Daşkent döwlet agrar uniwersiteti"},
            {"code": "U11", "name": "Samarkant döwlet weterinar lukmançylygy, maldarçylyk we biotehnologiýalar uniwersiteti (Samarkant oba hojalyk instituty)"},
            {"code": "U12", "name": "Nizami adyndaky Daşkent döwlet mugallymçylyk uniwersiteti"},
            {"code": "U13", "name": "Buhara döwlet uniwersiteti"},
            {"code": "U14", "name": "Özbegistan Respublikasynyň Dünýä ykdysadyýeti we diplomatiýa uniwersiteti"},
            {"code": "U15", "name": "Merkezi Aziýa Halkara instituty"}
        ],
        "BLR": [
            {"code": "B1", "name": "Ýewfrosiniýa Polotskaýa adyndaky Polotsk döwlet uniwersiteti"},
            {"code": "B2", "name": "Belarus döwlet tehnologik uniwersiteti"},
            {"code": "B3", "name": "Belarus Milli tehniki uniwersiteti"},
            {"code": "B4", "name": "Belarus Döwlet lukmançylyk uniwersiteti"},
            {"code": "B5", "name": "Belarus döwlet ykdysadyýet uniwersiteti"},
            {"code": "B6", "name": "Belarus alyjylar kooperasiýasynyň söwda-ykdysady uniwersiteti"},
            {"code": "B7", "name": "Brest döwlet tehniki uniwersiteti"},
            {"code": "B8", "name": "Belarus döwlet oba hojalyk akademiýasy"},
            {"code": "B9", "name": "Belarus döwlet agrar tehniki uniwersiteti"},
            {"code": "B10", "name": "A.S.Puşkin adyndaky Brest döwlet uniwersiteti"},
            {"code": "B11", "name": "Fransisk Skorina adyndaky Gomel döwlet uniwersiteti"},
            {"code": "B12", "name": "Brest döwlet tehniki uniwersiteti"},
            {"code": "B13", "name": "P.O. Suhoý adyndaky Gomel döwlet tehniki uniwersiteti"},
            {"code": "B14", "name": "Belorus döwlet uniwersiteti"},
            {"code": "B15", "name": "Belorus unknown15 uniwersiteti"},
            {"code": "B16", "name": "Belorus unknown16 uniwersiteti"}

        ],
        "DEU": [
            {"code": "D1", "name": "Swikau Günbatarsakson ýokary okuw mekdebi – Amaly ylymlar uniwersiteti"},
            {"code": "D2", "name": "Berlin amaly ylymlar Beauth uniwersiteti"},
            {"code": "D3", "name": "Martin Lýuter adyndaky Halle-Wittenberg uniwersiteti"}
        ],
        "KGZ": [
            {"code": "KG1", "name": "I.Razzakow adyndaky Gyrgyz döwlet tehniki uniwersiteti"},
            {"code": "KG2", "name": "Gyrgyz Respublikasynyň Daşary işler ministrliginiň K.Dikambaýew adyndaky Diplomatik akademiýasy"}
        ],
        "GEO": [
            {"code": "GE1", "name": "Tbilisi döwlet lukmançylyk uniwersiteti"}
        ],
        "IRN": [
            {"code": "IR1", "name": "Maşat Lukmançylyk ylymlary uniwersiteti"},
            {"code": "IR2", "name": "Maşadyň Ferdöwsi adyndaky uniwersiteti"},
            {"code": "IR3", "name": "Maşadyň Ferdöwsi adyndaky uniwersiteti"},
            {"code": "IR4", "name": "Gürgen oba hojalyk ylymlary we tebigy serişdeler uniwersiteti"},
            {"code": "IR5", "name": "Eýran Yslam Respublikasynyň Daşary işler ministrliginiň Syýasy we halkara barlaglar instituty"}
        ],
        "HUN": [
            {"code": "H1", "name": "Zemmelwaýs uniwersiteti"},
            {"code": "H2", "name": "Sent Iştwan uniwersiteti"},
            {"code": "H3", "name": "Wengriýanyň Daşary işler we söwda ministrliginiň Diplomatik akademiýasy"}
        ],
        "SGP": [
            {"code": "SG1", "name": "Singapur Pte Ltd-nin Dolandyryş we ösüş instituty"}
        ],
        "TUR": [
            {"code": "TR1", "name": "Bilkent uniwersiteti"},
            {"code": "TR2", "name": "Bilkent kiberparky"},
            {"code": "TR3", "name": "Türkiýe Respublikasynyň Daşary işler ministrliginiň Diplomatik akademiýasy"}
        ],
        "UKR": [
            {"code": "UK1", "name": "Harkowyň Pýotr Wasilenko adyndaky milli oba hojalyk tehniki uniwersiteti"},
            {"code": "UK2", "name": "Ukrainanyň Bioserişdeleri we tebigaty ulanyş milli uniwersiteti"},
            {"code": "UK3", "name": "Ukrainanyň Daşary işler ministrliginiň ýanyndaky G.Udowenko adyndaky Diplomatik akademiýasy"}
        ],
        "ARM": [
            {"code": "ARM1", "name": "Ermenistanyň Milli agrar uniwersiteti"},
            {"code": "ARM2", "name": "Ermenistan Respublikasynyň Daşary işler ministrliginiň Diplomatik mekdebi"},
            {"code": "ARM3", "name": "Ermenistanyň Döwlet bedenterbiýe instituty"},
            {"code": "ARM4", "name": "Ýerewan döwlet uniwersiteti"}
        ],
        "CRO": [
            {"code": "HR1", "name": "Horwatiýa Respublikasynyň Daşary işler we Ýewropa integrasiýasy ministrliginiň Diplomatik akademiýasy"}
        ],
        "SUI": [
            {"code": "SU1", "name": "Ženewanyň syýasy howpsuzlyk merkezi"}
        ],
        "AFG": [
            {"code": "AF1", "name": "Owganystanyň Daşary işler ministrliginiň Diplomatiýa instituty"},
            {"code": "AF2", "name": "Jowzjan uniwersiteti"}
        ],
        "IND": [
            {"code": "IN1", "name": "Hindistanyň Daşary işler ministrliginiň Suşma Swaraj adyndaky Diplomatik gullugy instituty"}
        ],
        "PLE": [
            {"code": "PL1", "name": "Palestinanyň Daşary işler ministrliginiň Diplomatiýa instituty"}
        ],
        "KSA": [
            {"code": "KS1", "name": "Saud Arabystany Patyşalygynyň Daşary işler ministrliginiň Emir Saud Al Faýsal adyndaky Diplomatiýany öwreniş institutynyň arasynda Hyzmatdaşlyk Maksatnama"}
        ],
        "QAR": [
            {"code": "Q1", "name": "Katar Döwletiniň Daşary işler ministrliginiň Diplomatiýa instituty"}
        ],
        "KUW": [
            {"code": "KU1", "name": "Kuweýt döwletiniň Daşary işler ministrliginiň Saud Al-Nesser Al-Sabah adyndaky Diplomatik instituty"}
        ],
        "ARG": [
            {"code": "ARG1", "name": "Argentina Respublikasynyň Daşary işler we kult ministrliginiň Milli daşary gulluk instituty"}
        ],
        "TUN": [
            {"code": "TUN1", "name": "Tunis Respublikasynyň Taýýarlyk we Okuwlar boýunça Diplomatik instituty"}
        ],
        "MAR": [
            {"code": "MR1", "name": "Marokko Patyşalygynyň Daşary işler we halkara hyzmatdaşlyk ministrliginiň Diplomatik Akademiýasy"}
        ],
        "FRA": [
            {"code": "FR1", "name": "Ýewropanyň Mümkinçilikler we howpsuzlyk instituty"}
        ],
        "BAH": [
            {"code": "BH1", "name": "Muhammed bin Mubarak Al Halifa adyndaky Diplomatik bilimleri Akademiýasy"}
        ],
        "TJK": [
            {"code": "TJ1", "name": "Täjigistan Respublikasynyň Prezidentiniň ýanyndaky Strategik barlaglar merkezi"},
            {"code": "TJ2", "name": "Täjigistan Respublikasynyň Daşary işler ministrliginiň Diplomatik gullugynyň işgärleriniň hünärini ýokarlandyryş we gaýtadan taýýarlaýyş merkezi"},
            {"code": "TJ3", "name": "Täjik milli uniwersiteti"}
        ],
        "SRB": [
            {"code": "SR1", "name": "Serbiýa Respublikasynyň Daşary işler ministrliginiň Diplomatik akademiýasy"}
        ]
    }

    def map_university_names(data, university_map):
        def get_university_name(row):
            for entry in university_map.get(row["Partner Country Code"], []):
                if entry["code"] == row["Partner University Code"]:
                    return entry["name"]
            return None

        data["Partner University Name"] = data.apply(get_university_name, axis=1)
        return data

    st.title("Ýokary okuw mekdepleriniň hyzmatdaşlyk edýän daşary ýurtlarynyň hem-de olaryň ýokary okuw mekdepleriniň sany barada maglumat")

    # Load data
    data = pd.read_csv("HALKARA_HYZ_data_1.csv")

    map_university_names(data, university_map)
    # st.dataframe(data)
    data["Year"] = data["Year"].astype(str)


    # Filters
    years = ["All Years"] + sorted(data["Year"].unique().tolist())
    universities = ["All Universities"] + sorted(data["University"].unique().tolist())

    selected_year = st.selectbox("Select Year", years)
    selected_university = st.selectbox("Select University", universities)


    def filter_data(data, selected_university, selected_year):
        filtered_data = data
        if selected_year != "All Years":
            filtered_data = filtered_data[filtered_data["Year"] == selected_year]
        if selected_university != "All Universities":
            filtered_data = filtered_data[filtered_data["University"] == selected_university]
        return filtered_data

    # Filter data
    filtered_data = filter_data(data, selected_university, selected_year)




    # Analysis
    def analyze_partnerships(data, selected_university, selected_year):
        filtered_data = filter_data(data, selected_university, selected_year)

        unique_countries = filtered_data["Partner Country Code"].nunique()
        unique_universities = filtered_data["Partner University Code"].nunique()

        country_names = filtered_data["Partner Country Code"].unique().tolist()
        university_names = filtered_data["Partner University Name"].dropna().unique().tolist()
        print(len(country_names))
        print(len(university_names))

        return unique_countries, unique_universities, country_names, university_names, filtered_data


    unique_countries, unique_universities, country_names, university_names, filtered_data = analyze_partnerships( data, selected_university, selected_year)

    # Display results
    # st.write(f"### Selected University: {selected_university}")
    # st.write(f"### Selected Year: {selected_year}")
    st.write(f"#### Unique Partner Countries: {unique_countries}")
    st.write(f"#### Unique Partner Universities: {unique_universities}")
    country_names = [country for country in country_names if pd.notna(country)]
    university_names = [university for university in university_names if pd.notna(university)]


    # Function to map filtered country codes to their respective universities
    def map_country_to_universities(filtered_data, university_map):
        country_university_map = {}

        # Extract unique country codes and university codes from the filtered data
        country_codes = filtered_data["Partner Country Code"].dropna().unique()
        university_codes = filtered_data["Partner University Code"].dropna().unique()

        # Match university names for each country code
        for country in country_codes:
            if country in university_map:
                # Map universities for the current country
                universities = [
                    uni["name"]
                    for uni in university_map[country]
                    if uni["code"] in university_codes
                ]
                country_university_map[country] = universities
            else:
                # If the country code exists but no universities are found
                country_university_map[country] = []

        return country_university_map


    # Example usage with Streamlit
    country_university_map = map_country_to_universities(filtered_data, university_map)

    # Display in Streamlit with Expanders
    with st.expander("Partner Countries and Universities (Click to Expand)"):
        st.write("#### Partner Countries and Universities")
        if country_university_map:
            for country, universities in country_university_map.items():
                st.write(f"**{country}:**")
                if universities:
                    st.markdown("\n".join([f"- {university}" for university in universities]))
                else:
                    st.write("No universities available for this country.")
        else:
            st.write("No partner countries or universities available.")

    def calculate_growth(data):
        # Group data by year
        grouped = data.groupby("Year")

        # Cumulative unique counts
        unique_countries_growth = []
        unique_universities_growth = []
        years = []

        cumulative_countries = set()
        cumulative_universities = set()

        for year, group in grouped:
            years.append(year)

            # Update cumulative sets
            cumulative_countries.update(group["Partner Country Code"].dropna().unique())
            cumulative_universities.update(group["Partner University Code"].dropna().unique())

            # Append counts
            unique_countries_growth.append(len(cumulative_countries))
            unique_universities_growth.append(len(cumulative_universities))

        # Create a DataFrame for analysis
        growth_df = pd.DataFrame({
            "Year": years,
            "Unique Countries": unique_countries_growth,
            "Unique Universities": unique_universities_growth
        })
        return growth_df


    def visualize_growth_line_chart(growth_df):
        """
        Displays a Streamlit line chart for unique countries and universities over time.
        """
        st.subheader("Line Chart: Growth of Unique Countries and Universities Over Time")

        # Transform the DataFrame for line chart format
        line_chart_data = growth_df.set_index("Year")

        # Use Streamlit's built-in line chart
        st.line_chart(line_chart_data)

    growth_df = calculate_growth(filtered_data)

    # Visualize the growth in a line chart
    visualize_growth_line_chart(growth_df)



    def analyze_partnerships(data):
        # Group by Partner Country Code to count partnerships
        country_counts = data.groupby("Partner Country Code").size().reset_index(name="Count")
        print("Country Counts Before Merge:", country_counts)

        # Merge with country metadata to add latitude and longitude
        country_counts = country_counts.merge(country_metadata, left_on="Partner Country Code", right_on="Country Code", how="left")
        print("Country Counts After Merge:", country_counts)

        return country_counts
    country_counts = analyze_partnerships(filtered_data)
    st.write(country_counts)

    # World Map, WE ARE ALSO CONSIDERING HERE UNIVERSITIS TOO

    def plot_world_map(country_counts):
        # Create a map visualization
        map_data = country_counts.copy()
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state=pdk.ViewState(
                    latitude=20, longitude=0, zoom=1.5
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=map_data,
                        get_position="[Longitude, Latitude]",
                        get_radius="Count * 7000",
                        get_fill_color="[144, 238, 0,  144]", 
                        # [144, 238, 0,  144]
                        # [200, 30, 0, 160]
                        pickable=True,
                    )
                ],
            )
        )

    st.subheader("World Map of Partnerships")
    plot_world_map(country_counts)


    # def plot_trends(data):
    #     # Pivot the data for grouped bar chart
    #     pivot_data = data.pivot(index="Year", columns="Partner Country Code", values="Count").fillna(0)

    #     # Plot the grouped bar chart
    #     ax = pivot_data.plot(kind="bar", stacked=True, figsize=(10, 6))

    #     # Customize the chart
    #     plt.title("Partnership Trends Over Time")
    #     plt.xlabel("Year")
    #     plt.ylabel("Number of Partnerships")
    #     plt.legend(title="Partner Country Code", bbox_to_anchor=(1.05, 1), loc="upper left")
    #     plt.tight_layout()

    #     # Display the chart in Streamlit
    #     st.pyplot(plt)
    #     plt.clf()  # Clear the figure for subsequent plots

    # plot_trends(filtered_data)



    # Calculate non-unique counts for bar chart
    def calculate_non_unique_counts(data):
        """
        Calculate non-unique counts of partnership countries and universities per year,
        ensuring each country is counted only once per university within the year.
        """
        # Ensure 'Year' and 'University' are treated as strings
        data["Year"] = data["Year"].astype(str)
        data["University"] = data["University"].astype(str)

        # Group by 'Year' and 'University', and remove duplicates within each group
        unique_partners_per_university = data.groupby(["Year", "University"])["Partner Country Code"].nunique().reset_index()

        # Group by 'Year' again to calculate the total unique counts for all universities
        yearly_counts = unique_partners_per_university.groupby("Year").agg({
            "Partner Country Code": "sum"  # Sum up unique counts per university for each year
        }).reset_index()

        # Calculate non-unique university partnerships directly from the original data
        non_unique_university_counts = data.groupby("Year").agg({
            "Partner University Code": "count"  # Total university partnerships without deduplication
        }).reset_index()

        # Merge the two results
        final_counts = yearly_counts.merge(non_unique_university_counts, on="Year")

        # Rename columns for clarity
        final_counts.rename(columns={
            "Partner Country Code": "Non-Unique Country Count",
            "Partner University Code": "Non-Unique University Count"
        }, inplace=True)

        return final_counts


    # Calculate corrected non-unique counts
    corrected_non_unique_counts_df = calculate_non_unique_counts(filtered_data)

    # Visualize using Streamlit's bar chart
    st.subheader("Jemi hyzmatdaş ýurt we uniwersitet sany")
    bar_chart_data = corrected_non_unique_counts_df.set_index("Year")[[
        "Non-Unique Country Count", 
        "Non-Unique University Count"
    ]]
    st.bar_chart(bar_chart_data)

    def analyze_partner_universities(data):
        # Group by Partner Country Code and count unique partner universities
        partner_universities = data.groupby("Partner Country Code")["Partner University Code"].nunique().reset_index()
        partner_universities.rename(columns={"Partner University Code": "Number of Universities"}, inplace=True)
        partner_universities = partner_universities.merge(country_metadata, left_on="Partner Country Code", right_on="Country Code", how="left")
        return partner_universities

    def plot_partner_universities_with_streamlit(partner_universities):
        # Prepare data for st.bar_chart
        partner_universities_chart = partner_universities.set_index("Partner Country Code")["Number of Universities"]
        st.bar_chart(partner_universities_chart)

    # Analysis
    st.header("Partner University Analysis")
    partner_universities = analyze_partner_universities(filtered_data)
    plot_partner_universities_with_streamlit(partner_universities)


    def plot_country_distribution(data):
        # Count unique universities per country
        university_distribution = data.groupby("Partner Country Code")["Partner University Code"].nunique().reset_index()
        university_distribution = university_distribution.merge(country_metadata, left_on="Partner Country Code", right_on="Country Code", how="left")
        university_distribution = university_distribution.sort_values("Partner University Code", ascending=False)

        # Limit the number of slices displayed
        top_n = 10  # Show top 10 countries
        others = university_distribution.iloc[top_n:].sum(numeric_only=True)["Partner University Code"]
        top_countries = university_distribution.iloc[:top_n]
        others_row = pd.DataFrame([{"Partner Country Code": "Others", "Partner University Code": others}])
        top_countries = pd.concat([top_countries, others_row], ignore_index=True)

        # Plot the improved pie chart
        fig, ax = plt.subplots(figsize=(8, 6))
        wedges, texts, autotexts = ax.pie(
            top_countries["Partner University Code"], 
            labels=top_countries["Partner Country Code"], 
            autopct='%1.1f%%', 
            startangle=90, 
            textprops={'fontsize': 15}, 
            colors=plt.cm.tab20.colors
        )
        ax.set_title("Distribution of Partner Universities by Country", fontsize=16, weight="bold")
        
        # Improve label formatting
        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_fontsize(9)

        # Display the chart
        st.pyplot(fig)

    col1, col2, col3 = st.columns(3)
    with col2:
        st.header("Distribution of Partner Universities")
        plot_country_distribution(filtered_data)


    def plot_heatmap(data):
        # Pivot table for heatmap
        heatmap_data = data.pivot_table(index="Year", columns="Partner Country Code", values="Partner University Code", aggfunc="count", fill_value=0)

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt="d", linewidths=0.5)
        ax.set_title("Heatmap of Partnerships Over Time", fontsize=16, weight="bold")
        ax.set_xlabel("Partner Country Code", fontsize=14)
        ax.set_ylabel("Year", fontsize=14)
        st.pyplot(fig)


    st.header("Heatmap of Partnerships")
    plot_heatmap(filtered_data)



    def plot_top_partners(data, university_map):
        # Helper function to map university codes to names
        def get_university_name(code):
            for country, universities in university_map.items():
                for uni in universities:
                    if uni["code"] == code:
                        return uni["name"]
            return code  # Fallback to code if name not found

        # Top countries
        top_countries = data.groupby("Partner Country Code").size().reset_index(name="Partnerships").sort_values("Partnerships", ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(top_countries["Partner Country Code"], top_countries["Partnerships"], color="orange")
        ax.set_title("Top 10 Partner Countries", fontsize=16, weight="bold")
        ax.set_xlabel("Country Code", fontsize=14)
        ax.set_ylabel("Number of Partnerships", fontsize=14)
        st.pyplot(fig)

        # Top universities
        top_universities = data.groupby("Partner University Code").size().reset_index(name="Partnerships").sort_values("Partnerships", ascending=False).head(10)
        top_universities["Partner University Name"] = top_universities["Partner University Code"].apply(get_university_name)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(top_universities["Partner University Name"], top_universities["Partnerships"], color="green")
        ax.set_title("Top 10 Partner Universities", fontsize=16, weight="bold")
        ax.set_xlabel("University Name", fontsize=14)
        ax.set_ylabel("Number of Partnerships", fontsize=14)
        plt.xticks(rotation=45, ha="right", fontsize=10)
        st.pyplot(fig)

    st.header("Top Partner Countries and Universities")
    plot_top_partners(filtered_data, university_map)

if page == "Alymlyk derejeler":
    st.title("Ýokary hünär bilim edaralarynda işleýän alymlyk derejeli we alymlyk atly işgärleriniň sany barada maglumat")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


    # Load Data
    long_df = pd.read_csv('Alymlyk_derejeler_restructured_data.csv')
    long_df.fillna(0, inplace=True)

    # Ensure Year is an integer
    long_df["Year"] = long_df["Year"].astype(str)

    # Sidebar Filters
    universities = sorted(long_df['University'].unique())
    universities.insert(0, "Ählisi")  # Add "ALL" option at the beginning

    selected_universities = st.multiselect("Uniwersitet saýlaň", universities, default="Ählisi")
    selected_types = st.multiselect("Dereje saýlaň", sorted(long_df['Type'].unique()), default=long_df['Type'].unique())

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Filter Data
    if "Ählisi" in selected_universities:
        filtered_df = long_df[long_df['Type'].isin(selected_types)]
    else:
        filtered_df = long_df[(long_df['University'].isin(selected_universities)) & (long_df['Type'].isin(selected_types))]

    # Line Chart for Historical Data
    st.write("###  Alymlyk derejeleriniň ýyllar boýy tendensiýalary")
    if not filtered_df.empty:
        line_chart_data = filtered_df.pivot_table(index='Year', columns='Type', values='Count', aggfunc='sum').fillna(0)
        st.line_chart(line_chart_data)
    else:
        st.write("Saýlananlar üçin maglumat ýok.")

    # Forecast Button
    if st.button("2030-njy ýyla çenli çaklama"):
        st.write("### Alymlyk derejeleriniň çaklama tendensiýalary (2025–2030)")

        # Prepare data for each type and forecast separately
        forecast_results = []
        combined_data = []

        for faculty_type in selected_types:
            type_data = filtered_df[filtered_df['Type'] == faculty_type]
            regression_data = type_data.groupby('Year')['Count'].sum().reset_index()

            # Prepare data for regression
            X = regression_data['Year'].values.reshape(-1, 1)
            y = regression_data['Count'].values

            if len(X) > 1:  # Ensure there is enough data for regression
                # Fit Linear Regression
                model = LinearRegression()
                model.fit(X, y)

                m = model.coef_[0]
                b = model.intercept_

                # Forecast future years
                future_years = np.arange(2025, 2031).reshape(-1, 1)
                future_counts = model.predict(future_years)
                # st.write(f"### Forecasting Formula: Faculty Count = {m:.2f} × Year + {b:.2f}")

                # Create forecast DataFrame
                forecast_df = pd.DataFrame({
                    'Year': future_years.flatten(),
                    'Count': future_counts,
                    'Type': faculty_type
                })

                # Combine historical and forecasted data
                combined_df = pd.concat([regression_data.assign(Type=faculty_type), forecast_df], ignore_index=True)
                combined_data.append(combined_df)

        # Combine all types into one DataFrame
        final_combined_df = pd.concat(combined_data, ignore_index=True)
        final_combined_df['Year'] = final_combined_df['Year'].astype(str)  # Convert Year to string for chart

        # Pivot for chart
        forecast_chart_data = final_combined_df.pivot_table(index='Year', columns='Type', values='Count', aggfunc='sum').fillna(0)

        # Display updated line chart
        st.write("### Ähli görnüşler üçin birleşdirilen taryhy we çak edilýän maglumatlar")
        st.line_chart(forecast_chart_data)

        # Visualize Linear Fit for Each Type
        st.write("### Linear Fit Visualization for All Types")
        plt.figure(figsize=(12, 8))

        for faculty_type in selected_types:
            type_data = final_combined_df[final_combined_df['Type'] == faculty_type]
            historical_data = type_data[type_data['Year'].astype(int) <= 2024]
            future_data = type_data[type_data['Year'].astype(int) > 2024]

            # Plot historical data
            plt.scatter(historical_data['Year'], historical_data['Count'], label=f"{faculty_type} (taryhy)")

            # Plot forecasted data
            plt.plot(future_data['Year'], future_data['Count'], label=f"{faculty_type} (çaklama)")

        plt.xlabel("Ýyl")
        plt.ylabel("Sany")
        plt.title(" Alymlyk derejeleriniň görnüşleri üçin çyzykly laýyklyk")
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt)

    st.write("### Alymlyk derejeleriň ýyl we görnüşi boýunça hasaplamalar")
    bar_chart_data = filtered_df.groupby(['Year', 'Type'])['Count'].sum().unstack(fill_value=0)
    st.bar_chart(bar_chart_data)

    st.write("### Wagtyň geçmegi bilen alymlyk derejeleriniň ýylylyk kartasy")
    heatmap_data = filtered_df.pivot_table(index='Year', columns='Type', values='Count', aggfunc='sum', fill_value=0)
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu")
    plt.title("alymlyk derejeleriniň ýylylyk kartasy")
    plt.xlabel("alymlyk derejesiniň görnüşi")
    plt.ylabel("Ýyl")
    st.pyplot(plt)


    col1, col2, col3 = st.columns(3)

            # Add content to each column
    with col2:
        st.write("### Alymlyk derejeleriniň göterim paýy")

        # Calculate total counts for each type
        specific_types = ['professor', 'dosent', 'ylymlaryň kandidaty', 'ylymlaryň doktory']
        distribution_data = filtered_df[filtered_df['Type'].isin(specific_types)]
        distribution_summary = distribution_data.groupby('Type')['Count'].sum()

        # Calculate overall faculty count
        overall_faculty_count = long_df[
            long_df['Type'] == 'Alymlyk derejeli we alymlyk atly işgärleriň jemi sany'
        ]['Count'].sum()

        # Calculate percentage distribution
        distribution_percentages = (distribution_summary / overall_faculty_count) * 100

        # Plot pie chart
        plt.figure(figsize=(18, 8))
        plt.pie(distribution_percentages, labels=distribution_percentages.index, autopct='%1.1f%%', startangle=140, colors=["#f59393" , "#87cefa", "#f2f277", "#90ee90"], textprops={"fontsize": 20})
        # plt.title("Percentage Distribution of Faculty Types")
        st.pyplot(plt)




    st.write("### Uniwersitet ara alymlyk derejeleriniň paýlanyşy")

    # Filter data for specific types
    specific_types = ['professor', 'dosent', 'ylymlaryň kandidaty', 'ylymlaryň doktory']
    filtered_specific_types = filtered_df[filtered_df['Type'].isin(specific_types)]

    # Group data by University and Type
    university_type_data = filtered_specific_types.groupby(['University', 'Type'])['Count'].sum().unstack(fill_value=0)

    # Plot grouped bar chart
    university_type_data.plot(kind='bar', figsize=(12, 8))
    plt.title("Uniwersitet boýunça alymlyk derejeleriniň paýlanyşy")
    plt.xlabel("Uniwersitet")
    plt.ylabel("Alymlyk derejeleriniň sany")
    plt.xticks(rotation=45)
    plt.legend(title="Alymlyk derejeleriniň görnüşi")
    st.pyplot(plt)

    st.write("### Uniwersitetleriň her alymlyk derejesi boýunça göterim goşandy")

    # Filter data for specific types
    specific_types = ['professor', 'dosent', 'ylymlaryň kandidaty', 'ylymlaryň doktory']
    filtered_specific_types = filtered_df[filtered_df['Type'].isin(specific_types)]

    # Group data by University and Type
    university_type_data = filtered_specific_types.groupby(['University', 'Type'])['Count'].sum().unstack(fill_value=0)

    # Calculate percentage contribution
    percentage_contribution = university_type_data.div(university_type_data.sum(axis=0), axis=1) * 100

    # Use Streamlit's bar chart to visualize
    st.bar_chart(percentage_contribution)

if page == "Halkara indedeksli zurnallar":
    st.title("Ýokary okuw mekdepleriniň Daşary ýurt neşirlerinde çap edilen hem-de çap edilmegi meýilleşdirilýän ylmy makalalarynyň sany barada maglumat")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

     # Load Data
    long_df = pd.read_csv('makalalar_restructured_data.csv')
    long_df.fillna(0, inplace=True)

    # Ensure Year is an integer
    long_df["Year"] = long_df["Year"].astype(str)

    # Sidebar Filters
    universities = sorted(long_df['University'].unique())
    universities.insert(0, "Ählisi")  # Add "ALL" option at the beginning

    selected_universities = st.multiselect("Uniwersitet saýlaň", universities, default="Ählisi")
    selected_types = st.multiselect("Makala görnüşi saýlaň", sorted(long_df['Type'].unique()), default=long_df['Type'].unique())

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Filter Data
    if "Ählisi" in selected_universities:
        filtered_df = long_df[long_df['Type'].isin(selected_types)]
    else:
        filtered_df = long_df[(long_df['University'].isin(selected_universities)) & (long_df['Type'].isin(selected_types))]

    # Line Chart for Historical Data
    st.write("### Halkara indedeksli makalalaryň ýyllar boýy tendensiýalary")
    if not filtered_df.empty:
        line_chart_data = filtered_df.pivot_table(index='Year', columns='Type', values='Count', aggfunc='sum').fillna(0)
        st.line_chart(line_chart_data)
    else:
        st.write("Saýlananlar üçin maglumat ýok.")

    # Forecast Button
    if st.button("2030-njy ýyla çenli çaklama"):
        st.write("### Halkara indedeksli makalalaryň çaklama tendensiýalary (2025–2030)")

        # Prepare data for each type and forecast separately
        forecast_results = []
        combined_data = []

        for faculty_type in selected_types:
            type_data = filtered_df[filtered_df['Type'] == faculty_type]
            regression_data = type_data.groupby('Year')['Count'].sum().reset_index()

            # Prepare data for regression
            X = regression_data['Year'].values.reshape(-1, 1)
            y = regression_data['Count'].values

            if len(X) > 1:  # Ensure there is enough data for regression
                # Fit Linear Regression
                model = LinearRegression()
                model.fit(X, y)

                m = model.coef_[0]
                b = model.intercept_

                # Forecast future years
                future_years = np.arange(2025, 2031).reshape(-1, 1)
                future_counts = model.predict(future_years)
                # st.write(f"### Forecasting Formula: Faculty Count = {m:.2f} × Year + {b:.2f}")

                # Create forecast DataFrame
                forecast_df = pd.DataFrame({
                    'Year': future_years.flatten(),
                    'Count': future_counts,
                    'Type': faculty_type
                })

                # Combine historical and forecasted data
                combined_df = pd.concat([regression_data.assign(Type=faculty_type), forecast_df], ignore_index=True)
                combined_data.append(combined_df)

        # Combine all types into one DataFrame
        final_combined_df = pd.concat(combined_data, ignore_index=True)
        final_combined_df['Year'] = final_combined_df['Year'].astype(str)  # Convert Year to string for chart

        # Pivot for chart
        forecast_chart_data = final_combined_df.pivot_table(index='Year', columns='Type', values='Count', aggfunc='sum').fillna(0)

        # Display updated line chart
        st.write("### Ähli görnüşler üçin birleşdirilen taryhy we çak edilýän maglumatlar")
        st.line_chart(forecast_chart_data)

        # Visualize Linear Fit for Each Type
        st.write("### Linear Fit Visualization for All Types")
        plt.figure(figsize=(12, 8))

        for faculty_type in selected_types:
            type_data = final_combined_df[final_combined_df['Type'] == faculty_type]
            historical_data = type_data[type_data['Year'].astype(int) <= 2024]
            future_data = type_data[type_data['Year'].astype(int) > 2024]

            # Plot historical data
            plt.scatter(historical_data['Year'], historical_data['Count'], label=f"{faculty_type} (taryhy)")

            # Plot forecasted data
            plt.plot(future_data['Year'], future_data['Count'], label=f"{faculty_type} (çaklama)")

        plt.xlabel("Ýyl")
        plt.ylabel("Sany")
        plt.title("Halkara indedeksli makalalaryň görnüşleri üçin çyzykly laýyklyk")
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt)

    st.write("### Halkara indedeksli makalalryň ýyl we görnüşi boýunça hasaplamalar")
    bar_chart_data = filtered_df.groupby(['Year', 'Type'])['Count'].sum().unstack(fill_value=0)
    st.bar_chart(bar_chart_data)

    st.write("### Wagtyň geçmegi bilen halkara indedeksli makalalaryň ýylylyk kartasy")
    heatmap_data = filtered_df.pivot_table(index='Year', columns='Type', values='Count', aggfunc='sum', fill_value=0)
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu")
    plt.title("Halkara indedeksli makalalaryň ýylylyk kartasy")
    plt.xlabel("Halkara indedeksli makalalaryň görnüşi")
    plt.ylabel("Ýyl")
    st.pyplot(plt)


    col1, col2, col3 = st.columns(3)

            # Add content to each column
    with col2:
        st.write("### Halkara indedeksli makalalaryň göterim paýy")

        # Calculate total counts for each type
        specific_types = ['Elibrary.ru', 'РИНЦ', 'Web of Science ýa-da Scopus']
        distribution_data = filtered_df[filtered_df['Type'].isin(specific_types)]
        distribution_summary = distribution_data.groupby('Type')['Count'].sum()

        # Calculate overall faculty count
        overall_faculty_count = long_df[
            long_df['Type'] == 'Jemi'
        ]['Count'].sum()

        # Calculate percentage distribution
        distribution_percentages = (distribution_summary / overall_faculty_count) * 100

        # Plot pie chart
        plt.figure(figsize=(18, 8))
        plt.pie(distribution_percentages, labels=distribution_percentages.index, autopct='%1.1f%%', startangle=140, colors=["#f59393" , "#87cefa", "#f2f277"], textprops={"fontsize": 20})
        # plt.title("Percentage Distribution of Faculty Types")
        st.pyplot(plt)




    st.write("### Uniwersitet ara halkara indedeksli makalalaryň paýlanyşy")

    # Filter data for specific types
    specific_types = ['Elibrary.ru', 'РИНЦ', 'Web of Science ýa-da Scopus']
    filtered_specific_types = filtered_df[filtered_df['Type'].isin(specific_types)]

    # Group data by University and Type
    university_type_data = filtered_specific_types.groupby(['University', 'Type'])['Count'].sum().unstack(fill_value=0)

    # Plot grouped bar chart
    university_type_data.plot(kind='bar', figsize=(12, 8))
    plt.title("Uniwersitet boýunça halkara indedeksli makalalaryň paýlanyşy")
    plt.xlabel("Uniwersitet")
    plt.ylabel("Halkara indedeksli makalalaryň sany")
    plt.xticks(rotation=45)
    plt.legend(title="Halkara indedeksli makalalaryň görnüşi")
    st.pyplot(plt)

    st.write("### Uniwersitetleriň her halkara indedeksli makalalar boýunça göterim goşandy")

    # Filter data for specific types
    specific_types = ['Elibrary.ru', 'РИНЦ', 'Web of Science ýa-da Scopus']
    filtered_specific_types = filtered_df[filtered_df['Type'].isin(specific_types)]

    # Group data by University and Type
    university_type_data = filtered_specific_types.groupby(['University', 'Type'])['Count'].sum().unstack(fill_value=0)

    # Calculate percentage contribution
    percentage_contribution = university_type_data.div(university_type_data.sum(axis=0), axis=1) * 100

    # Use Streamlit's bar chart to visualize
    st.bar_chart(percentage_contribution)

if page ==  "Maddy enjamlaýyn üpjünçilik":
    st.title("Ýokary okuw mekdepleriniň Maddy-enjamlaýyn binýady barada maglumat")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

     # Load Data
    long_df = pd.read_csv('maddy_restructured_data.csv')
    long_df.fillna(0, inplace=True)

    # Ensure Year is an integer
    long_df["Year"] = long_df["Year"].astype(str)

    # Sidebar Filters
    universities = sorted(long_df['University'].unique())
    universities.insert(0, "Ählisi")  # Add "ALL" option at the beginning

    selected_universities = st.multiselect("Uniwersitet saýlaň", universities, default="Ählisi")
    selected_types = st.multiselect("Enjam görnüşi saýlaň", sorted(long_df['Type'].unique()), default=long_df['Type'].unique())

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Filter Data
    if "Ählisi" in selected_universities:
        filtered_df = long_df[long_df['Type'].isin(selected_types)]
    else:
        filtered_df = long_df[(long_df['University'].isin(selected_universities)) & (long_df['Type'].isin(selected_types))]

    # Line Chart for Historical Data
    st.write("### Enjamlaryň ýyllar boýy tendensiýalary")
    if not filtered_df.empty:
        line_chart_data = filtered_df.pivot_table(index='Year', columns='Type', values='Count', aggfunc='sum').fillna(0)
        st.line_chart(line_chart_data)
    else:
        st.write("Saýlananlar üçin maglumat ýok.")

    # Forecast Button
    if st.button("2030-njy ýyla çenli çaklama"):
        st.write("### Enjamlaryňçaklama tendensiýalary (2029–2030)")

        # Prepare data for each type and forecast separately
        forecast_results = []
        combined_data = []

        for faculty_type in selected_types:
            type_data = filtered_df[filtered_df['Type'] == faculty_type]
            regression_data = type_data.groupby('Year')['Count'].sum().reset_index()

            # Prepare data for regression
            X = regression_data['Year'].values.reshape(-1, 1)
            y = regression_data['Count'].values

            if len(X) > 1:  # Ensure there is enough data for regression
                # Fit Linear Regression
                model = LinearRegression()
                model.fit(X, y)

                m = model.coef_[0]
                b = model.intercept_

                # Forecast future years
                future_years = np.arange(2029, 2031).reshape(-1, 1)
                future_counts = model.predict(future_years)
                # st.write(f"### Forecasting Formula: Faculty Count = {m:.2f} × Year + {b:.2f}")

                # Create forecast DataFrame
                forecast_df = pd.DataFrame({
                    'Year': future_years.flatten(),
                    'Count': future_counts,
                    'Type': faculty_type
                })

                # Combine historical and forecasted data
                combined_df = pd.concat([regression_data.assign(Type=faculty_type), forecast_df], ignore_index=True)
                combined_data.append(combined_df)

        # Combine all types into one DataFrame
        final_combined_df = pd.concat(combined_data, ignore_index=True)
        final_combined_df['Year'] = final_combined_df['Year'].astype(str)  # Convert Year to string for chart

        # Pivot for chart
        forecast_chart_data = final_combined_df.pivot_table(index='Year', columns='Type', values='Count', aggfunc='sum').fillna(0)

        # Display updated line chart
        st.write("### Ähli görnüşler üçin birleşdirilen taryhy we çak edilýän maglumatlar")
        st.line_chart(forecast_chart_data)

        # Visualize Linear Fit for Each Type
        st.write("### Linear Fit Visualization for All Types")
        plt.figure(figsize=(12, 8))

        for faculty_type in selected_types:
            type_data = final_combined_df[final_combined_df['Type'] == faculty_type]
            historical_data = type_data[type_data['Year'].astype(int) <= 2024]
            future_data = type_data[type_data['Year'].astype(int) > 2024]

            # Plot historical data
            plt.scatter(historical_data['Year'], historical_data['Count'], label=f"{faculty_type} (taryhy)")

            # Plot forecasted data
            plt.plot(future_data['Year'], future_data['Count'], label=f"{faculty_type} (çaklama)")

        plt.xlabel("Ýyl")
        plt.ylabel("Sany")
        plt.title("Enjamlaryň görnüşleri üçin çyzykly laýyklyk")
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(plt)

    st.write("### Enjamlaryň ýyl we görnüşi boýunça hasaplamalar")
    bar_chart_data = filtered_df.groupby(['Year', 'Type'])['Count'].sum().unstack(fill_value=0)
    st.bar_chart(bar_chart_data)

    st.write("### Wagtyň geçmegi bilen enjamlaryň  ýylylyk kartasy")
    heatmap_data = filtered_df.pivot_table(index='Year', columns='Type', values='Count', aggfunc='sum', fill_value=0)
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu")
    plt.title("Enjamlaryň ýylylyk kartasy")
    plt.xlabel("Enjamlaryň görnüşi")
    plt.ylabel("Ýyl")
    st.pyplot(plt)


    col1, col2, col3 = st.columns(3)

            # Add content to each column
    with col2:
        st.write("### Enjamlaryň göterim paýy")

        # Calculate total counts for each type
        specific_types = ['Kompýuter tehnikalar', 'Interaktiw tagtalar', 'Proýektorlar', 'Interaktiw işjeň paneller', 'VR enjamlar', 'AR enjamlar']
        distribution_data = filtered_df[filtered_df['Type'].isin(specific_types)]
        distribution_summary = distribution_data.groupby('Type')['Count'].sum()

        # Calculate overall faculty count
        overall_faculty_count = long_df[
            long_df['Type'] == 'Jemi'
        ]['Count'].sum()

        # Calculate percentage distribution
        distribution_percentages = (distribution_summary / overall_faculty_count) * 100

        # Plot pie chart
        plt.figure(figsize=(18, 8))
        plt.pie(distribution_percentages, labels=distribution_percentages.index, autopct='%1.1f%%', startangle=140, colors=["#f59393" , "#87cefa", "#f2f277", "#90ee90", "#e193f5", "#98f5eb"], textprops={"fontsize": 20}, pctdistance=1.2,labeldistance=1.8)
        # plt.title("Percentage Distribution of Faculty Types")
        st.pyplot(plt)




    st.write("### Uniwersitet ara enjamlaryň paýlanyşy")

    # Filter data for specific types
    specific_types = ['Kompýuter tehnikalar', 'Interaktiw tagtalar', 'Proýektorlar', 'Interaktiw işjeň paneller', 'VR enjamlar', 'AR enjamlar']
    filtered_specific_types = filtered_df[filtered_df['Type'].isin(specific_types)]

    # Group data by University and Type
    university_type_data = filtered_specific_types.groupby(['University', 'Type'])['Count'].sum().unstack(fill_value=0)

    # Plot grouped bar chart
    university_type_data.plot(kind='bar', figsize=(12, 8))
    plt.title("Uniwersitet boýunça enjamlaryň paýlanyşy")
    plt.xlabel("Uniwersitet")
    plt.ylabel("Enjamlaryň sany")
    plt.xticks(rotation=45)
    plt.legend(title="Enjamlaryňgörnüşi")
    st.pyplot(plt)

    st.write("### Uniwersitetleriň her enjam boýunça göterim goşandy")

    # Filter data for specific types
    specific_types = ['Kompýuter tehnikalar', 'Interaktiw tagtalar', 'Proýektorlar', 'Interaktiw işjeň paneller', 'VR enjamlar', 'AR enjamlar']
    filtered_specific_types = filtered_df[filtered_df['Type'].isin(specific_types)]

    # Group data by University and Type
    university_type_data = filtered_specific_types.groupby(['University', 'Type'])['Count'].sum().unstack(fill_value=0)

    # Calculate percentage contribution
    percentage_contribution = university_type_data.div(university_type_data.sum(axis=0), axis=1) * 100

    # Use Streamlit's bar chart to visualize
    st.bar_chart(percentage_contribution)

if page == "Quota":
    st.title("Türkmenistanda ýokary bilimi ösdürmegiň Strategiýasyny taýýarlamak üçin MAGLUMATLAR")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("Bap: Mekdep uçurymlarynyň seljermeleri (2015–2042)"):

        # Page Title
        st.title("Mekdep uçurymlarynyň seljermeleri (2015–2042)")

        # Load Data
        graduates_data = pd.read_csv('restructured_school_graduates.csv')  # Replace with your restructured file
        graduates_data.fillna(0, inplace=True)
        graduates_data["Year"] = graduates_data["Year"].astype(str)

        # Region Filter (No "Ählisi", includes "JEMI" as total)
        regions = sorted(graduates_data['Region'].unique())
        selected_regions = st.multiselect("Welaýat saýlaň", regions, default=regions)

        # Year Filter (Includes "Ählisi" for all years)
        years = sorted(graduates_data['Year'].unique())
        years.insert(0, "Ählisi")  # Add "All" option
        selected_years = st.multiselect("Ýyllary saýlaň", years, default="Ählisi")

        # Filter Data
        if "Ählisi" in selected_years:
            filtered_df = graduates_data[graduates_data['Region'].isin(selected_regions)]
        else:
            filtered_df = graduates_data[(graduates_data['Region'].isin(selected_regions)) & (graduates_data['Year'].isin(selected_years))]

        # Line Chart for Historical Data
        st.write("### Mekdep uçurymlarynyň Ýyllar Boýy Tendensiýalary")
        if not filtered_df.empty:
            line_chart_data = filtered_df.pivot_table(index='Year', columns='Region', values='Graduates', aggfunc='sum').fillna(0)
            st.line_chart(line_chart_data)
        else:
            st.write("Saýlananlar üçin maglumat ýok.")

        # Pie Chart for Regional Contribution
        col1, col2, col3 = st.columns(3)

        # Add content to each column
        with col2:
            st.write("### Welaýatlaryň Göterim Paýy")

            # Specify the regions for the pie chart
            specific_regions = ['AHAL', 'BALKAN', 'DAŞOGUZ', 'LEBAP', 'MARY', 'AŞGABAT']
            distribution_data = filtered_df[filtered_df['Region'].isin(specific_regions)]

            # Check if there is data to process
            if distribution_data.empty:
                st.write("Saýlanan welaýatlar üçin maglumat ýok.")
            else:
                # Calculate total graduates per region
                distribution_summary = distribution_data.groupby('Region')['Graduates'].sum()

                # Calculate overall graduates
                overall_graduates = distribution_summary.sum()

                # Check for zero total graduates to avoid division errors
                if overall_graduates == 0:
                    st.write("Maglumatlar bar, ýöne welayat ara yok, yokarky diagramma esaslanyp bilersiňiz.")
                else:
                    # Calculate percentage distribution
                    distribution_percentages = (distribution_summary / overall_graduates) * 100

                    # Debugging (optional)
                    # st.write("Distribution Summary:", distribution_summary)
                    # st.write("Percentage Distribution:", distribution_percentages)

                    # Plot pie chart
                    plt.figure(figsize=(18, 8))
                    plt.pie(distribution_percentages, labels=distribution_percentages.index, autopct='%1.1f%%',
                            startangle=140, colors=["#f59393", "#87cefa", "#f2f277", "#90ee90", "#ffcccb", "#aaffc3"],
                            textprops={"fontsize": 20})
                    st.pyplot(plt)


        # Graduates Grouped Bar Chart
        st.write("### Mekdep Uçurymlarynyň Ýyl we Welaýat boýunça Hasaplamalar")
        bar_chart_data = filtered_df.groupby(['Year', 'Region'])['Graduates'].sum().unstack(fill_value=0)
        st.bar_chart(bar_chart_data)

        # Graduates Heatmap
        st.write("### Wagtyň Geçmegi bilen Mekdep Uçurymlarynyň Ýylylyk Kartasy")
        heatmap_data = filtered_df.pivot_table(index='Year', columns='Region', values='Graduates', aggfunc='sum', fill_value=0)
        plt.figure(figsize=(12, 8))
        sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu")
        plt.title("Mekdep Uçurymlarynyň Ýylylyk Kartasy", fontsize=16)
        plt.xlabel("Welaýat", fontsize=14)
        plt.ylabel("Ýyl", fontsize=14)
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        st.pyplot(plt)


        # Regional Lat/Lon Data
        region_coords = pd.DataFrame({
            'Region': ['AHAL', 'BALKAN', 'DAŞOGUZ', 'LEBAP', 'MARY', 'AŞGABAT'],
            'Latitude': [38.982647, 39.5296023, 41.83, 39.12, 37.6, 37.95],
            'Longitude': [58.213583, 54.2990248, 59.96, 63.57, 61.83, 58.38]
        })
        # Filter out "JEMI" from the regions
        # Filter out "JEMI" from the regions
        filtered_df = filtered_df[filtered_df['Region'] != 'JEMI']

        # Map Visualization
        st.write("### Welaýatlaryň Ýerleşiş Kartasy (Uçurymlar Bilen)")

        if not filtered_df.empty:
            # Aggregate data for the selected years
            map_data = filtered_df.groupby('Region', as_index=False)['Graduates'].sum()

            # Merge with region coordinates
            map_data = pd.merge(map_data, region_coords, on="Region")

            if map_data.empty:
                st.write("Maglumat ýok!")
            else:
                # Plot the map
                st.pydeck_chart(
                    pdk.Deck(
                        map_style="mapbox://styles/mapbox/light-v9",
                        initial_view_state=pdk.ViewState(
                            latitude=38.5, longitude=59, zoom=6, pitch=0  # Flat map (no tilt)
                        ),
                        layers=[
                            pdk.Layer(
                                "ScatterplotLayer",
                                data=map_data,
                                get_position="[Longitude, Latitude]",
                                get_radius="Graduates *  1",  # Adjust radius based on data
                                get_fill_color="[0, 255, 0, 144]",  # Red with transparency
                                pickable=True,
                            )
                        ],
                        tooltip={"text": "Region: {Region}\nGraduates: {Graduates}"}
                    )
                )
        else:
            st.write("Saýlanan maglumat ýok!")


        # Calculate YoY Change for JEMI Graduates
        st.write("### Mekdep Uçurymlarynyň Ýyl-ýyla Göterim Üýtgeýşi")
        jemi_trend = graduates_data[graduates_data['Region'] == 'JEMI'].copy()
        jemi_trend['Graduates'] = jemi_trend['Graduates'].astype(float)  # Ensure numeric type

        if 'Graduates' in jemi_trend.columns and (jemi_trend['Graduates'] > 0).any():
            # Calculate Year-over-Year percentage change
            jemi_trend['YoY Change (%)'] = jemi_trend['Graduates'].pct_change() * 100

            # Plot the YoY Change
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(
                x='Year', y='YoY Change (%)', data=jemi_trend, palette="viridis", ax=ax
            )
            ax.axhline(0, color="gray", linestyle="--", linewidth=1)
            ax.set_title("Mekdep Uçurymlarynyň Ýyl-ýyla Göterim Üýtgeýşi", fontsize=16, weight='bold')
            ax.set_xlabel("Ýyl", fontsize=14)
            ax.set_ylabel("Göterim Üýtgeýşi (%)", fontsize=14)
            st.pyplot(fig)

            # Display the percentage changes as a DataFrame below the plot
            st.write("### Göterim Üýtgeýşi Maglumatlary")
            st.dataframe(jemi_trend[['Year', 'Graduates', 'YoY Change (%)']].reset_index(drop=True))
        else:
            st.warning("JEMI uçurymlar boýunça maglumat ýok.")

    with st.expander("Bap: ÝOM kwota seljermeleri (2015–2024)"):
        # Title for the dashboard
        st.title("ÝOM kwota seljermeleri (2015–2024)")
        data = pd.read_csv('Q_all_restructured_data.csv')  # Replace with your restructured file
        data["Ýyl"] = data["Ýyl"].astype(str)
        # Replace values in 'Student Type' column
        data["Talyp görnüşi"] = data["Talyp görnüşi"].replace({
            "Scholarship": "BŽ",
            "Non Scholarship": "Tölegli"
        })




        # Multiselect for filters with "ALL" option
        years = ["Ählisi"] + sorted(data['Ýyl'].unique())
        universities = ["Ählisi"] + sorted(data['Uniwersitet'].unique())
        faculties = ["Ählisi"] + sorted(data['Ugur'].unique())
        regions = ["Ählisi"] + sorted(data['Welaýat'].unique())
        study_types = ["Ählisi"] + sorted(data['Hünär'].unique())
        student_types = ["Ählisi"] + sorted(data['Talyp görnüşi'].unique())

        col1, col2, col3 = st.columns(3)

        # Add content to each column
        with col1:
            selected_years = st.multiselect("Ýyl saýlaň", options=years, default="Ählisi")
        with col2:
            selected_universities = st.multiselect("Uniwersitet saýlaň", options=universities, default="Ählisi")
        with col3:
            selected_faculties = st.multiselect("Ugur saýlaň", options=faculties, default="Ählisi")


        col1, col2, col3 = st.columns(3)

        with col1:
            selected_regions = st.multiselect("Welaýat saýlaň", options=regions, default="Ählisi")
        with col2:
            selected_study_types = st.multiselect("Hünär saýlaň", options=study_types, default="Ählisi")
        with col3:
            selected_student_types = st.multiselect("Talyp görnüşini saýlaň", options=student_types, default="Ählisi")

        # Apply filters
        filtered_data = data.copy()



        if "Ählisi" not in selected_years:
            filtered_data = filtered_data[filtered_data['Ýyl'].isin(selected_years)]

        if "Ählisi" not in selected_universities:
            filtered_data = filtered_data[filtered_data['Uniwersitet'].isin(selected_universities)]

        if "Ählisi" not in selected_faculties:
            filtered_data = filtered_data[filtered_data['Ugur'].isin(selected_faculties)]

        if "Ählisi" not in selected_regions:
            filtered_data = filtered_data[filtered_data['Welaýat'].isin(selected_regions)]

        if "Ählisi" not in selected_study_types:
            filtered_data = filtered_data[filtered_data['Hünär'].isin(selected_study_types)]

        if "Ählisi" not in selected_student_types:
            filtered_data = filtered_data[filtered_data['Talyp görnüşi'].isin(selected_student_types)]

        # Display Filtered Data
        # st.write("### Filtered Data", filtered_data)

        university_coords = pd.DataFrame({
                    'Uniwersitet': ['TDU', 'HYYÖU', 'HNGU', 'TDBGI', 'TDLU', 'TDBSI', 'HGI', 'TDMaI', 'TDYDI', 'TTII', 'TMDDI', 'TITU', 'TITUKI', 'TOHU', 'TDMI', 'TMK', 'TDÇA', 'SSTDMI', 'TDEI', 'TOHI', 'HAA'],
                    'Latitude': [37.9308047, 37.9311669, 37.877472, 37.9242034, 37.8784063, 37.9187744, 37.9293351, 37.9211045, 37.8998289, 37.9420864, 37.9507819, 37.9612627, 38.0434327, 37.9526083, 37.8962383, 37.9373864, 37.936482, 39.0885626, 37.2584823, 41.8280269, 38.0550484],
                    'Longitude': [58.3848102, 58.3876358, 58.3861546, 58.4254617, 58.3641239, 58.3764255, 58.3887706, 58.3903317, 58.362772, 58.3784814, 58.3526043, 58.3246639, 58.1660508, 58.3420542, 58.3656084, 58.3801838, 58.3695422, 63.5794743, 62.3403715, 59.9348195, 58.047581]
                })

        region_coords = pd.DataFrame({
            'Welaýat': ['AHAL', 'BALKAN', 'DAŞOGUZ', 'LEBAP', 'MARY', 'AŞGABAT'],
            'Latitude': [38.982647, 39.5296023, 41.83, 39.12, 37.6, 37.95],
            'Longitude': [58.213583, 54.2990248, 59.96, 63.57, 61.83, 58.38]
        })


        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


        # Regional Map
        # Regional Map

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Welaýat ara karta")
            if not filtered_data.empty:
                # Aggregate data for the selected regions
                map_data = filtered_data.groupby('Welaýat', as_index=False)['Kwota'].sum()

                # Merge with region coordinates
                map_data = pd.merge(map_data, region_coords, on="Welaýat", how="inner")

                if map_data.empty:
                    st.write("No region data available!")
                else:
                    # Plot the map
                    st.pydeck_chart(
                        pdk.Deck(
                            map_style="mapbox://styles/mapbox/light-v9",
                            initial_view_state=pdk.ViewState(
                                latitude=38.5, longitude=59, zoom=6, pitch=0  # Flat map (no tilt)
                            ),
                            layers=[
                                pdk.Layer(
                                    "ScatterplotLayer",
                                    data=map_data,
                                    get_position="[Longitude, Latitude]",
                                    get_radius="Kwota * 7",  # Adjust radius based on data
                                    get_fill_color="[0, 255, 0, 144]",  # Green with transparency
                                    pickable=True,
                                )
                            ],
                            tooltip={"text": "Welaýat: {Welaýat}\Kwota: {Kwota}"}
                        )
                    )
            else:
                st.write("No region data available!")

        with col2:
            st.write("### Uniwersitet ara kartasy")
            if not filtered_data.empty:
                # Aggregate data for the selected universities
                university_map_data = filtered_data.groupby('Uniwersitet', as_index=False)['Kwota'].sum()

                # Merge with university coordinates
                university_map_data = pd.merge(university_map_data, university_coords, on="Uniwersitet", how="inner")

                if university_map_data.empty:
                    st.write("No university data available!")
                else:
                    # Plot the map
                    st.pydeck_chart(
                        pdk.Deck(
                            map_style="mapbox://styles/mapbox/light-v9",
                            initial_view_state=pdk.ViewState(
                                latitude=38, longitude=59, zoom=5, pitch=0  # Flat map
                            ),
                            layers=[
                                pdk.Layer(
                                    "ScatterplotLayer",
                                    data=university_map_data,
                                    get_position="[Longitude, Latitude]",
                                    get_radius="Kwota * 10",  # Adjust radius based on data
                                    get_fill_color="[0, 0, 255, 144]",  # Blue with transparency
                                    pickable=True,
                                )
                            ],
                            tooltip={"text": "Uniwersitet: {Uniwersitet}\Kwota: {Kwota}"}
                        )
                    )
            else:
                st.write("No university data available!")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)



        # Create a reusable pie chart function
        def create_pie_chart(data, group_by, title):
            grouped_data = data.groupby(group_by)['Kwota'].sum()
            percentages = (grouped_data / grouped_data.sum()) * 100

            # Plot
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(
                percentages,
                labels=percentages.index,
                autopct='%1.1f%%',
                startangle=140,
                colors=["#f59393", "#87cefa", "#f2f277", "#90ee90", "#ffcccb", "#aaffc3"]
            )
            ax.set_title(title, fontsize=16)
            st.pyplot(fig)

        col1, col2, col3 = st.columns(3)
        # Pie Chart for Regions
        with col1:
            create_pie_chart(filtered_data, 'Welaýat', "Welaýat boýunça kwota paýlanyşy")
        # Pie Chart for Student Types
        with col2:
            create_pie_chart(filtered_data, 'Talyp görnüşi', "Talyp görnüşi boýunça kwota paýlanyşy (BZ vs. Tölegli)")
        with col3:
            create_pie_chart(filtered_data, 'Hünär', "Hünäri boýunça kwota paýlanyşy")


        col1, col2= st.columns(2)
        # Pie Chart for Faculties (Ugurlar)
        with col1:
            create_pie_chart(filtered_data, 'Ugur', "Ugur boýunça kwota paýlanyşy")

        # Pie Chart for Universities
        with col2:
            create_pie_chart(filtered_data, 'Uniwersitet', "Uniwersitet boýunça kwota paýlanyşy")




        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.write("### Derňemek üçin üýtgeýji saýlaň")
        group_by_options = ["Uniwersitet", "Ugur", "Welaýat", "Hünär", "Talyp görnüşi"]
        selected_group_by = st.multiselect("Üýtgeýjileri saýlaň", options=group_by_options, default=["Uniwersitet"])

        if selected_group_by:
            # Aggregate Data
            line_chart_data = filtered_data.groupby(["Ýyl"] + selected_group_by, as_index=False)['Kwota'].sum()

            # Pivot Data for Line Chart
            line_chart_pivot = line_chart_data.pivot_table(index="Ýyl", columns=selected_group_by, values="Kwota", aggfunc="sum").fillna(0)

            # Display Line Chart
            st.write(f"### Kwota tendensiýasy - {', '.join(selected_group_by)}")
            st.line_chart(line_chart_pivot)
        else:
            st.warning("Please select at least one variable to group by.")


        st.write("### Ýylyň dowamynda göterim üýtgemeginiň derňewi")
        # Dynamic Grouping Variables
        selected_group_by_pct = st.multiselect("Üýtgeýji saýlaň", options=group_by_options, default=["Uniwersitet"])

        if selected_group_by_pct:
            # Aggregate Data for Quota
            percentage_data = filtered_data.groupby(["Ýyl"] + selected_group_by_pct, as_index=False)['Kwota'].sum()

            # Pivot Data for Percentage Change Calculation
            percentage_pivot = percentage_data.pivot_table(index="Ýyl", columns=selected_group_by_pct, values="Ýyl", aggfunc="sum").fillna(0)

            # Calculate Year-over-Year Percentage Change
            percentage_change = percentage_pivot.pct_change().fillna(0) * 100

            # Display Percentage Change Line Chart
            st.write(f"### Göterim üýtgemegi -  {', '.join(selected_group_by_pct)}")
            st.line_chart(percentage_change)

            # Display Data Table for Reference
            st.write("### Göterim üýtgemegi ")
            st.dataframe(percentage_change)
        else:
            st.warning("Please select at least one variable to group by.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        # Pivot data for heatmap

        with col1:
            heatmap_data = filtered_data.pivot_table(index='Welaýat', columns='Ýyl', values='Kwota', aggfunc='sum', fill_value=0)

            # Plot Heatmap
            st.write("###  Welaýat we ýyl boýunça kwota ýylylyk kartasy")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", cbar=True, linewidths=.5, ax=ax)
            ax.set_title("Kwota ýylylyk kartasy")
            ax.set_xlabel("Ýyl")
            ax.set_ylabel("Welaýat")
            st.pyplot(fig)

        with col2:
            heatmap_data = filtered_data.pivot_table(index='Uniwersitet', columns='Ýyl', values='Kwota', aggfunc='sum', fill_value=0)

            st.write("### Uniwersitet we ýyl boýunça kwota ýylylyk kartasy")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", cbar=True, linewidths=.5, ax=ax)
            ax.set_title("Kwota ýylylyk kartasy")
            ax.set_xlabel("Ýyl")
            ax.set_ylabel("Uniwersitet")
            st.pyplot(fig)

        with col3:
            heatmap_data = filtered_data.pivot_table(index='Talyp görnüşi', columns='Ýyl', values='Kwota', aggfunc='sum', fill_value=0)

            st.write("### Talyp görnüşi we ýyl boýunça kwota ýylylyk kartasy")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", cbar=True, linewidths=.5, ax=ax)
            ax.set_title("kwota ýylylyk kartasy")
            ax.set_xlabel("Ýyl")
            ax.set_ylabel("Talyp görnüşi")
            st.pyplot(fig)



        # Prepare Data
        # Prepare the sunburst data
        sunburst_data = filtered_data[filtered_data['Kwota'] > 0].groupby(['Uniwersitet', 'Ugur', 'Welaýat'], as_index=False)['Kwota'].sum()
        st.write("### Uniwersitetlerde, ugurlarda we welaýatlarda kwota paýlanyşy")
        if sunburst_data.empty:
            st.warning("No data available to display. Please refine your filters.")
        else:
            fig = px.sunburst(
                data_frame=sunburst_data,
                path=['Uniwersitet', 'Ugur', 'Welaýat'],
                values='Kwota',
                # title="Uniwersitetlerde, fakultetlerde we welaýatlarda kwota paýlanyşy",
                color='Kwota',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig)


        # Group Data for Bubble Chart
        bubble_data = filtered_data.groupby(['Uniwersitet', 'Ugur'])['Kwota'].sum().reset_index()

        # Plot Bubble Chart
        st.write("### Kwota paýlanyşynyň köpürjik diagrammasy")
        fig = px.scatter(
            bubble_data,
            x='Uniwersitet',
            y='Ugur',
            size='Kwota',
            color='Kwota',
            # title="Bubble Chart: Quota Distribution",
            labels={'Kwota': 'Kwota'},
            hover_data=['Kwota']
        )
        st.plotly_chart(fig)

        # Ýyl,Uniwersitet,Ugur,Welaýat,Hünär,Talyp görnüşi,Kwota


        # # Group and Pivot Data for Stacked Bar
        # stacked_data = filtered_data.groupby(['Ýyl', 'Ugur', 'Hünär'])['Kwota'].sum().reset_index()
        # stacked_pivot = stacked_data.pivot(index='Ýyl', columns='Ugur', values='Kwota').fillna(0)

        # # Plot Stacked Bar Chart
        # st.write("### Stacked Bar Chart of Quota by Faculty")
        # fig, ax = plt.subplots(figsize=(12, 6))
        # stacked_pivot.plot(kind='bar', stacked=True, ax=ax, colormap='viridis')
        # ax.set_title("Quota Distribution by Faculty and Year")
        # ax.set_ylabel("Quota")
        # ax.set_xlabel("Year")
        # st.pyplot(fig)


        # Treemap Data


        # Prepare Data for Radar Chart
        # Group data by 'Ugur' and sum 'Kwota'
        # Group data by 'Ugur' and sum 'Kwota'
        grouped_data = filtered_data.groupby(['Ugur', 'Talyp görnüşi'])['Kwota'].sum().unstack(fill_value=0)
        topics = grouped_data.index.tolist()

        # Data layers (BZ and Tolegli)
        data_layers = [grouped_data[col].values for col in grouped_data.columns]
        labels = grouped_data.columns.tolist()

        # Add first element to close the radar chart loop
        angles = [n / float(len(topics)) * 2 * pi for n in range(len(topics))]
        angles += angles[:1]

        for idx in range(len(data_layers)):
            data_layers[idx] = list(data_layers[idx]) + [data_layers[idx][0]]  # Close loop

        # Plot radar chart
        fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={"polar": True})
        colors = ["blue", "orange"] # Customize colors for layers

        for idx, layer in enumerate(data_layers):
            ax.bar(
                angles,
                layer,
                color=colors[idx],
                alpha=0.6,
                width=0.35,
                label=labels[idx]
            )

        # Add labels for topics
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(topics, fontsize=16, rotation=45)

        # Title and Legend
        ax.set_title("Ugurlar we Talyp Görnüşleri", va='bottom', fontsize=22, pad=15)

        ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1), fontsize=16)

        # Increase radial labels font size
        ax.tick_params(axis='y', labelsize=16)

        # Streamlit Display
        st.pyplot(fig)


        # University-wise Tolegli and BZ Students
        st.write("### Uniwersitet ara talyp görnüşi")
        university_bar_data = filtered_data.groupby(['Uniwersitet', 'Talyp görnüşi'])['Kwota'].sum().unstack(fill_value=0)
        st.bar_chart(university_bar_data)

        # Ugur-wise Tolegli and BZ Students
        col1, col2= st.columns(2)
        with col1:
            st.write("### Ugurlar ara talyp görnüşi")
            ugur_bar_data = filtered_data.groupby(['Ugur', 'Talyp görnüşi'])['Kwota'].sum().unstack(fill_value=0)
            st.bar_chart(ugur_bar_data)

        with col2:

            st.write("### Welaýat ara talyp görnüşi ")
            university_ugur_bar_data = filtered_data.groupby(['Welaýat', 'Talyp görnüşi'])['Kwota'].sum().unstack(fill_value=0)
            st.bar_chart(university_ugur_bar_data)

        # University-wise Ugurlar
        st.write("###  Uniwersitet ara Ugurlar")
        university_ugur_bar_data = filtered_data.groupby(['Uniwersitet', 'Ugur'])['Kwota'].sum().unstack(fill_value=0)
        st.bar_chart(university_ugur_bar_data)

        st.write("### Uniwersitet ara Hünärler")
        university_ugur_bar_data = filtered_data.groupby(['Uniwersitet', 'Hünär'])['Kwota'].sum().unstack(fill_value=0)
        st.bar_chart(university_ugur_bar_data)

        st.write("### Uniwersitet ara welaýat")
        university_ugur_bar_data = filtered_data.groupby(['Uniwersitet', 'Welaýat'])['Kwota'].sum().unstack(fill_value=0)
        st.bar_chart(university_ugur_bar_data)



        # Ýyl,Uniwersitet,Ugur,Welaýat,Hünär,Talyp görnüşi,Kwota
        # Grouping data
        connections = filtered_data.groupby(['Welaýat', 'Uniwersitet', 'Talyp görnüşi'])['Kwota'].sum().reset_index()

        # Create source, target, and values for the Sankey diagram
        regions = connections['Welaýat'].unique()
        universities = connections['Uniwersitet'].unique()
        student_types = connections['Talyp görnüşi'].unique()

        region_index = {region: i for i, region in enumerate(regions)}
        university_index = {university: i + len(regions) for i, university in enumerate(universities)}
        student_type_index = {stype: i + len(regions) + len(universities) for i, stype in enumerate(student_types)}

        # Nodes
        nodes = list(regions) + list(universities) + list(student_types)

        # Links
        links = []
        for _, row in connections.iterrows():
            links.append({
                'source': region_index[row['Welaýat']],
                'target': university_index[row['Uniwersitet']],
                'value': row['Kwota']
            })
            links.append({
                'source': university_index[row['Uniwersitet']],
                'target': student_type_index[row['Talyp görnüşi']],
                'value': row['Kwota']
            })

        # Prepare Sankey Data
        sankey_data = go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes
            ),
            link=dict(
                source=[link['source'] for link in links],
                target=[link['target'] for link in links],
                value=[link['value'] for link in links]
            )
        )

        # Create the figure
        st.write("### Maglumat akymy diagrammasy")
        fig = go.Figure(sankey_data)
        # fig.update_layout(title_text="Sankey Diagram: Region to University to Student Type", font_size=10)

        # Display the figure in Streamlit
        st.plotly_chart(fig)




        # Define variable options
        variables = ['Ýyl', 'Uniwersitet', 'Ugur', 'Welaýat', 'Hünär', 'Talyp görnüşi', 'Kwota']

        st.write("### Sepme diagramma")

        # User selections
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X-oky üçin üýtgeýän ululuk saýlaň", variables, index=0)
            y_axis = st.selectbox("Y-oky üçin üýtgeýän ululuk saýlaň", variables, index=1)
        with col2:
            color_by = st.selectbox("Reňklendirmek üçin saýlaň", ["None"] + variables, index=0)


        # Prepare scatter plot

        if x_axis and y_axis:
            plot_data = filtered_data.copy()

            # Handle "None" options for color and size
            color = color_by if color_by != "None" else None
        
            # Create scatter plot
            fig = px.scatter(
                plot_data,
                x=x_axis,
                y=y_axis,
                color=color,
                hover_data=variables,
                title=f"Scatter Plot: {x_axis} vs {y_axis}",
            )
            st.plotly_chart(fig)
        else:
            st.write("Please select variables for X-Axis and Y-Axis.")


        # Define available variables for selection
        variables = ['Ýyl', 'Uniwersitet', 'Ugur', 'Welaýat', 'Hünär', 'Talyp görnüşi']

        st.write("### Topar diagramma")

        # User selections for clustering and grouping
        st.write("Üýtgeýän ululyklary saýlaň")
        col1, col2, col3 = st.columns(3)
        with col1:
            x_axis = st.selectbox("Y-oky", variables, index=2)  # Default is 'Ugur'
        with col2:
            cluster_by = st.selectbox("Toparlamak üçin", variables, index=5)  # Default is 'Talyp görnüşi'
        with col3:
            color_by = st.selectbox("Reňklemek üçin", variables, index=3)  # Default is 'Welaýat'

        # Prepare data for the chart
        # st.write("Clustered Bar Chart Visualization")
        if x_axis and cluster_by and color_by:
            bar_data = data.groupby([x_axis, cluster_by, color_by])['Kwota'].sum().reset_index()

            # Create the clustered bar chart
            fig = px.bar(
                bar_data,
                x='Kwota',
                y=x_axis,
                color=color_by,
                barmode='group',
                facet_col=cluster_by,
                title=f"Topar diagrammasy: {x_axis} - Kwota, {cluster_by} boýunça toparlanan we {color_by} boýunça reňklenen ",
                labels={'Kwota': 'Kwota'},
                height=600,
            )
            st.plotly_chart(fig)
        else:
            st.write("Please select variables for all axes.")

    with st.expander("Bap: ÝOM kwota çaklamalary (2024–2035)"):
        st.title("ÝOM kwota çaklamalary (2024–2035)")








# problem ds yurt kop:
# tolegli kop
# liivng expenses 
# decentralization
# mugt okamak 
# kuwwatlygyny 
# 16.4 ahwat last year mekdep grad to uni 
# welyatalarda acmak
# quality, ayratyn from bilim
# grants, 
# kampuses, 
# 

# 36-njy yyla cenli mekdep boyunca 
# population for 52 year 
# 

# tolegli islegler we bz islegler 

# 2024-2025 ahlisi

# her wuzyn ahwaty gecen yyla seredip






# 18.12.2024
# 2007 giren 2012 gutarya -> zahmet ucin gerekmish
# 20120-2024 -> zahmete gelip gowshanlar 

# dasaru yurt + local vs zahmetde gelenler 

# 2:
# pudak boyunca yom dalde toparlar boyunca, pudak boyunca dasary yurtmy yada localmy??


# 3: 
# zahmet ?


# maddy enjamlayyn vs talyp sany -> 5 talyba bir comp we 5 yyldan konelya 
# proyet 25 eboliup 
# AR VR > 3 
# tejribe -? 40% talyp/6 /15/  10 yyldan tazelemek
#  her 10 yyldan


#  sagat sany = 


# almaly tehnik


# shamca 15% kabul edilyan sany wuza bagly dal, oz caklamak, haysy ugurlardan?


# hyzmatdaslykda north we souht karta cykarmak, kodlamak bularam 


# her pudak pzije indicator 


