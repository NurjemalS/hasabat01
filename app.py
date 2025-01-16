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
import altair as alt


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
    "Kwota", 
    "Bazar", 
    "Bazar çaklama", 
    # "Hünärler",
    # "Hümarmen ugurlar",
    # "Bakalawr ugurlar",
    # "Magistr ugurlar",
    "Alymlyk derejeler",
    "Halkara indedeksli zurnallar",
    "Maddy enjamlaýyn üpjünçilik",
    "Hyzmatdaşlyklar"
])


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
            {"code": "B15", "name": "Belarus döwlet informatika we radioelektronika uniwersiteti"},
            {"code": "B16", "name": "Belarus döwlet aragatnaşyk akademiýasy"}

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
    years = ["Ähli ýyllar"] + sorted(data["Year"].unique().tolist())
    universities = ["Ähli uniwersitetler"] + sorted(data["University"].unique().tolist())

    selected_year = st.selectbox(" Ýyl saýlaň  ", years)
    selected_university = st.selectbox("Uniwersitet saýlaň    ", universities)


    def filter_data(data, selected_university, selected_year):
        filtered_data = data
        if selected_year != "Ähli ýyllar":
            filtered_data = filtered_data[filtered_data["Year"] == selected_year]
        if selected_university != "Ähli uniwersitetler":
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
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.write(f"#### Hyzmatdaşlyk edýän ýurtlarymyz (unique): {unique_countries}")
    st.write(f"#### Hyzmatdaşlyk edýän uniwersitetlerimiz (unique): {unique_universities}")
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
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("Hyzmatdaşlyk edýän ýurtlarymyz we uniwersitetlerimiz"):
        st.write("#### Hyzmatdaşlyk edýän ýurtlarymyz we uniwersitetlerimiz")
        if country_university_map:
            for country, universities in country_university_map.items():
                st.write(f"**{country}:**")
                if universities:
                    st.markdown("\n".join([f"- {university}" for university in universities]))
                else:
                    st.write("No universities available for this country.")
        else:
            st.write("No partner countries or universities available.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

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
            "Ýurtlar (Unique)": unique_countries_growth,
            "Uniwersitetler (Unique)": unique_universities_growth
        })
        return growth_df


    def visualize_growth_line_chart(growth_df):
        """
        Displays a Streamlit line chart for unique countries and universities over time.
        """
        st.subheader("Hyzmatdaşlyk edýän ýurtlaryň we uniwersitetleriň tendensiýasy")

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

    st.subheader("Hyzmatdaşlyk kartasy")
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
            "Partner Country Code": "Ýurt sany (Non-Unique)",
            "Partner University Code": "Uniwersitet sany (Non-Unique)"
        }, inplace=True)

        return final_counts


    # Calculate corrected non-unique counts
    corrected_non_unique_counts_df = calculate_non_unique_counts(filtered_data)

    # Visualize using Streamlit's bar chart
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Jemi hyzmatdaş ýurt we uniwersitet sany")
    bar_chart_data = corrected_non_unique_counts_df.set_index("Year")[[
        "Ýurt sany (Non-Unique)", 
        "Uniwersitet sany (Non-Unique)"
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
    st.subheader("Ýurt boýunça uniwersitet seljermesi")
    partner_universities = analyze_partner_universities(filtered_data)
    plot_partner_universities_with_streamlit(partner_universities)


    def create_country_distribution_pie_chart(data, title):
        # Group data and calculate percentages
        country_distribution = data.groupby("Partner Country Code")["Partner University Code"].nunique().reset_index()
        country_distribution = country_distribution.merge(country_metadata, left_on="Partner Country Code", right_on="Country Code", how="left")
        country_distribution = country_distribution.rename(columns={"Partner University Code": "University Count"})
        country_distribution['Percentage'] = (country_distribution['University Count'] / country_distribution['University Count'].sum()) * 100

        # Create Plotly Pie Chart
        fig_pie = px.pie(
            country_distribution,
            names="Partner Country Code",
            values="University Count",
            title=title,
            labels={"Partner Country Code": "Country", "University Count": "University Count"},
            height=600
        )

        # Display in Streamlit
        st.plotly_chart(fig_pie)

    col1, col2, col3 = st.columns(3)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with col2:
        st.subheader("Ýurt boýunça hyzmatdaşlygyň göterim paýy")
        create_country_distribution_pie_chart(filtered_data, "")



    def plot_heatmap(data):
        # Pivot table for heatmap
        heatmap_data = data.pivot_table(index="Year", columns="Partner Country Code", values="Partner University Code", aggfunc="count", fill_value=0)

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt="d", linewidths=0.5)
        ax.set_title("", fontsize=16, weight="bold")
        ax.set_xlabel("Ýurt kody", fontsize=14)
        ax.set_ylabel("Ýyl", fontsize=14)
        st.pyplot(fig)


    st.subheader("Hyzmatdaşlyk ýylylyk kartasy")
    plot_heatmap(filtered_data)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)




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
        ax.set_title("Ýokary 10 ýurt", fontsize=16, weight="bold")
        ax.set_xlabel("Ýurt kody", fontsize=14)
        ax.set_ylabel("Hyzmatdaşlyk sany", fontsize=14)
        st.pyplot(fig)

        # Top universities
        top_universities = data.groupby("Partner University Code").size().reset_index(name="Partnerships").sort_values("Partnerships", ascending=False).head(10)
        top_universities["Partner University Name"] = top_universities["Partner University Code"].apply(get_university_name)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(top_universities["Partner University Name"], top_universities["Partnerships"], color="green")
        ax.set_title("Ýokary 10 uniwersitet", fontsize=16, weight="bold")
        ax.set_xlabel("Uniwersitet", fontsize=14)
        ax.set_ylabel("Hyzmatdaşlyk sany", fontsize=14)
        plt.xticks(rotation=45, ha="right", fontsize=10)
        st.pyplot(fig)

    st.subheader("Ýokary görkezijili ýurtlar we uniwersitetler")
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
    years = ["Ählisi"] + sorted(long_df['Year'].unique())
    universities = sorted(long_df['University'].unique())
    universities.insert(0, "Ählisi")  # Add "ALL" option at the beginning

    selected_universities = st.multiselect("Uniwersitet saýlaň", universities, default="Ählisi")
    selected_types = st.multiselect("Dereje saýlaň", sorted(long_df['Type'].unique()), default=long_df['Type'].unique())
    selected_years = st.multiselect("Ýyl saýlaň", options=years, default="Ählisi")


    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    filtered_df = long_df.copy()

    # Filter Data
    if "Ählisi" in selected_types:
        filtered_df = filtered_df[filtered_df['Type'].isin(selected_types)]

    if "Ählisi" not in selected_years:
        filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]

    if "Ählisi" not in selected_universities:
        filtered_df = filtered_df[(filtered_df['University'].isin(selected_universities))]

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




    st.write("### Uniwersitet ara alymlyk derejeleriniň paýlanyşy (dogry maglumat üçin bir ýyl saýlaň)")

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


    st.write("### Uniwersitetleriň her alymlyk derejesi boýunça göterim goşandy (dogry maglumat üçin bir ýyl saýlaň)")

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
    filtered_df = long_df.copy()

    # Sidebar Filters
    years = ["Ählisi"] + sorted(long_df['Year'].unique())
    universities = sorted(long_df['University'].unique())
    universities.insert(0, "Ählisi")  # Add "ALL" option at the beginning

    selected_universities = st.multiselect("Uniwersitet saýlaň", universities, default="Ählisi")
    selected_types = st.multiselect("Makala görnüşi saýlaň", sorted(long_df['Type'].unique()), default=long_df['Type'].unique())
    selected_years = st.multiselect("Ýyl saýlaň", options=years, default="Ählisi")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Filter Data
    if "Ählisi" in selected_types:
        filtered_df = filtered_df[filtered_df['Type'].isin(selected_types)]

    if "Ählisi" not in selected_years:
        filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]

    if "Ählisi" not in selected_universities:
        filtered_df = filtered_df[(filtered_df['University'].isin(selected_universities))]
        

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
    filtered_df = long_df.copy()

    # Sidebar Filters
    years = ["Ählisi"] + sorted(long_df['Year'].unique())
    universities = sorted(long_df['University'].unique())
    universities.insert(0, "Ählisi")  # Add "ALL" option at the beginning

    selected_universities = st.multiselect("Uniwersitet saýlaň", universities, default="Ählisi")
    selected_types = st.multiselect("Enjam görnüşi saýlaň", sorted(long_df['Type'].unique()), default=long_df['Type'].unique())
    selected_years = st.multiselect("Ýyl saýlaň", options=years, default="Ählisi")


    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Filter Data
    if "Ählisi" in selected_types:
        filtered_df = filtered_df[filtered_df['Type'].isin(selected_types)]

    if "Ählisi" not in selected_years:
        filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]

    if "Ählisi" not in selected_universities:
        filtered_df = filtered_df[(filtered_df['University'].isin(selected_universities))]

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




    st.write("### Uniwersitet ara enjamlaryň paýlanyşy (dogry maglumat üçin bir ýyl saýlaň)")

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

    st.write("### Uniwersitetleriň her enjam boýunça göterim goşandy (dogry maglumat üçin bir ýyl saýlaň)")

    # Filter data for specific types
    specific_types = ['Kompýuter tehnikalar', 'Interaktiw tagtalar', 'Proýektorlar', 'Interaktiw işjeň paneller', 'VR enjamlar', 'AR enjamlar']
    filtered_specific_types = filtered_df[filtered_df['Type'].isin(specific_types)]

    # Group data by University and Type
    university_type_data = filtered_specific_types.groupby(['University', 'Type'])['Count'].sum().unstack(fill_value=0)

    # Calculate percentage contribution
    percentage_contribution = university_type_data.div(university_type_data.sum(axis=0), axis=1) * 100

    # Use Streamlit's bar chart to visualize
    st.bar_chart(percentage_contribution)

if page == "Kwota":
    st.title("Türkmenistanda ýokary bilimi ösdürmegiň Strategiýasyny taýýarlamak üçin MAGLUMATLAR")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("Bap: Mekdep uçurymlarynyň seljermeleri (2015–2042)"):

        # Page Title
        st.title("Mekdep uçurymlarynyň seljermeleri (2015–2042)")

        # Load Data
        graduates_data = pd.read_csv('restructured_school_graduates_.csv')  # Replace with your restructured file
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
            specific_regions = ['AHAL', 'BALKAN', 'DAŞOGUZ', 'LEBAP', 'MARY', 'AŞGABAT', 'ARKADAG']
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
                            startangle=140, colors=["#f59393", "#87cefa", "#f2f277", "#90ee90", "#ffcccb", "#aaffc3", "#f2de8d"],
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
            'Region': ['AHAL', 'BALKAN', 'DAŞOGUZ', 'LEBAP', 'MARY', 'AŞGABAT', 'ARKADAG'],
            'Latitude': [38.982647, 39.5296023, 41.83, 39.12, 37.6, 37.95, 38.096559],
            'Longitude': [58.213583, 54.2990248, 59.96, 63.57, 61.83, 58.38, 58.0553248]
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
                                get_radius="Graduates * 0.25",  # Adjust radius based on data
                                get_fill_color="[0, 255, 0, 144]",  # Red with transparency
                                pickable=True,
                            )
                        ],
                        tooltip={"text": "Region: {Region}\nGraduates: {Graduates}"}
                    )
                )
        else:
            st.write("Saýlanan maglumat ýok!")


        # # Calculate YoY Change for JEMI Graduates
        # st.write("### Mekdep Uçurymlarynyň Ýyl-ýyla Göterim Üýtgeýşi")
        # jemi_trend = graduates_data[graduates_data['Region'] == 'JEMI'].copy()
        # jemi_trend['Graduates'] = jemi_trend['Graduates'].astype(float)  # Ensure numeric type

        # if 'Graduates' in jemi_trend.columns and (jemi_trend['Graduates'] > 0).any():
        #     # Calculate Year-over-Year percentage change
        #     jemi_trend['YoY Change (%)'] = jemi_trend['Graduates'].pct_change() * 100

        #     # Plot the YoY Change
        #     fig, ax = plt.subplots(figsize=(10, 6))
        #     sns.barplot(
        #         x='Year', y='YoY Change (%)', data=jemi_trend, palette="viridis", ax=ax
        #     )
        #     ax.axhline(0, color="gray", linestyle="--", linewidth=1)
        #     ax.set_title("Mekdep Uçurymlarynyň Ýyl-ýyla Göterim Üýtgeýşi", fontsize=16, weight='bold')
        #     ax.set_xlabel("Ýyl", fontsize=14)
        #     ax.set_ylabel("Göterim Üýtgeýşi (%)", fontsize=14)
        #     st.pyplot(fig)

        #     # Display the percentage changes as a DataFrame below the plot
        #     st.write("### Göterim Üýtgeýşi Maglumatlary")
        #     st.dataframe(jemi_trend[['Year', 'Graduates', 'YoY Change (%)']].reset_index(drop=True))
        # else:
        #     st.warning("JEMI uçurymlar boýunça maglumat ýok.")
    

      # Dynamic Region Selection
        st.write("### Göterim üýtgemegi")

        region_options = ["ALL"] + sorted(filtered_df['Region'].unique()) + ["JEMI"]
        selected_regions = st.multiselect("Welaýat saýlaň", options=region_options, default="ALL")

        # Aggregate Data for Graduates
        percentage_data = filtered_df.groupby(["Year", "Region"], as_index=False)['Graduates'].sum()

        # Add Total (JEMI) Column
        total_data = percentage_data.groupby("Year", as_index=False)['Graduates'].sum()
        total_data["Region"] = "JEMI"
        percentage_data = pd.concat([percentage_data, total_data], ignore_index=True)

        # Filter by Selected Regions
        if "ALL" not in selected_regions:
            selected_regions = [region for region in selected_regions if region != "JEMI"] + ["JEMI"]
            percentage_data = percentage_data[percentage_data["Region"].isin(selected_regions)]

        # Pivot Data for Percentage Change Calculation
        percentage_pivot = percentage_data.pivot_table(index="Year", columns="Region", values="Graduates", aggfunc="sum").fillna(0)

        # Calculate Year-over-Year Percentage Change
        percentage_change = percentage_pivot.pct_change().fillna(0) * 100

        # Display Percentage Change Line Chart
        st.line_chart(percentage_change)

        # Display Data Table for Reference
        st.write("### Göterim üýtgemegi Maglumatlary")
        st.dataframe(percentage_change)


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
                    'Uniwersitet': ['TDU', 'HYYÖU', 'HNGU', 'TDBGI', 'TDLU', 'TDBSI', 'HGI', 'TDMal', 'TDYDI', 'TTII', 'TMDDI', 'TITU', 'TITUKI', 'TOHU', 'TDMI', 'TMK', 'TDÇA', 'SSTDMI', 'TDEI', 'TOHI', 'HAA'],
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
            # Group data and calculate percentages
            grouped_data = data.groupby(group_by)['Kwota'].sum().reset_index()
            grouped_data['Percentage'] = (grouped_data['Kwota'] / grouped_data['Kwota'].sum()) * 100

            # Create Plotly Pie Chart
            fig_pie = px.pie(
                grouped_data,
                names=group_by,
                values='Kwota',
                title=title,
                labels={group_by: "Category", "Kwota": "Value"},
                height=600
            )

            # Display in Streamlit
            st.plotly_chart(fig_pie)

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

# Primary group-by options
        group_by_options = ["Uniwersitet", "Ugur", "Welaýat", "Hünär", "Talyp görnüşi"]
        selected_group_by = st.selectbox("Üýtgeýji saýlaň", options=group_by_options, index=0)  # Default is 'Uniwersitet'

        # Secondary filter based on selected group-by
        unique_values = ["Ählisi"] + sorted(filtered_data[selected_group_by].unique())
        selected_values = st.multiselect(f"{selected_group_by} boýunça saýlaň", options=unique_values, default="Ählisi")
        # st.write(selected_values)

        # Apply secondary filter
        filtered_chart_data = filtered_data.copy()
        if "Ählisi" not in selected_values:
            filtered_chart_data = filtered_chart_data[filtered_chart_data[selected_group_by].isin(selected_values)]

        # Aggregate Data
        line_chart_data = filtered_chart_data.groupby(["Ýyl", selected_group_by], as_index=False)['Kwota'].sum()

        # Pivot Data for Line Chart
        line_chart_pivot = line_chart_data.pivot_table(index="Ýyl", columns=selected_group_by, values="Kwota", aggfunc="sum").fillna(0)

        # Display Line Chart
        st.write(f"### Kwota tendensiýasy - {selected_group_by}")
        st.line_chart(line_chart_pivot)

        st.write("### Ýylyň dowamynda göterim üýtgemeginiň derňewi")

        # Primary Group-by Options
        group_by_options = ["Uniwersitet", "Ugur", "Welaýat", "Hünär", "Talyp görnüşi"]
        selected_group_by_pct = st.selectbox("Üýtgeýji saýlaň ", options=group_by_options)

        # Secondary Filter for the Selected Group
        if selected_group_by_pct:
            unique_values_pct = ["ALL"] + sorted(filtered_data[selected_group_by_pct].unique())
            selected_values_pct = st.multiselect(f"{selected_group_by_pct} boýunça saýlaň", options=unique_values_pct, default="ALL")

            # Apply Secondary Filter
            filtered_pct_data = filtered_data.copy()
            if "ALL" not in selected_values_pct:
                filtered_pct_data = filtered_pct_data[filtered_pct_data[selected_group_by_pct].isin(selected_values_pct)]

            # Aggregate Data for Quota
            percentage_data = filtered_pct_data.groupby(["Ýyl", selected_group_by_pct], as_index=False)['Kwota'].sum()

            # Pivot Data for Percentage Change Calculation
            percentage_pivot = percentage_data.pivot_table(index="Ýyl", columns=selected_group_by_pct, values="Kwota", aggfunc="sum").fillna(0)

            # Calculate Year-over-Year Percentage Change
            percentage_change = percentage_pivot.pct_change().fillna(0) * 100

            # Display Percentage Change Line Chart
            st.write(f"### Göterim üýtgemegi -  {selected_group_by_pct}")
            st.line_chart(percentage_change)

            # Display Data Table for Reference
            st.write("### Göterim üýtgemegi Maglumatlary")
            st.dataframe(percentage_change)
        else:
            st.warning("Üýtgeýji saýlaň.")



    


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
                thickness=10,
                line=dict(color="black", width=0.6),
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

    with st.expander("Bap: ÝOM kwota çaklamalary"):
        st.title("ÝOM kwota çaklamalary")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        quota_data = pd.read_csv("Q_all_restructured_data.csv")  # Replace with your actual file
        graduates_data = pd.read_csv("restructured_school_graduates_.csv")  # Replace with your actual file
     
        # Filter 2024 data
        quota_2024 = quota_data[quota_data['Ýyl'] == 2024]
        graduates_2024 = graduates_data[graduates_data['Year'] == 2024]

        # # Overall AHWAT
        total_kwota_2024 = quota_2024['Kwota'].sum()
        total_graduates_2024 = graduates_2024[graduates_2024['Region'] == 'JEMI']
        overall_ahwat = total_kwota_2024 / total_graduates_2024['Graduates']

        # # AHWAT by Region
        region_kwota_2024 = quota_2024.groupby('Welaýat')['Kwota'].sum().reset_index()
        region_graduates_2024 = graduates_2024.groupby('Region')['Graduates'].sum().reset_index()
        region_ahwat = pd.merge(region_kwota_2024, region_graduates_2024, left_on='Welaýat', right_on='Region')
        region_ahwat['AHWAT'] = region_ahwat['Kwota'] / region_ahwat['Graduates']
        region_ahwat = region_ahwat.drop(columns=['Region'])
        region_ahwat['AHWAT'] = region_ahwat['AHWAT'] * 100 

        col1, col2, col3 = st.columns(3)

        # Add content to each column
        with col1:
            st.metric(label="ÝOM kwota 2024:", value=total_kwota_2024)
        with col2:
            st.metric(label="Uçurum 2024:", value= total_graduates_2024['Graduates'])
        with col3:
            st.metric(label="Ahwat:", value=overall_ahwat*100)

        # Slider to select AHwat value between 17 and 75
        selected_ahwat = st.slider(
            "Ahwat saýlaň:",
            min_value=17.0,
            max_value=75.0,
            value=float(overall_ahwat * 100),  # Ensure the value is a float
            step=0.01
        )
            
        st.write("### Welaýat ara ahwat")
        st.dataframe(region_ahwat)

        st.write("### Şeýlelikde jemi we welaýat ara kwota çaklamalary")

        graduates_data.loc[
            (graduates_data['Year'] > 2024) & (graduates_data['Region'] == 'JEMI'),
            'Kwota'
        ] = graduates_data.loc[graduates_data['Year'] > 2024, 'Graduates'] * (selected_ahwat / 100)

        for region in region_ahwat['Welaýat']:
            graduates_data.loc[
                (graduates_data['Year'] > 2024) & (graduates_data['Region'] == region),
                'Kwota'
            ] = (
                graduates_data.loc[(graduates_data['Year'] > 2024) & (graduates_data['Region'] == region), 'Graduates'] *
                (region_ahwat.loc[region_ahwat['Welaýat'] == region, 'AHWAT'].iloc[0] / 100)
            )

        graduates_data = graduates_data.dropna(subset=['Kwota'])

        forecasted_quota = graduates_data[['Year', 'Region', 'Kwota']]
        historical_quota = quota_data.groupby(['Ýyl', 'Welaýat'])['Kwota'].sum().reset_index()
        historical_quota.rename(columns={'Ýyl': 'Year', 'Welaýat': 'Region'}, inplace=True)
        combined_quota = pd.concat([historical_quota, forecasted_quota], ignore_index=True)

        # Filter combined_quota for years between 2015 and 2024
        filtered_quota = combined_quota[(combined_quota['Year'] >= 2015) & (combined_quota['Year'] <= 2024)]

        # Calculate JEMI as the sum of Kwota for all regions per year
        jemi_quota = filtered_quota.groupby('Year')['Kwota'].sum().reset_index()
        jemi_quota['Region'] = 'JEMI'

        # Append JEMI to the combined quota
        combined_quota = pd.concat([combined_quota, jemi_quota], ignore_index=True)

        # Display the updated combined quota
        # st.write("### Combined Quota with JEMI (2015–2024)")

        # User Selection for Regions
        regions = list(combined_quota['Region'].unique())
        selected_regions = st.multiselect("Welaýat saýlaň", options=regions, default=["JEMI"])

        # Filter data for selected regions
        filtered_data = combined_quota[combined_quota['Region'].isin(selected_regions)]
        filtered_data["Year"] = filtered_data["Year"].astype(str)
        # Prepare data for line chart
        line_chart_data = filtered_data.groupby(['Year', 'Region'])['Kwota'].sum().unstack().fillna(0)


        # Plot line chart using Streamlit's built-in line chart functionality
        st.line_chart(line_chart_data)

        st.write("### Şeýlelikde uniwersitet ara kwota çaklamalary")

# Calculate university distribution from 2024 quota data
        university_distribution = quota_2024.groupby('Uniwersitet')['Kwota'].sum()
        university_distribution = (university_distribution / university_distribution.sum()) * 100

        # Initialize a DataFrame
        university_distribution = university_distribution.reset_index()
        university_distribution.columns = ['Uniwersitet', 'Distribution']
        st.write("Her uniwersitetiň kwotada paýy (2024)")
        st.dataframe(university_distribution)

        # Study type (Hünärmen vs Bakalawr) percentages for each university
        study_distribution = (
            quota_2024.groupby(['Uniwersitet', 'Hünär'])['Kwota'].sum() /
            quota_2024.groupby('Uniwersitet')['Kwota'].sum()
        ).reset_index()

        # Rename columns for clarity
        study_distribution.rename(columns={'Kwota': 'Percentage'}, inplace=True)

        # Display the updated DataFrame
        # st.dataframe(study_distribution)

       # Step 1: Get 2024 university distribution

       # Filter data for years after 2024 and Region "JEMI"
        combined_quota["Year"] = pd.to_numeric(combined_quota["Year"], errors="coerce")

        # Filter data for years after 2024 and region 'JEMI'
        combined_quota = combined_quota[(combined_quota['Year'] > 2024) & (combined_quota['Region'] == 'JEMI')]

        # Add university distribution to filtered_data
        combined_quota = combined_quota.assign(key=1)  # Add a temporary key for cross join
        university_distribution = university_distribution.assign(key=1)

        university_quota = pd.merge(combined_quota, university_distribution, on='key').drop(columns='key')

        # Calculate university quota
        university_quota['University_Kwota'] = university_quota['Kwota'] * (university_quota['Distribution'] / 100)

        # Merge with study distribution to split into Hünärmen and Bakalawr
        study_distribution = study_distribution.rename(columns={'Uniwersitet': 'University'})  # Ensure consistent naming
        final_data = pd.merge(university_quota, study_distribution, left_on='Uniwersitet', right_on='University', how='inner')

        # Calculate study type quota
        final_data['Study_Type_Kwota'] = final_data['University_Kwota'] * (final_data['Percentage'])
        # st.dataframe(final_data)

        # Filter historical data for years 2015-2024
        historical_data = quota_data[(quota_data['Ýyl'] >= 2015) & (quota_data['Ýyl'] <= 2024)]

        # Group by year, university, and study type for historical data
        historical_grouped = historical_data.groupby(['Ýyl', 'Uniwersitet', 'Hünär'])['Kwota'].sum().reset_index()
        historical_grouped.rename(columns={'Ýyl': 'Year', 'Kwota': 'Quota'}, inplace=True)

        # Add JEMI (all universities combined) for historical data
        jemi_historical = historical_grouped.groupby(['Year', 'Hünär'])['Quota'].sum().reset_index()
        jemi_historical['Uniwersitet'] = 'JEMI'
        historical_grouped = pd.concat([historical_grouped, jemi_historical], ignore_index=True)


        # Combine historical and forecasted data
        combined_data = pd.concat([historical_grouped, final_data], ignore_index=True)
        combined_data["Year"] = combined_data["Year"].astype(str)
        combined_data['Combined_Quota'] = combined_data['Quota'].combine_first(combined_data['Study_Type_Kwota'])
        combined_data = combined_data[combined_data['Uniwersitet'] != 'JEMI']

        # st.dataframe(combined_data)

        # Multiselect for universities, including 'JEMI'
        all_universities = list(combined_data['Uniwersitet'].unique())
        all_universities.insert(0, "Ählisi")        
        selected_universities = st.multiselect("Uniwersitet saýlaň", options=all_universities, default="Ählisi")

        if "Ählisi" in selected_universities:
            filtered_data = combined_data.copy()  # Select all data if "ALL" is chosen
        else:
            filtered_data = combined_data[combined_data['Uniwersitet'].isin(selected_universities)]
        
        # Radio buttons for study type
        study_type = st.radio("Hünär saýlaň", options=['Hünärmen', 'Bakalawr', 'Ikisem'])

        # Filter combined data based on user selection
        if study_type != 'Ikisem':
            filtered_data = filtered_data[filtered_data['Hünär'] == study_type]
        

        # Pivot data for line chart
        pivot_data = filtered_data.pivot_table(index='Year', columns='Uniwersitet', values='Combined_Quota', aggfunc='sum').fillna(0)
        
        # Plot line chart using Streamlit
        st.line_chart(pivot_data)

        st.write("### Şeýlelikde ugur boýunça kwota çaklamalary")

# Calculate university distribution from 2024 quota data
        ugur_distribution = quota_2024.groupby('Ugur')['Kwota'].sum()
        ugur_distribution = (ugur_distribution / ugur_distribution.sum()) * 100

        # Initialize a DataFrame
        ugur_distribution = ugur_distribution.reset_index()
        ugur_distribution.columns = ['Ugur', 'Distribution']
        st.write("Her ugruň kwotada paýy (2024)")
        st.dataframe(ugur_distribution)

        # Study type (Hünärmen vs Bakalawr) percentages for each university
        study_distribution = (
            quota_2024.groupby(['Ugur', 'Hünär'])['Kwota'].sum() /
            quota_2024.groupby('Ugur')['Kwota'].sum()
        ).reset_index()

        # Rename columns for clarity
        study_distribution.rename(columns={'Kwota': 'Percentage'}, inplace=True)

        # Display the updated DataFrame
        # st.dataframe(study_distribution)

       # Step 1: Get 2024 university distribution

       # Filter data for years after 2024 and Region "JEMI"
        combined_quota["Year"] = pd.to_numeric(combined_quota["Year"], errors="coerce")

        # Filter data for years after 2024 and region 'JEMI'
        combined_quota = combined_quota[(combined_quota['Year'] > 2024) & (combined_quota['Region'] == 'JEMI')]

        # Add university distribution to filtered_data
        combined_quota = combined_quota.assign(key=1)  # Add a temporary key for cross join
        ugur_distribution = ugur_distribution.assign(key=1)

        university_quota = pd.merge(combined_quota, ugur_distribution, on='key').drop(columns='key')

        # Calculate university quota
        university_quota['Ugur_Kwota'] = university_quota['Kwota'] * (university_quota['Distribution'] / 100)

        # Merge with study distribution to split into Hünärmen and Bakalawr
        study_distribution = study_distribution.rename(columns={'Ugur': 'Ugur'})  # Ensure consistent naming
        final_data = pd.merge(university_quota, study_distribution, left_on='Ugur', right_on='Ugur', how='inner')

        # Calculate study type quota
        final_data['Study_Type_Kwota'] = final_data['Ugur_Kwota'] * (final_data['Percentage'])
        # st.dataframe(final_data)

        # Filter historical data for years 2015-2024
        historical_data = quota_data[(quota_data['Ýyl'] >= 2015) & (quota_data['Ýyl'] <= 2024)]

        # Group by year, university, and study type for historical data
        historical_grouped = historical_data.groupby(['Ýyl', 'Ugur', 'Hünär'])['Kwota'].sum().reset_index()
        historical_grouped.rename(columns={'Ýyl': 'Year', 'Kwota': 'Quota'}, inplace=True)

        # Add JEMI (all universities combined) for historical data
        jemi_historical = historical_grouped.groupby(['Year', 'Hünär'])['Quota'].sum().reset_index()
        jemi_historical['Ugur'] = 'JEMI'
        historical_grouped = pd.concat([historical_grouped, jemi_historical], ignore_index=True)


        # Combine historical and forecasted data
        combined_data = pd.concat([historical_grouped, final_data], ignore_index=True)
        combined_data["Year"] = combined_data["Year"].astype(str)
        combined_data['Combined_Quota'] = combined_data['Quota'].combine_first(combined_data['Study_Type_Kwota'])
        combined_data = combined_data[combined_data['Ugur'] != 'JEMI']

        # st.dataframe(combined_data)

        # Multiselect for universities, including 'JEMI'
        all_ugur = list(combined_data['Ugur'].unique())
        all_ugur.insert(0, "Ählisi")        
        selected_ugurs = st.multiselect("Ugur saýlaň (azyndan iki ugur saýlaň)     ", options=all_ugur, default="Ählisi")

        if "Ählisi" in selected_ugurs:
            filtered_data = combined_data.copy()  # Select all data if "ALL" is chosen
        else:
            filtered_data = combined_data[combined_data['Ugur'].isin(selected_ugurs)]
        
        # Radio buttons for study type
        study_type = st.radio("Hünär saýlaň  ", options=['Hünärmen', 'Bakalawr', 'Ikisem'])

        # Filter combined data based on user selection
        if study_type != 'Ikisem':
            filtered_data = filtered_data[filtered_data['Hünär'] == study_type]
        

        # Pivot data for line chart
        pivot_data = filtered_data.pivot_table(index='Year', columns='Ugur', values='Combined_Quota', aggfunc='sum').fillna(0)
        
        # Plot line chart using Streamlit
        st.line_chart(pivot_data)


if page == "Bazar":
    st.title("Türkmenistanda bazar ykdysadyýeti barada maglumatlar")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.write("### Bazar ykdysadyýeti")

        # Load Data
    df = pd.read_csv('bazar_intro.csv')  # Replace with your restructured file
    df["Ýyl"] = df["Ýyl"].astype(str)


    # Calculate percentage increase for each variable
    df["Zähmete ukyply ýaşdaky ilatyň sanynyň öňki görkezijä görä tapawudy, göterimde %"] = df["Zähmete ukyply ýaşdaky ilatyň sany"].pct_change() * 100
    df["Ykdysady taýdan işjeň ilatynyň sanynyň öňki görkezijä görä tapawudy, göterimde %"] = df["Ykdysady taýdan işjeň ilatynyň sany"].pct_change() * 100

    # Display the data
    st.dataframe(df)

    # Streamlit bar chart for population distribution
    st.write("### Ilat paýlanyşy")
    bar_data = df.set_index("Ýyl")[["Zähmete ukyply ýaşdaky ilatyň sany", "Ykdysady taýdan işjeň ilatynyň sany"]]
    # st.bar_chart(bar_data)
    bar_data = df.set_index("Ýyl")[["Zähmete ukyply ýaşdaky ilatyň sany", "Ykdysady taýdan işjeň ilatynyň sany"]].reset_index()

    # Using Plotly for a grouped bar chart
    fig = px.bar(
        bar_data,
        x="Ýyl",  # X-axis for years
        y=["Zähmete ukyply ýaşdaky ilatyň sany", "Ykdysady taýdan işjeň ilatynyň sany"],  # Variables for grouped bars
        barmode="group",  # Grouped bars
        title="Ilat Paýlanyşy (Grouped Bar Chart)",
        labels={"value": "Sany", "variable": "Ululyklar", "Ýyl": "Ýyllar"},  # Custom labels
        height=600
    )
    # Set the x-axis to category to ensure only present years are shown
    fig.update_layout(xaxis_type="category")

    # Display the chart in Streamlit
    st.plotly_chart(fig)



    bazar_df = pd.read_csv('data_bazar2015.csv')  # Replace with your restructured file
    bazar_df["Year"] = bazar_df["Year"].astype(str)
    bazar_df = bazar_df[bazar_df["Variable"] != "Ý.B. Işgärler göterimde %"]
    bazar_df = bazar_df[bazar_df["Variable"] != "Ugurlar boýunça Ý.B. Işgärler göterimde %"]

    # Streamlit UI

    # Step 1: State Selection
    state = st.radio("Döwlet saýlaň", options=bazar_df["State"].unique(), horizontal=True)

    if state == "JEMI":
    # Include all variables regardless of state
        variables_to_include = bazar_df["Variable"].unique()
    else:
        # Include variables specific to the selected state
        variables_to_include = bazar_df[bazar_df["State"] == state]["Variable"].unique()

        # Step 2: Ugur and Variable Selection
    selected_ugurs = st.multiselect("Ugur saýlaň", options=bazar_df["Ugur"].unique(), default=["Jemi"])
    selected_variables = st.multiselect("Üýtgeýän ululyk saýlaň", options=variables_to_include, default=list(variables_to_include))

    # Filter Data by Ugur and Variable
    filtered_data = bazar_df[(bazar_df["Ugur"].isin(selected_ugurs)) & (bazar_df["Variable"].isin(selected_variables))]

    # Step 3: Visualization
    # st.write("### Filtered Data Table")
    # st.dataframe(filtered_data)

    # Group by Year for Visualization
    grouped_data = filtered_data.groupby(["Year", "Variable"])["Value"].sum().unstack()

    # Bar Chart
    st.write("### Ýyllaryň dowamynda üýtgeýän ululyk")
    # st.bar_chart(grouped_data)

    if not filtered_data.empty:
        # Reset index for easier manipulation
        filtered_data_reset = filtered_data.reset_index()

        # Create a grouped bar chart for selected variables
        fig = px.bar(
            filtered_data_reset,
            x="Year",  # X-axis for years
            y="Value",  # Y-axis for values
            color="Variable",  # Color-coded by variable
            barmode="group",  # Grouped bars for each year
            title="",
            labels={"Year": "Ýyllar", "Value": "Value", "Variable": "Üýtgeýän ululyk"},
            height=600,
        )
        fig.update_layout(xaxis_type="category")
        # Display the chart
        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected criteria.")

  
        # Calculate Percentage Change Year-over-Year
    grouped_data_percentage = grouped_data.pct_change() * 100

    # Replace NaN or infinite values (e.g., for first year) with 0
    grouped_data_percentage = grouped_data_percentage.fillna(0)

    # Line Chart Showing Percentage Change
    st.write("### Göterim üýtgemegi ")
    st.line_chart(grouped_data_percentage)

    with st.expander("Ý.B. Işgärleriň seljermesi"):
        st.write("### Ý.B. Işgärleriň seljermesi")

        # Load Data
        bazar_df = pd.read_csv('data_bazar2015.csv')
        bazar_df["Year"] = bazar_df["Year"].astype(str)
        bazar_df = bazar_df[bazar_df["Variable"] != "Ý.B. Işgärler göterimde %"]
        bazar_df = bazar_df[bazar_df["Variable"] != "Ugurlar boýunça Ý.B. Işgärler göterimde %"]



        # Step 1: State Selection
        state = st.radio("Döwlet saýlaň ", options=bazar_df["State"].unique(), horizontal=True)

        # Step 2: Year Selection
        selected_years = st.multiselect(
            "Ýyllary saýlaň", 
            options=bazar_df["Year"].unique(), 
            default=bazar_df["Year"].unique()
        )

        # Filter data for the selected state and years
        state_data = bazar_df[
            (bazar_df["State"] == state) & 
            (bazar_df["Year"].isin(selected_years))
        ]

        # Filter only for "Ý.B. Işgärleriň sany" and "Işgärleriň sany" variables
        filtered_state_data = state_data[state_data["Variable"].isin(["Ý.B. Işgärleriň sany", "Işgärleriň sany"])]

        # Pivot Data for Analysis
        pivot_data = filtered_state_data.pivot_table(
            index=["Ugur", "Year"],
            columns="Variable",
            values="Value",
            aggfunc="sum"
        ).reset_index()

        # Drop rows where total workers are NaN or 0
        pivot_data = pivot_data.dropna(subset=["Işgärleriň sany"])
        pivot_data = pivot_data[pivot_data["Işgärleriň sany"] > 0]

        # Calculate Higher Education Percentage
        pivot_data["YB_Percentage"] = (pivot_data["Ý.B. Işgärleriň sany"] / pivot_data["Işgärleriň sany"]) * 100

        # --- Overall Distribution for JEMI ---
        # Filter data for JEMI Ugur
        jemi_data = pivot_data[pivot_data["Ugur"] == "Jemi"]

        # Visualization 1: Overall Distribution (JEMI)
        st.write("### Ý.B. Işgärleriň paýlanyşy")
        if not jemi_data.empty:
            total_yb = jemi_data["Ý.B. Işgärleriň sany"].sum()
            total_workers = jemi_data["Işgärleriň sany"].sum()
            pie_data = pd.DataFrame({
                "Category": ["Ý.B. Işgärler", "Işgärleriň"],
                "Value": [total_yb, total_workers - total_yb]
            })

            fig_pie1 = px.pie(
                pie_data,
                names="Category",
                values="Value",
                title=f"Ý.B. Işgärleriň paýlanyşy - {', '.join(selected_years)}",
                labels={"Category": "Category", "Value": "Value"},
                height=600
            )
            st.plotly_chart(fig_pie1)
        else:
            st.write("No data available for the selected criteria.")

        # --- Detailed Ugur Breakdown ---
        # Filter data for higher-educated workers

        filtered_pivot_data = pivot_data[pivot_data["Ugur"] != "Jemi"]  # Exclude "Jemi" for sector-wise analysis

        # Calculate the total higher-educated workers from the filtered data
        total_yb_filtered = filtered_pivot_data["Ý.B. Işgärleriň sany"].sum()

        # Calculate percentage distribution for each sector
        filtered_pivot_data["Percentage"] = (
            filtered_pivot_data["Ý.B. Işgärleriň sany"] / total_yb_filtered
        ) * 100

        # Visualization: Pie Chart for Higher-Educated Workers Distribution Across Sectors
        st.write("### Ý.B. Işgärleriň ugurlar boýunça paýlanyşy")
        if not filtered_pivot_data.empty:
            fig_pie_filtered = px.pie(
                filtered_pivot_data,
                names="Ugur",
                values="Percentage",
                title="Ý.B. Işgärleriň ugurlar boýunça paýlanyşy",
                labels={"Ugur": "Sector", "Percentage": "Percentage (%)"},
                height=600
            )
            st.plotly_chart(fig_pie_filtered)
        else:
            st.write("No data available for the selected criteria.")

        st.write("### Ugurlar boýunça Ý.B. işgärler")
        sector_data = filtered_state_data.pivot_table(
            index=["Ugur", "Year"],
            columns="Variable",
            values="Value",
            aggfunc="sum"
        ).reset_index()

        # Drop rows where total workers are NaN or 0
        sector_data = sector_data.dropna(subset=["Işgärleriň sany"])
        sector_data = sector_data[sector_data["Işgärleriň sany"] > 0]

        # Calculate Higher Education Percentage for Each Sector
        sector_data["YB_Percentage"] = (sector_data["Ý.B. Işgärleriň sany"] / sector_data["Işgärleriň sany"]) * 100

        # Group by Sector to calculate the mean percentage across selected years
        sector_distribution = sector_data.groupby("Ugur")["YB_Percentage"].mean().reset_index()
        # Visualization 2: Detailed Ugur Breakdown
        if not sector_data.empty:
            fig_bar = px.bar(
                sector_data,
                x="Ugur",
                y="YB_Percentage",
                color="Year",
                barmode="group",
                title="Ugurlar boýunça Ý.B. işgärler göterimde %",
                labels={"YB_Percentage": "Göterimde (%)", "Ugur": "Ugur", "Year": "Ýyl"},
                height=600
            )
            st.plotly_chart(fig_bar)
        else:
            st.write("No sector data available for the selected criteria.")


        # --- Additional Visualization: Line Chart for JEMI Trend ---
        st.write("### Ý.B. işgärler göterimde ýyllar boýunça tendensiýasy")
        if not jemi_data.empty:
            jemi_trend = jemi_data.groupby("Year")["YB_Percentage"].mean().reset_index()

            fig_line = px.line(
                jemi_trend,
                x="Year",
                y="YB_Percentage",
                title="",
                labels={"YB_Percentage": "Göterimde (%)", "Year": "Ýyl"},
                height=600
            )
            st.plotly_chart(fig_line)
        else:
            st.write("No JEMI data available for selected criteria.")
        

        # Step 1: Ugur Selection
        selected_ugurs = st.multiselect(
            "Ugur saýlaň  ",
            options=bazar_df["Ugur"].unique(),
            default=["Jemi"]  # Default to overall "Jemi"
        )

        filtered_data = bazar_df[
        (bazar_df["Ugur"].isin(selected_ugurs)) &
        (bazar_df["Variable"] == "Ý.B. Işgärleriň sany")
        ]


        # Pivot Data for Visualization
        pivot_data = filtered_data.pivot_table(
            index=["Year", "Ugur"],
            columns="State",
            values="Value",
            aggfunc="sum"
        ).reset_index()

        # Melt the data for Plotly compatibility
        melted_data = pivot_data.melt(
            id_vars=["Year", "Ugur"],
            value_vars=["Döwlet", "Döwlet dahylsyz"],
            var_name="State",
            value_name="Value"
        )

        # Visualization: Single Line Chart
        st.write("### Ugurlar boýunça döwlet we döwlete dahylsyz Ý.B. işgärleriň tendensiýasy")
        if not melted_data.empty:
            # Use Plotly for a combined line chart
            fig = px.line(
                melted_data,
                x="Year",
                y="Value",
                color="State",
                line_group="Ugur",
                title="",
                labels={"Value": "Ý.B. Işgärler", "Year": "Ýyl", "State": "Döwlet:"},
                height=600
            )
            st.plotly_chart(fig)
        else:
            st.write("No data available for the selected criteria.")

    with st.expander("ÝOM tamamlanlaryň seljermesi"):
        # Filter data for relevant variables
        graduate_data = bazar_df[bazar_df["Variable"].isin(["Daşary ýurdy tamamlap ykrar edilenler", "ÝOM tamamlanlar"])]

        # Pivot data for analysis
        pivot_data = graduate_data.pivot_table(
            index=["Year", "Ugur"],
            columns="Variable",
            values="Value",
            aggfunc="sum"
        ).reset_index()

        # Melt data for Plotly compatibility
        melted_data = pivot_data.melt(
            id_vars=["Year", "Ugur"],
            value_vars=["Daşary ýurdy tamamlap ykrar edilenler", "ÝOM tamamlanlar"],
            var_name="Graduate Type",
            value_name="Count"
        )

        # Streamlit UI
        st.write(" ### ÝOM tamamlanlaryň seljermesi")

        # Step 1: Sector Selection
        selected_ugurs = st.multiselect(
            "Ugur saýlaň   ",
            options=bazar_df["Ugur"].unique(),
            default="Jemi"
        )


        # Filter data based on selected sectors and years
        filtered_data = melted_data[
            (melted_data["Ugur"].isin(selected_ugurs)) 
        ]

        # Ensure data exists
        if filtered_data.empty:
            st.write("No data available for the selected sectors and years.")
        else:
            # 1. Line Chart: Trends Over Time
            st.write("###  Ugurlar boýunça ÝOM tamamlanlaryň we Daşary ýurdy tamamlap ykrar edenleriň tendensiýasy")
            fig_line = px.line(
                filtered_data,
                x="Year",
                y="Count",
                color="Graduate Type",
                line_group="Ugur",
                title="",
                labels={"Year": "Ýyl", "Count": "ÝOM tamamlan talyp sany", "Graduate Type": "ÝOM tamamlanlaryň görnüşi"},
                height=600
            )
            st.plotly_chart(fig_line)


            # Percentage Change: Dynamic Line Chart
            st.write("### Ugurlar boýunça göterim üýtgemeler tendensiýasy")

            # Calculate Percentage Change for Each Ugur
            percentage_data = filtered_data.groupby(["Year", "Graduate Type", "Ugur"], as_index=False)["Count"].sum()

            # Filter based on selected Ugurs
            selected_ugurs_for_percentage = st.multiselect(
                "Saýlanan ugurlardan ugur saýlaň",
                options=filtered_data["Ugur"].unique(),
                default=filtered_data["Ugur"].unique()
            )

            # Only include selected Ugurs for percentage change
            percentage_data = percentage_data[percentage_data["Ugur"].isin(selected_ugurs_for_percentage)]

            # Pivot data for percentage change calculation
            percentage_pivot = percentage_data.pivot_table(
                index=["Year", "Ugur"],
                columns="Graduate Type",
                values="Count",
                aggfunc="sum"
            ).fillna(0)

            # Calculate year-over-year percentage change for each Ugur
            percentage_change_data = []
            for ugur in selected_ugurs_for_percentage:
                ugur_data = percentage_pivot.xs(ugur, level="Ugur").pct_change().fillna(0) * 100
                ugur_data = ugur_data.reset_index()
                ugur_data["Ugur"] = ugur  # Add Ugur as a column
                percentage_change_data.append(ugur_data)

            # Combine all percentage change data
            combined_percentage_data = pd.concat(percentage_change_data, ignore_index=True)

            # Melt data for Plotly compatibility
            melted_percentage = combined_percentage_data.melt(
                id_vars=["Year", "Ugur"],
                var_name="Graduate Type",
                value_name="Percentage Change"
            )

            # Line Chart for Percentage Change
            fig_percentage = px.line(
                melted_percentage,
                x="Year",
                y="Percentage Change",
                color="Graduate Type",
                line_group="Ugur",
                title="",
                labels={"Year": "Ýyl", "Percentage Change": "Göterim üýtgemesi", "Graduate Type": "ÝOM tamamlanlaryň görnüşi"},
                height=600
            )
            st.plotly_chart(fig_percentage)

           

            col1, col2 = st.columns(2)

            with col1:
                # 2. Grouped Bar Chart: Comparison by Sector and Year
                st.write("###  ÝOM tamamlanlaryň we Daşary ýurdy tamamlap ykrar edenleriň deňeşdirmesi ")
                fig_bar = px.bar(
                    filtered_data,
                    x="Year",  # X-axis for years
                    y="Count",  # Y-axis for graduate counts
                    color="Graduate Type",  # Color-coded by type of graduate
                    barmode="group",  # Grouped bars for each year
                    facet_col="Ugur",  # Separate columns for each sector
                    title="",
                    labels={"Year": "Ýyl", "Count": "ÝOM tamamlanlaryň sany", "Graduate Type": "ÝOM tamamlanlaryň görnüşi"},
                    height=800
                )

                # Update layout to set xaxis_type as category for all subplots
                facet_axes = [f"xaxis{i+1}" for i in range(len(filtered_data["Ugur"].unique()))]  # Generate axis names dynamically
                for axis in facet_axes:
                    if axis in fig_bar.layout:
                        fig_bar.layout[axis].type = "category"  # Ensure x-axis is treated as a category

                st.plotly_chart(fig_bar)


            with col2:
                st.write("### ÝOM tamamlanlaryň we Daşary ýurdy tamamlap ykrar edenleriň göterim paýy ")

                # Calculate percentage distribution for each year
                percentage_data = filtered_data.groupby(["Year", "Graduate Type"])["Count"].sum().reset_index()
                total_per_year = percentage_data.groupby("Year")["Count"].sum().reset_index().rename(columns={"Count": "Total"})
                percentage_data = percentage_data.merge(total_per_year, on="Year")
                percentage_data["Percentage"] = (percentage_data["Count"] / percentage_data["Total"]) * 100

                # Create stacked bar chart
                fig_stacked_bar = px.bar(
                    percentage_data,
                    x="Year",
                    y="Percentage",
                    color="Graduate Type",
                    barmode="stack",
                    title="",
                    labels={"Year": "Ýyl", "Percentage": "ÝOM tamamlanlaryň göterim paýy", "Graduate Type": "ÝOM tamamlanlaryň görnüşi"},
                    height=600
                )

                fig_stacked_bar.update_layout(xaxis_type="category")

                st.plotly_chart(fig_stacked_bar)

    with st.expander("ÝOM kwota - ÝOM tamamlanlar"):
        st.write("### ÝOM kwota - ÝOM tamamlanlar seljermesi")
        # Filter data for relevant variables
        student_data = bazar_df[bazar_df["Variable"].isin(["ÝOM kwota", "ÝOM tamamlanlar"])]

        # Pivot data for analysis
        pivot_data = student_data.pivot_table(
            index=["Year", "Ugur"],
            columns="Variable",
            values="Value",
            aggfunc="sum"
        ).reset_index()

        # Calculate Efficiency Ratio
        pivot_data["Completion Ratio"] = (pivot_data["ÝOM tamamlanlar"] / pivot_data["ÝOM kwota"]) * 100

        # Melt data for Plotly compatibility
        melted_data = pivot_data.melt(
            id_vars=["Year", "Ugur"],
            value_vars=["ÝOM kwota", "ÝOM tamamlanlar"],
            var_name="Metric",
            value_name="Count"
        )

        # Step 1: Sector Selection
        selected_ugurs = st.multiselect(
            " Ugur saýlaň  ",
            options=bazar_df["Ugur"].unique(),
            default="Jemi"
        )

        # Filter data based on selected sectors
        filtered_data = melted_data[melted_data["Ugur"].isin(selected_ugurs)]

        # Ensure data exists
        if filtered_data.empty:
            st.write("No data available for the selected sectors.")
        else:
            # 1. Line Chart: Trends Over Time
            st.write("### Ugur boýunça ÝOM kwota - ÝOM tamamlanlar tendensiýasy")
            fig_line = px.line(
                filtered_data,
                x="Year",
                y="Count",
                color="Metric",
                line_group="Ugur",
                title="",
                labels={"Year": "Ýyl", "Count": "Talyp sany", "Metric": "Metrika"},
                height=600
            )
            st.plotly_chart(fig_line)

            # 2. Stacked Bar Chart: Proportion of Enrolled vs. Graduated
            st.write("### ÝOM kwota - ÝOM tamamlanlar göterim paýy")
            filtered_data["Total"] = filtered_data.groupby(["Year", "Ugur"])["Count"].transform("sum")
            filtered_data["Percentage"] = (filtered_data["Count"] / filtered_data["Total"]) * 100

            fig_stacked = px.bar(
                filtered_data,
                x="Year",
                y="Percentage",
                color="Metric",
                barmode="stack",
                facet_col="Ugur",
                title="",
                labels={"Year": "Ýyl", "Percentage": "Göterim (%)", "Metric": "Metrika"},
                height=800
            )

              # Update layout to set xaxis_type as category for all subplots
            facet_axes = [f"xaxis{i+1}" for i in range(len(filtered_data["Ugur"].unique()))]  # Generate axis names dynamically
            for axis in facet_axes:
                if axis in fig_stacked.layout:
                    fig_stacked.layout[axis].type = "category"  # Ensure x-axis is treated as a category
            st.plotly_chart(fig_stacked)
        # 3. Scatter Plot: Enrolled vs. Graduated
        st.write("### ÝOM kwota - ÝOM tamamlanlar gatnaşyklary")

        # Exclude 'Jemi' from the data
        scatter_data = pivot_data[pivot_data["Ugur"] != "Jemi"].dropna(subset=["ÝOM kwota", "ÝOM tamamlanlar"])  # Remove rows with missing values

        # Create the scatter plot
        fig_scatter = px.scatter(
            scatter_data,
            x="ÝOM kwota",
            y="ÝOM tamamlanlar",
            color="Ugur",
            size="ÝOM kwota",  # Size of points based on enrolled students
            hover_name="Ugur",
            title="ÝOM kwota - ÝOM tamamlanlar sepme diagramma'",
            labels={
                "ÝOM kwota": "ÝOM kwota",
                "ÝOM tamamlanlar": "ÝOM tamamlan",
                "Ugur": "Ugur"
            },
            height=600
        )

        # Display the plot
        st.plotly_chart(fig_scatter)

    with st.expander("Täze Kabul edilen ÝBI sany - ÝOM tamamlanlar seljermesi"):

        # Display Explanation in Streamlit
    
        st.markdown("""
        ###### Täze Kabul edilen ÝBI sany hasaplamagyň formulasy:

        
        Täze Kabul edilen ÝBI sany = Kabul edilen ÝBI sany - Işden çykanlaryň sany * Ý.B. Işgärleriň sany/Işgärleriň sany + Pensiýa ýaşyna ýetenleriň takmynan sany
    
        ######  Maksat:

        Bu formula, işçi güýjüniň ösüşine we pudaklaýyn zerurlyklaryna baha bermäge kömek edip, her ýyl täze döredilen ýokary bilimli işçi wezipelerini hasaplaýar.     """)

        st.write("### Täze Kabul edilen ÝBI sany - ÝOM tamamlanlar seljermesi")

        # Filter relevant variables
        relevant_vars = [
            "Kabul edilen ÝBI sany",
            "Işden çykanlaryň sany",
            "Ý.B. Işgärleriň sany",
            "Işgärleriň sany",
            "Pensiýa ýaşyna ýetenleriň takmynan sany",
            "ÝOM tamamlanlar",
            "Daşary ýurdy tamamlap ykrar edilenler"
        ]
        bazar_df = bazar_df[bazar_df["Variable"].isin(relevant_vars)]

        # Pivot Data for Analysis
        pivot_data = bazar_df.pivot_table(
            index=["Year", "Ugur"],
            columns="Variable",
            values="Value",
            aggfunc="sum"
        ).reset_index()

        # Calculate newly `Kabul edilen ÝBI sany`
        pivot_data["Täze Kabul edilen ÝBI sany"] = (
            pivot_data["Kabul edilen ÝBI sany"] -
            pivot_data["Işden çykanlaryň sany"] * ((pivot_data["Ý.B. Işgärleriň sany"] * 100) / pivot_data["Işgärleriň sany"]) / 100 +
            pivot_data["Pensiýa ýaşyna ýetenleriň takmynan sany"]
        )

        # Streamlit UI

        # Radio Button for Graduate Type Selection
        graduate_type = st.radio(
            "ÝOM tamamlan görnüşini saýlaň",
            options=["ÝOM tamamlanlar", "Daşary ýurdy tamamlap ykrar edilenler", "Ähli tamamlanlar"],
            index=2, # Default to "Combined"
            horizontal=True
        )

        # Adjust Data Based on Graduate Type Selection
        if graduate_type == "Ähli tamamlanlar":
            pivot_data["Tamamlanlar"] = (
                pivot_data["ÝOM tamamlanlar"] + pivot_data["Daşary ýurdy tamamlap ykrar edilenler"]
            )
            graduate_label = "Combined Graduates"
        elif graduate_type == "ÝOM tamamlanlar":
            pivot_data["Tamamlanlar"] = pivot_data["ÝOM tamamlanlar"]
            graduate_label = "ÝOM tamamlanlar"
        else:
            pivot_data["Tamamlanlar"] = pivot_data["Daşary ýurdy tamamlap ykrar edilenler"]
            graduate_label = "Daşary ýurdy tamamlap ykrar edilenler"

        # Step 1: Sector (Ugur) Selection
        selected_ugurs = st.multiselect(
            "   Ugur saýlaň",
            options=bazar_df["Ugur"].unique(),
            default=["Jemi"]
        )

        # Filter data based on selected sectors
        filtered_data = pivot_data[pivot_data["Ugur"].isin(selected_ugurs)]

        # Visualization 1: Line Chart
        if not filtered_data.empty:
            st.write("### Täze Kabul edilen ÝBI sany - ÝOM tamamlanlar")
            comparison_data = filtered_data.melt(
                id_vars=["Year", "Ugur"],
                value_vars=["Täze Kabul edilen ÝBI sany", "Tamamlanlar"],
                var_name="Category",
                value_name="Count"
            )
            fig_line = px.line(
                comparison_data,
                x="Year",
                y="Count",
                color="Category",
                line_group="Ugur",
                title="",
                labels={"Count": "Sany", "Category": "Katigoriýa", "Year": "Ýyl"},
                height=600
            )
            st.plotly_chart(fig_line)
        else:
            st.write("No data available for the selected sectors.")


        if not filtered_data.empty:
            comparison_data = filtered_data.melt(
                id_vars=["Year", "Ugur"],
                value_vars=["Täze Kabul edilen ÝBI sany", "Tamamlanlar"],
                var_name="Category",
                value_name="Count"
            )

            # Calculate Percentage Change
            comparison_data["Percentage Change"] = comparison_data.groupby(["Category", "Ugur"])["Count"].pct_change() * 100

            # Drop NaN values that result from pct_change for the first year
            percentage_change_data = comparison_data.dropna(subset=["Percentage Change"])

            st.write("### Göterim üýtgemegi: Täze Kabul edilen ÝBI sany we Tamamlanlar")
            fig_line_pct = px.line(
                percentage_change_data,
                x="Year",
                y="Percentage Change",
                color="Category",
                line_group="Ugur",
                title="",
                labels={"Percentage Change": "Göterim (%) ", "Category": "Katigoriýa", "Year": "Ýyl"},
                height=600
            )
            st.plotly_chart(fig_line_pct)

        else:
            st.write("No data available for the selected sectors.")


        # Visualization 2: Stacked Bar Chart
        if not filtered_data.empty:
            st.write("### Täze Kabul edilen ÝBI sanynyň - ÝOM tamamlanlara gatnaşygy")
            stacked_data = filtered_data.melt(
                id_vars=["Year", "Ugur"],
                value_vars=["Täze Kabul edilen ÝBI sany", "Tamamlanlar"],
                var_name="Metric",
                value_name="Value"
            )
            fig_stacked = px.bar(
                stacked_data,
                x="Year",
                y="Value",
                color="Metric",
                barmode="stack",
                facet_col="Ugur",
                title="",
                labels={"Year": "Ýyl", "Value": "Sany", "Metric": "Katigoriýa"},
                height=800
            )
            fig_stacked.update_layout(xaxis_type="category")

            st.plotly_chart(fig_stacked)

        # Visualization 3: Scatter Plot
        if not filtered_data.empty:
            st.write("### Correlation Between Selected Graduates and Workforce")
            fig_scatter = px.scatter(
                filtered_data,
                x="Tamamlanlar",
                y="Täze Kabul edilen ÝBI sany",
                size="Işgärleriň sany",
                color="Ugur",
                hover_name="Ugur",
                title="",
                labels={"Tamamlanlar":"Tamamlanlar", "Täze Kabul edilen ÝBI sany": "Täze Kabul edilen ÝBI sany"},
                height=600
            )
            st.plotly_chart(fig_scatter)
        else:
            st.write("No data available for scatter plot.")

if page == "Bazar çaklama":
    st.markdown("""
        ###  Täze Kabul edilen ÝBI sanynynyň hem-de Daşary ýurdy tamamlap ykrar edilenleriň 4 ýyl boýunça hasaplamalaryna görä çaklamalar. (Linear Regression)

        ######  Maksat:
        Bu çaklama, geljek ýyllar üçin işçi güýjüniň ösüşine we pudaklaýyn zerurlyklaryna baha bermäge kömek edip, her ýyl ÝOM tamamlan talyplaryň pudaklara ýerleşişine baha bermäge kömek eder. """)
  
    # Load Data
    forecasted_graduates_by_ugur = pd.read_csv("forecasted_graduates_by_ugur.csv")  # Year, Ugur, ÝOM tamamlajaklar
    workplace_data = pd.read_csv("forecasted_taze_kabul_edilen_ybi_sany.csv")  # Year, Ugur, Täze Kabul edilen ÝBI sany
    abroad_grads = pd.read_csv("forecasted_abroad_grads.csv")  # Year, Ugur, Daşary ýurdy tamamlap ykrar edilenler

    # University and Industry Ugur Mapping
    ugur_mapping = {
        "1. Matematika we tebigy ylymlar": [13, 14, 15, 16, 19, 20],
        "2. Inženerçilik işi, tehnologiýalar we tehniki ylymlar": [2, 3, 4, 5, 6, 8, 10, 13, 14, 15, 19, 20],
        "3. Saglygy goraýyş we lukmançylyk ylymlary": [17, 13, 14, 15, 19, 20],
        "4. Oba hojalygy we oba hojalyk ylymlary": [1, 13, 14, 15, 19, 20],
        "5. Jemgyýet baradaky ylymlar": [7, 9, 10, 11, 12, 13, 14, 15, 19, 20],
        "6. Bilim we pedagogika (mugallymçylyk) ylymlary": [13, 14, 15, 16, 19, 20],
        "7. Ynsanperwer ylymlar": [13, 14, 15, 16, 19, 20],
        "8. Sungat we medeniýet": [13, 14, 15, 16, 18, 19, 20],
    }

    # Industry Ugurs (Example list)
    industry_ugurs = [
        "1.Оba hojalygy, tokaý hojalygy we balyk tutmak",
        "2.Magdan gazyp çykaryjy senagat we känleri işläp taýýarlamak",
        "3.Işläp bejerýän önümçilikler",
        "4.Elektrik energiýasy, gaz, bug bilen üpjün etmek we howany kondisionirlemek",
        "5.Suw üpjünçiligi, galyndylary arassalamak, gaýtadan işlemek we ikinji çig maly almak",
        "6.Gurluşyk",
        "7.Lomaý we bölek satuw söwdasy; awtomobilleri we motosiklleri abatlamak",
        "8.Ulag işleri we ýükleri saklamak",
        "9.Myhmanhanalaryň we restoranlaryň işleri",
        "10.Habar beriş serişdeleri we aragatnaşyk",
        "11.Maliýe dellalçylygy we ätiýaçlandyrmak",
        "12.Gozgalmaýan emläk bilen bagly amallar",
        "13.Hünärmenlik, ylmy we tehniki işler",
        "14.Administratiw we kömekçi işler",
        "15.Döwlet dolandyryşy we goranmak; hökmany durmuş üpjünçilik",
        "16.Bilim",
        "17.Saglygy goraýyş we ilata durmuş taýdan hyzmat etmek",
        "18.Sungat, dynç alyş we göwün açyş",
        "19.Gaýry hyzmat ediş işler",
        "20. Işleriň gaýry görnüşleri",
    ]

    # Add "ALL" option to university and industry ugurs
    university_ugurs = ["Ählisi"] + list(ugur_mapping.keys())
    industry_ugurs = ["Ählisi"] + industry_ugurs

    # Step 1: Multiselect for University Ugur
    selected_university_ugurs = st.multiselect(
        "Uniwersitet ugur saýlaň ",
        options=university_ugurs,
        default=["Ählisi"]
    )

    # Step 2: Dynamically filter and sort Industry Ugurs based on University Ugur
    if "Ählisi" in selected_university_ugurs or not selected_university_ugurs:
        sorted_industry_ugurs = industry_ugurs
    else:
        matching_industry_ids = set(
            id for univ_ugur in selected_university_ugurs for id in ugur_mapping[univ_ugur]
        )
        industry_ugur_order = []
        for idx, industry in enumerate(industry_ugurs[1:], start=1):  # Skip "ALL"
            if idx in matching_industry_ids:
                industry_ugur_order.append((industry, True))  # Matching
            else:
                industry_ugur_order.append((industry, False))  # Non-Matching

        # Separate matching and non-matching industries
        matching_industries = [ind for ind, match in industry_ugur_order if match]
        non_matching_industries = [ind for ind, match in industry_ugur_order if not match]

        # Combine for display (matching first, then non-matching)
        sorted_industry_ugurs = ["Ählisi"] + matching_industries + ["--- Gabat gelmeýän pudaklar ---"] + non_matching_industries

    # Step 3: Multiselect for Industry Ugur (Sorted Options)
    selected_industry_ugurs = st.multiselect(
        "Bazar ugur saýlaň",
        options=sorted_industry_ugurs,
        default=["Ählisi"]
    )

    # Handle "ALL" selection in Industry Ugur
    if "Ählisi" in selected_industry_ugurs:
        selected_industry_ugurs = industry_ugurs[1:]  # Exclude "ALL"
    if "Ählisi" in selected_university_ugurs:
        selected_university_ugurs = university_ugurs[1:]  # Exclude "ALL"


    # Filter Dataframes
    filtered_forecasted_grads = forecasted_graduates_by_ugur[
        forecasted_graduates_by_ugur["Ugur"].isin(selected_university_ugurs)
    ]
    filtered_workplace_data = workplace_data[workplace_data["Ugur"].isin(selected_industry_ugurs)]
    filtered_abroad_grads = abroad_grads[abroad_grads["Ugur"].isin(selected_industry_ugurs)]

    # Combine Data for Unified Chart
    local_grads = filtered_forecasted_grads.rename(columns={"ÝOM tamamlajaklar": "Count"})
    local_grads["Category"] = "ÝOM tamamlajaklar"

    workplaces = filtered_workplace_data.rename(columns={"Täze Kabul edilen ÝBI sany": "Count"})
    workplaces["Category"] = "Täze Kabul edilen ÝBI sany"

    abroad = filtered_abroad_grads.rename(columns={"Daşary ýurdy tamamlap ykrar edilenler": "Count"})
    abroad["Category"] = "Daşary ýurdy tamamlap ykrar edilenler"

    combined_data = pd.concat([local_grads, workplaces, abroad], ignore_index=True)

    # Visualization: Combined Line Chart
    st.write("### Täze Kabul edilen ÝBI sany - Daşary ýurdy tamamlap ykrar edilenler - ÝOM tamamlajaklar")
    fig_combined = px.line(
        combined_data,
        x="Year",
        y="Count",
        color="Category",
        line_group="Ugur",
        title="",
        labels={"Year": "Ýyl", "Count": "Sany", "Category": "Katigoriýa"},
        height=600
    )
    st.plotly_chart(fig_combined)


    st.write("### Ýyl boýunça göterim üýtgemesi")
    combined_data["Percentage Change"] = combined_data.groupby(["Category", "Ugur"])[
        "Count"
    ].pct_change() * 100

    fig_growth = px.line(
        combined_data.dropna(subset=["Percentage Change"]),
        x="Year",
        y="Percentage Change",
        color="Category",
        line_group="Ugur",
        title="",
        labels={"Year": "Ýyl", "Percentage Change": "Göterim (%)", "Category": "Kategoriýa"},
        height=600
    )
    st.plotly_chart(fig_growth)

    # Calculate Growth
    workplace_growth = workplace_data.sort_values(by=["Ugur", "Year"])  # Sort by Ugur and Year
    workplace_growth["Growth"] = (
        workplace_growth.groupby("Ugur")["Täze Kabul edilen ÝBI sany"].pct_change() * 100
    )  # Calculate percentage growth

    # Fill NaN with 0 for the first year of each sector
    workplace_growth["Growth"] = workplace_growth["Growth"].fillna(0)

    # Visualization: Bar Chart of Growth
    st.write("### Bazar ugurlar boýunça täze Kabul edilen ÝBI sanynyň ösüşi")
    fig_top_sectors = px.bar(
        workplace_growth,
        x="Ugur",
        y="Growth",
        color="Ugur",
        title="",
        labels={"Ugur": "Ugur", "Growth": "Ösüş (%)"},
        height=600,
        text="Growth"  # Display growth percentage on bars
    )
    fig_top_sectors.update_traces(texttemplate='%{text:.2f}%', textposition='outside')  # Format text on bars
    st.plotly_chart(fig_top_sectors)


# Calculate Growth
    graduates_growth = forecasted_graduates_by_ugur.sort_values(by=["Ugur", "Year"])  # Sort by Ugur and Year
    graduates_growth["Growth"] = (
        graduates_growth.groupby("Ugur")["ÝOM tamamlajaklar"].pct_change() * 100
    )  # Calculate percentage growth

    # Fill NaN with 0 for the first year of each sector
    graduates_growth["Growth"] = graduates_growth["Growth"].fillna(0)

    # Visualization: Bar Chart of Growth
    st.write("### Uniwersitet ugurlar boýunça ÝOM tamamlajaklaryň ösüşi")
    fig_top_sectors_graduates = px.bar(
        graduates_growth,
        x="Ugur",
        y="Growth",
        color="Ugur",
        title="",
        labels={"Ugur": "Ugur", "Growth": "Ösüş (%)"},
        height=600,
        text="Growth"  # Display growth percentage on bars
    )
    fig_top_sectors_graduates.update_traces(texttemplate='%{text:.2f}%', textposition='outside')  # Format text on bars
    st.plotly_chart(fig_top_sectors_graduates)


    # st.write("### Proportion of Graduates and Newly Created Workplaces by Year")
    # fig_stacked = px.bar(
    #     combined_data,
    #     x="Year",
    #     y="Count",
    #     color="Category",
    #     barmode="stack",
    #     facet_col="Ugur",
    #     title="",
    #     labels={"Year": "Year", "Count": "Count", "Category": "Type"},
    #     height=800
    # )
    # st.plotly_chart(fig_stacked)

    st.write("### Täze Kabul edilen ÝBI sany - Daşary ýurdy tamamlap ykrar edilenler - ÝOM tamamlajaklar göterim paýy")
    selected_year = st.selectbox("Ýyl saýlaň    ", combined_data["Year"].unique())
    pie_data = combined_data[combined_data["Year"] == selected_year].groupby("Category")[
        "Count"
    ].sum().reset_index()

    fig_pie = px.pie(
        pie_data,
        names="Category",
        values="Count",
        title=f"Göterim paýy - {selected_year}",
        labels={"Category": "Kategoriýa", "Count": "Sany"},
        height=600
    )
    st.plotly_chart(fig_pie)

 