# C:\Users\TorosKutlu\Desktop\Borås Programmera mera i Python\Inlämningsuppgift_Programmera_mera_i_Python_LP3_2024-02-07-2\Python_code_Inlämningsuppgift_Programmera_mera_i_Python_LP3_2024-02-07-2\S2311150_solutions_2024_LP3-1.py

import pandas as pd

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
# Uppgift 4
# I denna uppgift ska du analysera inflationen som har uppmätts per kontinent under tidsperioden 1960-2022 enligt den uppdelning som finns i kolumnen Kontinent i df_region. Skriv ett program som använder informationen i df_cpi och df_region och som skapar en tabell som dels presenterar medelinflationen per kontinent under tidsperioden 1960-2022 samt de 3 högsta- och de 3 lägsta förekommande inflationerna per kontinent under tidsperioden och i vilka länder dessa inflationer uppmättes...------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

import numpy as np

# Calculate the mean inflation per continent for the period of 1960-2022
# We first melt the DataFrame to long format, group by continent, and then calculate the mean
df_melted = df_CPI_merged_with_Regions.melt(id_vars=['Land', 'Landskod', 'Kontinent'], var_name='Year', value_name='Inflation')
continent_mean_inflation = df_melted.groupby('Kontinent')['Inflation'].mean().reset_index()
continent_mean_inflation.rename(columns={'Inflation': 'average_yearly_inflation_for_period_1960_2022'}, inplace=True)

# Now, we find the top 3 and bottom 3 inflation rates per continent
def top_bottom_inflation(df, n=3):
    top = df.nlargest(n, 'Inflation')[['Land', 'Year', 'Inflation']]
    bottom = df.nsmallest(n, 'Inflation')[['Land', 'Year', 'Inflation']]
    return pd.concat([top, bottom], keys=['Top', 'Bottom'])

inflation_extremes = df_melted.groupby('Kontinent').apply(top_bottom_inflation).reset_index().drop('level_1', axis=1)

# Display the result
print(continent_mean_inflation)
print(inflation_extremes)