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

# Ensure all CPI data columns are numeric
for year in range(1960, 2023):  # Assuming CPI data spans from 1960 to 2022
    df_CPI_merged_with_Regions[str(year)] = pd.to_numeric(df_CPI_merged_with_Regions[str(year)], errors='coerce')

# Forward fill to address the FutureWarning
df_CPI_merged_with_Regions.iloc[:, 4:] = df_CPI_merged_with_Regions.iloc[:, 4:].ffill(axis=1)

# Calculate inflation rates as year-over-year changes in CPI
for year in range(1961, 2023):  # Start from 1961 since we need the previous year's data to calculate inflation
    prev_year = str(year - 1)
    current_year = str(year)
    df_CPI_merged_with_Regions[f'Inflation_{current_year}'] = ((df_CPI_merged_with_Regions[current_year] - df_CPI_merged_with_Regions[prev_year]) / df_CPI_merged_with_Regions[prev_year]) * 100

# Filter for columns that contain 'Inflation_' and 'Kontinent'
inflation_columns = [col for col in df_CPI_merged_with_Regions.columns if 'Inflation_' in col]
df_inflation_only = df_CPI_merged_with_Regions[['Kontinent'] + inflation_columns]

# Aggregate inflation data by continent
aggregated_inflation = df_inflation_only.groupby('Kontinent').agg(['mean', 'max', 'min'])

# Print the aggregated inflation data to verify
print(aggregated_inflation)

# Convert CPI values to numeric, ignoring non-numeric values which will become NaN
for year in range(1960, 2023):  # Assuming CPI data spans from 1960 to 2022
    df_CPI_merged_with_Regions[str(year)] = pd.to_numeric(df_CPI_merged_with_Regions[str(year)], errors='coerce')

# Calculate inflation rates as year-over-year changes in CPI
for year in range(1961, 2023):  # Start from 1961 since we need the previous year's data to calculate inflation
    prev_year = str(year - 1)
    current_year = str(year)
    df_CPI_merged_with_Regions[f'Inflation_{current_year}'] = ((df_CPI_merged_with_Regions[current_year] - df_CPI_merged_with_Regions[prev_year]) / df_CPI_merged_with_Regions[prev_year]) * 100

# Initialize a DataFrame to hold aggregated data
columns = ['Continent', 'Average_Inflation', 'Max_Inflation', 'Max_Inflation_Country', 'Max_Inflation_Year', 'Min_Inflation', 'Min_Inflation_Country', 'Min_Inflation_Year']

# Initialize a DataFrame to hold aggregated data
aggregated_data = pd.DataFrame(columns=['Continent', 'Average_Inflation', 'Max_Inflation', 'Max_Inflation_Country', 'Max_Inflation_Year', 'Min_Inflation', 'Min_Inflation_Country', 'Min_Inflation_Year'])

# Iterate over each continent
for continent in df_CPI_merged_with_Regions['Kontinent'].unique():
    continent_data = df_CPI_merged_with_Regions[df_CPI_merged_with_Regions['Kontinent'] == continent]

    # Calculate the mean, max, and min inflation for the continent
    mean_inflation = continent_data[inflation_columns].mean().mean()
    max_inflation = continent_data[inflation_columns].max().max()
    min_inflation = continent_data[inflation_columns].min().min()

    # Find the index of the max and min inflation within the continent data
    max_inflation_idx = continent_data[inflation_columns].max(axis=1).idxmax()
    min_inflation_idx = continent_data[inflation_columns].min(axis=1).idxmin()

    # Extract the country and year for max inflation
    max_inflation_country = continent_data.loc[max_inflation_idx, 'Land']
    max_inflation_year_col = continent_data.loc[max_inflation_idx, inflation_columns].idxmax()
    max_inflation_year = max_inflation_year_col.split('_')[1]  # Assuming the column name format is 'Inflation_YYYY'

    # Extract the country and year for min inflation
    min_inflation_country = continent_data.loc[min_inflation_idx, 'Land']
    min_inflation_year_col = continent_data.loc[min_inflation_idx, inflation_columns].idxmin()
    min_inflation_year = min_inflation_year_col.split('_')[1]  # Assuming the column name format is 'Inflation_YYYY'

    # Create a new DataFrame row for the current continent's aggregated data
    new_row = pd.DataFrame([{
        'Continent': continent,
        'Average_Inflation': mean_inflation,
        'Max_Inflation': max_inflation,
        'Max_Inflation_Country': max_inflation_country,
        'Max_Inflation_Year': max_inflation_year,
        'Min_Inflation': min_inflation,
        'Min_Inflation_Country': min_inflation_country,
        'Min_Inflation_Year': min_inflation_year
    }])

    # Append the new row to the aggregated_data DataFrame
    aggregated_data = pd.concat([aggregated_data, new_row], ignore_index=True)

# Print the final aggregated data
print(aggregated_data)
