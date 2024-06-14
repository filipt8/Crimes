import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    data = pd.read_csv('./daneprojekt/Crime_Data_2010_2017.csv')
    df = pd.DataFrame(data)
    return df

dane = load_data()

total_crimes = len(dane)
top_crimes = dane['Crime Code Description'].value_counts().nlargest(5)

new_names = [
    "Nieporządany dotyk - groźba / próba",
    "Kradzież pojazdu",
    "Włamanie do pojazdu",
    "Włamanie",
    "Kradzież do $950"
]

top_crimes.index = new_names
top_crimes_total = top_crimes.sum()
top_crimes_percentage = (top_crimes_total / total_crimes) * 100

plt.figure(figsize=(12, 8))
barplot = top_crimes.plot(kind='barh', color='crimson', edgecolor='black')

for index, value in enumerate(top_crimes):
    plt.text(value / 2, index, str(value), ha='center', va='center', fontsize=12, color='black')

plt.title('Najczęstsze przestępstwa')
plt.xlabel('Liczba popełnionych przestępstw')
plt.ylabel('Rodzaj przestępstwa')

plt.text(top_crimes.max(), len(top_crimes) - 0.5, 
         f'Top 5 to {top_crimes_percentage:.2f}% wszystkich przestępstw',
         ha='right', fontsize=12, color='black')

plt.gca().invert_yaxis()
plt.show()
