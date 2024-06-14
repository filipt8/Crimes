import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


def load_data():
    data = pd.read_csv('./daneprojekt/Crime_Data_2010_2017.csv')
    df = pd.DataFrame(data)
    return df

def days(dane, plec, narod, wiek):
    dane['Date Occurred'] = pd.to_datetime(dane['Date Occurred'], format='%m/%d/%Y')

    if isinstance(plec, str):
        plec = [plec]
    
    if isinstance(narod, str):
        narod = [narod]

    min_wiek, max_wiek = wiek

    dane_filtered = dane[(dane['Victim Sex'].isin(plec)) &
                         (dane['Victim Descent'].isin(narod)) &
                         (dane['Victim Age'].between(min_wiek, max_wiek))]

    dane_filtered['Day'] = dane['Date Occurred'].dt.day_name()

    days_mapping = {
        'Monday': 'Poniedziałek', 'Tuesday': 'Wtorek', 'Wednesday': 'Środa',
        'Thursday': 'Czwartek', 'Friday': 'Piątek', 'Saturday': 'Sobota', 'Sunday': 'Niedziela'
    }

    days_order = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]

    dane_filtered['Day_PL'] = dane_filtered['Day'].map(days_mapping)

    day_counts = dane_filtered['Day_PL'].value_counts().reindex(days_order, fill_value=0)

    df_days = pd.DataFrame({'Day': day_counts.index, 'Count': day_counts.values})

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='Count', y='Day', data=df_days, palette='light:#5A9_r', edgecolor='black')

    max_value = df_days['Count'].max()
    plt.axvline(max_value, color='red', linewidth=1, linestyle='--')

    for index, value in enumerate(df_days['Count']):
        plt.text(value / 2, index, f"({value})", va='center', fontsize=12, fontweight='bold')

    plt.xlabel('Liczba przestępstw')
    plt.ylabel('Dzień')
    plt.title('Liczba przestępstw w poszczególnych dniach')
    plt.yticks(fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    return plt.gcf()




def months(dane, plec, narod, wiek):
    dane['Date Occurred'] = pd.to_datetime(dane['Date Occurred'], format='%m/%d/%Y')

    if isinstance(plec, str):
        plec = [plec]
    
    if isinstance(narod, str):
        narod = [narod]

    min_wiek, max_wiek = wiek

    dane_filtered = dane[(dane['Victim Sex'].isin(plec)) &
                         (dane['Victim Descent'].isin(narod)) &
                         (dane['Victim Age'].between(min_wiek, max_wiek))]

    dane_filtered['Month'] = dane_filtered['Date Occurred'].dt.strftime('%b')
    month_mapping = {
        'Jan': 'Styczeń', 'Feb': 'Luty', 'Mar': 'Marzec', 'Apr': 'Kwiecień',
        'May': 'Maj', 'Jun': 'Czerwiec', 'Jul': 'Lipiec', 'Aug': 'Sierpień',
        'Sep': 'Wrzesień', 'Oct': 'Październik', 'Nov': 'Listopad', 'Dec': 'Grudzień'
    }
    dane_filtered['Month_PL'] = dane_filtered['Month'].map(month_mapping)

    miesiace = ["Styczeń", "Luty", "Marzec", "Kwiecień",
                "Maj", "Czerwiec", "Lipiec", "Sierpień",
                "Wrzesień", "Październik", "Listopad", "Grudzień"]
    miesiacliczba = dane_filtered['Month_PL'].value_counts().reindex(miesiace, fill_value=0)

    msc = pd.DataFrame({'Miesiąc': miesiace, 'Liczba przestępstw': miesiacliczba.values})

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='Liczba przestępstw', y='Miesiąc', data=msc, palette='light:#5A9_r', edgecolor='black')

    max_value = msc['Liczba przestępstw'].max()
    plt.axvline(max_value, color='red', linewidth=1, linestyle='--')

    for index, value in enumerate(msc['Liczba przestępstw']):
        plt.text(value / 2, index, f"({value})", va='center', ha='center', fontsize=10, color='black', fontweight='bold')

    plt.xlabel('Liczba przestępstw')
    plt.ylabel('Miesiąc')
    plt.title('Liczba przestępstw w poszczególnych miesiącach')

    return plt.gcf()



def hours(dane, plec, narod, wiek):
    def convert_time_occured(time):
        time = f"{int(time):04d}"
        hour = int(time[:2])
        minute = int(time[2:])
        return pd.to_datetime(f'{hour:02}:{minute:02}', format='%H:%M').time()
    
    dane['Time Occurred'] = dane['Time Occurred'].apply(convert_time_occured)

    if isinstance(plec, str):
        plec = [plec]
    
    if isinstance(narod, str):
        narod = [narod]

    min_wiek, max_wiek = wiek

    dane_filtered = dane[(dane['Victim Sex'].isin(plec)) &
                         (dane['Victim Descent'].isin(narod)) &
                         (dane['Victim Age'].between(min_wiek, max_wiek))]

    dane_filtered['Hour'] = dane_filtered['Time Occurred'].apply(lambda x: x.hour)

    hour_counts = dane_filtered['Hour'].value_counts().sort_index()

    df_hours = pd.DataFrame({'Hour': hour_counts.index, 'Count': hour_counts.values})

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='Hour', y='Count', data=df_hours, palette='light:#5A9_r', edgecolor='black')

    max_value = df_hours['Count'].max()
    plt.axhline(max_value, color='red', linewidth=1, linestyle='--')

    for index, value in enumerate(df_hours['Count']):
        plt.text(index, value + max_value * 0.01, f"({value})", ha='center', fontsize=9, fontweight='bold')

    plt.xlabel('Godzina')
    plt.ylabel('Liczba przestępstw')
    plt.title('Liczba przestępstw w poszczególnych godzinach')
    plt.xticks(range(24), fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    return plt.gcf()





def allthetime(dane, plec, narod, wiek):
    dane['Date Occurred'] = pd.to_datetime(dane['Date Occurred'], format='%m/%d/%Y')

    if isinstance(plec, str):
        plec = [plec]
    
    if isinstance(narod, str):
        narod = [narod]

    min_wiek, max_wiek = wiek

    dane_filtered = dane[(dane['Victim Sex'].isin(plec)) &
                         (dane['Victim Descent'].isin(narod)) &
                         (dane['Victim Age'].between(min_wiek, max_wiek))]

    dane_filtered.set_index('Date Occurred', inplace=True)
    crimes_per_month = dane_filtered.resample('M').size()

    plt.figure(figsize=(12, 6))
    crimes_per_month.plot(marker='o', linestyle='-', color='crimson', linewidth=2)

    plt.title('Liczba przestępstw w ciągu lat')
    plt.xlabel('Data')
    plt.ylabel('Liczba przestępstw')
    plt.grid(True)
    plt.tight_layout()

    return plt.gcf()




def crimesline(dane, plec, narod, wiek, crimes):
    dane['Date Occurred'] = pd.to_datetime(dane['Date Occurred'], format='%m/%d/%Y')

    if isinstance(plec, str):
        plec = [plec]
    
    if isinstance(narod, str):
        narod = [narod]

    if isinstance(crimes, str):
        narod = [crimes]

    min_wiek, max_wiek = wiek

    dane_filtered = dane[(dane['Victim Sex'].isin(plec)) &
                         (dane['Victim Descent'].isin(narod)) &
                         (dane['Crime Code Description'].isin(crimes)) &
                         (dane['Victim Age'].between(min_wiek, max_wiek))]

    dane_filtered.set_index('Date Occurred', inplace=True)
    
    plt.figure(figsize=(12, 6))

    for crime in crimes:
        crimes_per_month = dane_filtered[dane_filtered['Crime Code Description'] == crime].resample('M').size()
        crimes_per_month.plot(marker='o', linestyle='-', linewidth=2, label=crime)

    plt.title('Liczba przestępstw w czasie')
    plt.xlabel('Data')
    plt.ylabel('Liczba przestępstw')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.ylim(bottom=0)

    return plt.gcf()

# hours(load_data(), ['M', 'F'],['B', 'W'],(29, 33))
# months(load_data(), ['M', 'F'],['B', 'W'],(29, 33))
# days(load_data(), ['M', 'F'],['B', 'W'],(29, 30))
