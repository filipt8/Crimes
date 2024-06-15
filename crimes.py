import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plots import load_data, months, days, hours, allthetime, crimesline, geo_crime, percentage, area
import plotly.express as px
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Analiza danych kryminalnych')
dane = load_data()


if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = None
    st.session_state.genre = None

if st.sidebar.button('ZBIÓR'):
    st.session_state.button_clicked = 'opis_zbioru'
    st.session_state.genre = None

if st.sidebar.button('WYKRESY'):
    st.session_state.button_clicked = 'wykresy'

if st.sidebar.button('TEST'):
    st.session_state.button_clicked = 'test'

#####################################################################################

rasy = ('A - Inna Azjatycka',
        'B - Osoba czarnoskóra',
        'C - Chińska',
        'D - Kambodżańska',
        'F - Filipińska ',
        'G - Guamiańska',
        'H - Hiszpańska / Latynoska / Meksykańska',
        'I - Amerykański Indianin / Obywatel Alaski',
        'J - Japońska',
        'K - Koreańska',
        'L - Laotańska',
        'O - Inna',
        'P - Obywatel wysp Pacyfiku',
        'S - Samoańska',
        'U - Hawajska',
        'V - Wietnamska',
        'W - Osoba białoskóra',
        'X - Nieznana',
        'Z - Azjatycki Indianin')
victim_ages = sorted(dane['Victim Age'].unique())

######################################################################################

if st.session_state.button_clicked == 'opis_zbioru':
    url = "https://www.kaggle.com/datasets/cityofLA/crime-in-los-angeles"
    
    st.session_state.genre = st.sidebar.radio(
        "",
        ["***Opis zbioru i zmiennych***", "***Przykładowe dane***"],
        index=None
    )

    if 'data' not in st.session_state:
        st.session_state.data = load_data()

    if st.session_state.genre:
        if st.session_state.genre == "***Przykładowe dane***":
            #st.write("Wybrano opcję Dane --- przerzucić wyżej")
            st.dataframe(st.session_state.data.head(100))
        elif st.session_state.genre == "***Opis zbioru i zmiennych***":
            st.header("Crimes in Los Angeles")
            st.write(f"""
                    Zbiór przestępstw popełnionych od początku 2010r. do września 2017r.
                    Znajdują się w nim dane dotyczące przestępstw i wykroczeń na terenie całego Los Angeles.
                    Zajmiemy się następującymi kwestiami:
                    Link do źródła danych [kaggle.com]({url})
            """)
            st.subheader("Opis zmiennych")
            st.write("""
                    Numer zgłoszenia - `DR Number`

                    Data zgłoszenia - `Date Reported`

                    Data zdarzenia - `Date Occurred`

                    Godzina zdarzenia - `Time Occurred`

                    Miejsce zdarzenia - `Area ID`, `Area Name`, `Reporting District`

                    Kod i opis zdarzenia - `Crime Code`, `Crime Code Description`

                    Kod Modus Operandi, który pozwala na krótki opis zdarzeń przestępstwa - `MO Codes`

                    Wiek, płeć, oraz narodowość ofiary - `Victim Age`, `Victim Sex`, `Victim Descent`

                    Kod miejsca wraz z opisem - `Premise Code`, `Premise Description`

                    Kod broni użytej podczas interwencji wraz z opisem - `Weapon Used Code`, `Weapon Description`

                    Kod opisujący zakończenie akcji - `Status Description`

                    Adres zdarzenia - `Address`, `Cross Street`, `Location` 
            """)

##########################################################################################

elif st.session_state.button_clicked == 'wykresy':
    st.session_state.genre = st.sidebar.radio(
        "",
        ["***Oś czasu***", "***Top 5***","***Geolokacja***"],
        index=None
    )

    if st.session_state.genre:
        if st.session_state.genre == "***Oś czasu***":
            
            period_filter = st.sidebar.selectbox("Oś czasu:",
                ("Całościowa","Miesięczna", "Tygodniowa", "Godzinowa"))
            
            gender_filter = st.sidebar.multiselect('Płeć ofiary:', ['M', 'F', 'H', 'X'], default=['M', 'F'])

            start_age, end_age = st.sidebar.select_slider(
                "Przedział wiekowy",
                options=victim_ages,
                value=(min(victim_ages), max(victim_ages)))

            nationality_unique = dane['Victim Descent'].unique()
            nationality_filter = st.sidebar.multiselect("Narodowość ofiary:",nationality_unique, default=['W', 'B'])

            if period_filter == "Całościowa":
                result = allthetime(dane, gender_filter, nationality_filter, (start_age, end_age))
                st.pyplot(result)
                for i in range(0, len(rasy), 4):
                    st.write(", ".join(rasy[i:i+4]))
            elif period_filter == "Miesięczna":
                result = months(dane, gender_filter, nationality_filter, (start_age, end_age))
                st.pyplot(result)
                for i in range(0, len(rasy), 4):
                    st.write(", ".join(rasy[i:i+4]))
            elif period_filter == "Tygodniowa":
                result = days(dane, gender_filter, nationality_filter, (start_age, end_age))
                st.pyplot(result)
                for i in range(0, len(rasy), 4):
                    st.write(", ".join(rasy[i:i+4]))
            elif period_filter == "Godzinowa":
                result = hours(dane, gender_filter, nationality_filter, (start_age,end_age))
                st.pyplot(result)
                for i in range(0, len(rasy), 4):
                    st.write(", ".join(rasy[i:i+4]))

        elif st.session_state.genre == "***Top 5***":
            crimes_unique = dane['Crime Code Description'].unique()
            crimes_filter = st.sidebar.multiselect("Przestępstwo:",crimes_unique, default=['BATTERY - SIMPLE ASSAULT','BURGLARY FROM VEHICLE','BURGLARY','THEFT PLAIN - PETTY ($950 & UNDER)'])

            gender_filter = st.sidebar.multiselect('Płeć ofiary:', ['M', 'F', 'H', 'X'], default=['M', 'F'])

            start_age, end_age = st.sidebar.select_slider(
                "Przedział wiekowy",
                options=victim_ages,
                value=(min(victim_ages), max(victim_ages)))

            nationality_unique = dane['Victim Descent'].unique()
            nationality_filter = st.sidebar.multiselect("Narodowość ofiary:",nationality_unique, default=['W', 'B'])


            st.write('Niestety przy filtrowaniu dla przestępstwa `VEHICLE - STOLEN` jego wykres będzie praktycznie powielał oś X ze względu na to, że dane nie posiadają kolumny opisującej winowajce a jedynie ofiare przestępstwa.')

            col1, col2 = st.columns(2)
            with col1:
                st.image('./top5plot.png', caption='Top 5 najczęściej popełnianych przestępstw')

            with col2:    
                result = crimesline(dane, gender_filter, nationality_filter, (start_age,end_age), crimes_filter)
                st.pyplot(result)

            for i in range(0, len(rasy), 4):
                    st.write(", ".join(rasy[i:i+4]))
            
        elif st.session_state.genre == "***Geolokacja***":
            crimes_unique = dane['Crime Code Description'].unique()
            crimes_filter = st.sidebar.selectbox("Przestępstwo:",crimes_unique)

            prc = percentage(dane,crimes_filter)
            area_n = area(dane, crimes_filter)
            st.write(f"{crimes_filter} stanowi: {prc:.2f}% wszystkich przestępstw.")
            st.write(f"Najniebezpieczniejszą dzielnicą pod względem tego przestępstwa jest: {area_n}")

            result = geo_crime(dane, crimes_filter)
            st.pyplot(result)
            

#WSZĘDZIE MOŻESZ DODAĆ st.sidebar.selectbox CZY COŚ ŻEBY TO MIAŁO RĘCE I NOGI
#np. DLA MIESIĘCY... DLA POSZCZEGÓLNEGO PRZESTĘPSTWA - TAK SAMO PŁEĆ ITD
#MOŻNA DODAĆ TEKSTOWĄ CIEKAWOSTKE, ŻE NP. NAJMŁODSZA OFIARA BYŁA BIAŁA WIEK TYLE A NAJSTARSZA TYLE.

#PAMIETAJ JAKIEŚ ZJEBANE MODELE NA SZYBKO SKLEIĆ ZE 3 I POKAZAĆ ICH PLOTY

#MOŻESZ DOROBIĆ DO TEGO CZATBOTA, KTÓRY NA PODSTAWIE PODANYCH INFORMACJI SPRÓBUJE PRZEWIDZIEĆ KTO POPEŁNIŁ PRZESTĘPSTWO
#ALE TO JUŻ ZBYT POJEBANE CHYBA
#COŚ W STYLU PROFILERA - ZROBIŁA TO I TO, Z BRONIĄ W RĘKU, W TYM MIEJSCU O TEJ GODZINIE

#####################################################################################################

if st.session_state.button_clicked == 'test':
    gender_filter = st.sidebar.selectbox('Filter by Gender', ['All', 'Male', 'Female'])
    