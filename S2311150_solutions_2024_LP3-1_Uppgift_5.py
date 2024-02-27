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

# Display the first few rows of each DataFrame to verify the correctness of the data and the merge operation.
# This step is crucial for debugging and ensuring that the data is loaded and merged as expected.
print("printing df_Regions.head()", '\n')
print(df_Regions.head(), '\n')

print("printing df_Inflation.head()", '\n')
print(df_Inflation.head(), '\n')

print("printing df_CPI.head()", '\n')
print(df_CPI.head(), '\n')

print("printing df_CPI_merged_with_Regions.head()", '\n')
print(df_CPI_merged_with_Regions.head(), '\n')

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 5
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# Lägg till en 'COUNTRY' kolumn i df_Inflation genom att matcha landskoder med df_Regions
# Notera att vi döper om 'Land' till 'COUNTRY'
df_Inflation_With_Country_From_Regions = pd.merge(df_Inflation, df_Regions.rename(columns={'Land': 'COUNTRY'}), left_on='LOCATION', right_on='Landskod', how='left')

# Behåll alla kolumner från df_Inflation och lägg till 'COUNTRY'
df_Inflation_With_Country_From_Regions = df_Inflation_With_Country_From_Regions[['COUNTRY'] + list(df_Inflation.columns)]

# Visa de första raderna för att kontrollera att allt ser korrekt ut
print("printing df_Inflation_With_Country_From_Regions.head()", '\n')
print(df_Inflation_With_Country_From_Regions.head(), '\n')