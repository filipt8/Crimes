import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plots import load_data, months, days, hours, allthetime, crimesline, geo_crime, percentage, area
import plotly.express as px
import joblib
import time

st.title('Analiza danych kryminalnych')
dane = load_data()

####################################################################################

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = None
    st.session_state.genre = None

if st.sidebar.button('ZBIÓR'):
    st.session_state.button_clicked = 'opis_zbioru'
    st.session_state.genre = None

if st.sidebar.button('WYKRESY'):
    st.session_state.button_clicked = 'wykresy'

if st.sidebar.button('CHATBOT'):
    st.session_state.button_clicked = 'Chatbot'

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
                    Aplikacja obsługuje zbiór przestępstw popełnionych od początku 2010r. do września 2017r. na terenie całego Los Angeles.
                    
                    Dane w zbiorze są bardzo zróżnicowane, znaleźć w nich możemy przestępstwo dotyczące wykolejenia pociągu, które miało miejsce raz przez okres prawie 7 lat podczas gdy BATTERY - SIMPLE ASSAULT czyli próba wymuszenia 
                    'niepożądanego dotyku' drugiej osoby była odnotowana aż 145767 razy.
                     
                    Dane zawierają dosyć szczegółowe informacje na temat lokalizacji miejsca przestępstwa, czasu jego dokonania, ofiary, narzędzia zbrodni czy kodu Modus Operandi (charakterystyczna metoda, wzorzec lub technika działania).

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

                    Kod opisujący zakończenie akcji - ``Status Code, `Status Description`

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
            
if st.session_state.button_clicked == 'Chatbot':
    model = joblib.load('random_forest_model_crimes_10k_2.pkl')
    preprocessor = joblib.load('preprocessor_crimes_10k_2.pkl')

    dane['Weapon Used Code'] = dane['Weapon Used Code'].fillna(0)
    dane['Weapon Description'] = dane['Weapon Description'].fillna('NO WEAPON USED')
    dane['MO Codes'] = dane['MO Codes'].fillna('')
    data = dane.dropna(subset=['Area Name', 'Premise Description', 'Status Description', 'Victim Sex', 'Victim Descent'])

    mo_codes_data = pd.read_csv('MO_Codes.csv')

    mo_codes_dict = dict(zip(mo_codes_data['Description'], mo_codes_data['MO_Code']))
    mo_codes_unique = list(mo_codes_dict.keys())

    bins = [0, 21, 29, 39, 51, 100]
    labels = ['10-21', '22-29', '30-39', '40-51', '52-100']
    data['Victim Age'] = pd.cut(data['Victim Age'], bins=bins, labels=labels, right=False)

    area_dict = dict(zip(data['Area ID'], data['Area Name']))
    premise_dict = dict(zip(data['Premise Code'], data['Premise Description']))
    weapon_dict = dict(zip(data['Weapon Used Code'], data['Weapon Description']))
    status_dict = dict(zip(data['Status Code'], data['Status Description']))
    
    crime_code_dict = dict(zip(data['Crime Code'], data['Crime Code Description']))

    victim_descent_dict = {
        "A": "Other Asian", "B": "Black", "C": "Chinese", "D": "Cambodian",
        "F": "Filipino", "G": "Guamanian", "H": "Hispanic/Latin/Mexican",
        "I": "American Indian/Alaskan Native", "J": "Japanese", "K": "Korean",
        "L": "Laotian", "O": "Other", "P": "Pacific Islander", "S": "Samoan",
        "U": "Hawaiian", "V": "Vietnamese", "W": "White", "X": "Unknown", "Z": "Asian Indian"
    }
    victim_descent_unique = list(victim_descent_dict.values())
    status_desc_unique = data['Status Description'].dropna().unique()

    def typewriter(text: str, speed: int):
        tokens = text.split()
        container = st.empty()
        for index in range(len(tokens) + 1):
            curr_full_text = " ".join(tokens[:index])
            container.markdown(curr_full_text)
            time.sleep(1 / speed)

    def predict_crime(victim_age, victim_sex, victim_descent, premise_desc, area_name, weapon_desc, time_occurred, mo_descs, status_desc):
        premise_code = list(premise_dict.keys())[list(premise_dict.values()).index(premise_desc)]
        area_id = list(area_dict.keys())[list(area_dict.values()).index(area_name)]
        weapon_used_code = list(weapon_dict.keys())[list(weapon_dict.values()).index(weapon_desc)]
        status_code = list(status_dict.keys())[list(status_dict.values()).index(status_desc)]
        
        # Join multiple MO Codes into a single string separated by commas
        mo_codes = ','.join([str(mo_codes_dict[mo_desc]) for mo_desc in mo_descs])

        input_data = pd.DataFrame({
            'Victim Age': [victim_age],
            'Victim Sex': [victim_sex],
            'Victim Descent': [victim_descent],
            'Premise Code': [premise_code],
            'Area ID': [area_id],
            'Weapon Used Code': [weapon_used_code],
            'Time Occurred': [time_occurred],
            'MO Codes': [mo_codes],
            'Status Code': [status_code]
        })

        input_data['Victim Age'] = input_data['Victim Age'].astype(str)
        input_data['Victim Sex'] = input_data['Victim Sex'].astype(str)
        input_data['Victim Descent'] = input_data['Victim Descent'].astype(str)
        input_data['Premise Code'] = input_data['Premise Code'].astype(str)
        input_data['Area ID'] = input_data['Area ID'].astype(str)
        input_data['Weapon Used Code'] = input_data['Weapon Used Code'].astype(str)
        input_data['Time Occurred'] = input_data['Time Occurred'].astype(str)
        input_data['MO Codes'] = input_data['MO Codes'].astype(str)
        input_data['Status Code'] = input_data['Status Code'].astype(str)

        input_processed = preprocessor.transform(input_data)

        prediction = model.predict(input_processed)
        crime_code = prediction[0]
        crime_description = crime_code_dict.get(crime_code, "Unknown Crime Code")
        return crime_description
    
    st.write('Status Description: ')
    st.write('Adult Other - osoba dorosła była zaangażowana w incydent')
    st.write('Invest Cont - śledztwo w sprawie tego przestępstwa jest nadal w toku')
    st.write('Adult Arrest - osoba dorosła została aresztowana w związku z tym incydentem')
    st.write('Juv Arrest - osoba niepełnoletnia została aresztowana w związku z tym przestępstwem')
    st.write('Juv Other - osoba niepełnoletnia była zaangażowana w incydent')
    st.write('UNK - nieznane')

    with st.form("crime_prediction_form"):
        st.write("Please enter the details:")
        victim_age = st.selectbox('Victim Age', labels)
        victim_sex = st.selectbox('Victim Sex', ['M', 'F'])
        victim_descent_desc = st.selectbox('Victim Descent', victim_descent_unique)
        premise_desc = st.selectbox('Premise Description', list(premise_dict.values()))
        area_name = st.selectbox('Area Name', list(area_dict.values()))
        weapon_desc = st.selectbox('Weapon Description', list(weapon_dict.values()))
        time_occurred = st.number_input('Time Occurred', min_value=0, max_value=2359, step=1)
        mo_desc = st.multiselect('MO Codes', mo_codes_unique)
        status_desc = st.selectbox('Status Description', status_desc_unique)
        submitted = st.form_submit_button("Predict Crime Code")

        if submitted:
            result = predict_crime(victim_age, victim_sex, victim_descent_desc, premise_desc, area_name, weapon_desc, time_occurred, mo_desc, status_desc)
            typewriter(text=f'The predicted Crime Code is: :rainbow[{result}]', speed=5)

    