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

# Calculate inflation
for year in range(1961, 2023):  # Start from 1961 since we need the previous year's CPI
    df_CPI_merged_with_Regions[f'Inflation_{year}'] = ((df_CPI_merged_with_Regions[str(year)] - df_CPI_merged_with_Regions[str(year-1)]) / df_CPI_merged_with_Regions[str(year-1)]) * 100

# Initialize the summary DataFrame
columns = ['Continent', 'Average_Inflation', 'Top_3_Inflations', 'Bottom_3_Inflations']
df_Summary = pd.DataFrame(columns=columns)

# Aggregate data
for continent in df_CPI_merged_with_Regions['Kontinent'].unique():
    continent_data = df_CPI_merged_with_Regions[df_CPI_merged_with_Regions['Kontinent'] == continent]
    avg_inflation = continent_data[[f'Inflation_{year}' for year in range(1961, 2023)]].mean().mean()
    
    # Flatten the DataFrame and sort to find top and bottom inflations
    flattened = continent_data.melt(id_vars=['Land', 'Kontinent'], value_vars=[f'Inflation_{year}' for year in range(1961, 2023)], var_name='Year', value_name='Inflation').dropna()
    top_3 = flattened.nlargest(3, 'Inflation')
    bottom_3 = flattened.nsmallest(3, 'Inflation')
    
    # Append to the summary DataFrame
    df_Summary = df_Summary.append({'Continent': continent, 'Average_Inflation': avg_inflation, 'Top_3_Inflations': top_3, 'Bottom_3_Inflations': bottom_3}, ignore_index=True)

print(type(df_Summary))

# Display or save the summary
print(df_Summary)