# C:\Users\TorosKutlu\Desktop\Borås Programmera mera i Python\Inlämningsuppgift_Programmera_mera_i_Python_LP3_2024-02-07-2\Python_code_Inlämningsuppgift_Programmera_mera_i_Python_LP3_2024-02-07-2\S2311150_solutions_2024_LP3-1.py

import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# Skapa DataFrame-objekten df_cpi, df_regions och df_inflation som innehåller en kopia av innehållet i csv-filerna cpi.csv, regions.csv och inflation.csv. Innehållet i dessa DataFrame-objekt ska du sedan använda för att lösa nedanstående uppgifter.------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# Load CPI data into a DataFrame
df_CPI = pd.read_csv(r'C:\Users\TorosKutlu\Desktop\Borås Programmera mera i Python\Inlämningsuppgift_Programmera_mera_i_Python_LP3_2024-02-07-2\cpi.csv', delimiter=';', encoding='ISO-8859-1')

# Load regional data into a DataFrame
df_Regions = pd.read_csv(r'C:\Users\TorosKutlu\Desktop\Borås Programmera mera i Python\Inlämningsuppgift_Programmera_mera_i_Python_LP3_2024-02-07-2\regions.csv', delimiter=';', encoding='ISO-8859-1')

# Load inflation data into a DataFrame
df_Inflation = pd.read_csv(r'C:\Users\TorosKutlu\Desktop\Borås Programmera mera i Python\Inlämningsuppgift_Programmera_mera_i_Python_LP3_2024-02-07-2\inflation.csv', encoding='utf-8')

# Merge the regions DataFrame with the CPI DataFrame on the country code
# This will add 'Land' and 'Kontinent' columns to the CPI data
df_CPI_merged_with_Regions = pd.merge(df_Regions[['Land', 'Landskod', 'Kontinent']], df_CPI, on='Landskod')

# Display the first few rows of the DataFrame to verify it's correct
print("printing df_Regions.head()")
print(df_Regions.head(), '\n')

print("printing df_Inflation.head()")
print(df_Inflation.head(), '\n')

print("printing df_CPI.head()")
print(df_CPI.head(), '\n')

# Display the first few rows of the merged DataFrame to verify it's correct
print("printing df_CPI_merged_with_Regions.head()")
print(df_CPI_merged_with_Regions.head(), '\n')

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 2
# Skriv ett program där man först väljer de länder som ska ingå i analysen (max 3 länder). Avsluta inmatningen genom att mata in ordet END. Programmet ska därefter plotta inflationen (CPI) under tidsperioden 1960-2022 för de valda länderna i ett linjediagram med ett utseende enligt nedanstående figur. Linjediagrammets titel ska vara ’Inflation under tidsperioden 1960-2022. I graferna ska också högsta- och lägsta förekommande inflation per land markeras med en röd respektive blå cirkel. Ländernas namn ska finnas angivna i diagrammets etikett.
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
def plot_inflation(df, countries):
    """
    Plot the inflation rate from 1960 to 2022 for the selected countries.
    The highest and lowest inflation rates are marked with a red and blue dot respectively.
    """
    plt.figure(figsize=(10, 5))

    for country in countries:
        country_data = df[df['Land'] == country].iloc[:, 3:].T
        country_data.columns = ['Inflation']
        plt.plot(country_data, label=country)

        # Highlight the max and min inflation values
        max_value = country_data['Inflation'].max()
        max_year = country_data['Inflation'].idxmax()
        min_value = country_data['Inflation'].min()
        min_year = country_data['Inflation'].idxmin()
        
        plt.scatter(max_year, max_value, color='red')
        plt.scatter(min_year, min_value, color='blue')
        plt.text(max_year, max_value, f'{max_value:.2f}%', ha='center', va='bottom', color='red')
        plt.text(min_year, min_value, f'{min_value:.2f}%', ha='center', va='top', color='blue')

    plt.title('Inflation during the years 1960-2022')
    plt.xlabel('Year')
    plt.ylabel('Inflation Rate (%)')
    plt.legend()
    plt.grid(True)

    # Rotate x-axis labels to display years vertically
    plt.xticks(rotation=90)
    
    plt.show()

# Input loop for selecting countries
selected_countries = []
print("Enter the names of the countries you want to analyze (max 3). Type 'END' to finish:")

while len(selected_countries) < 3:
    country = input("Enter country name: ")
    if country == 'END':
        break
    if country in df_CPI_merged_with_Regions['Land'].values:
        selected_countries.append(country)
    else:
        print("Country not found, please enter a valid country name.")

# Plotting the inflation for the selected countries
if selected_countries:
    plot_inflation(df_CPI_merged_with_Regions, selected_countries)
else:
    print("No countries selected for analysis.")

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 3
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:




# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 4
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:




# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 5
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:



