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

# Initialize an empty DataFrame to hold all inflation data
inflation_data = pd.DataFrame()

# Calculate inflation rates and store them in the inflation_data DataFrame
for year in range(1961, 2023):  # Start from 1961 since we need the previous year's data to calculate inflation
    prev_year = str(year - 1)
    current_year = str(year)
    inflation_column = f'Inflation_{current_year}'
    inflation_data[inflation_column] = ((df_CPI_merged_with_Regions[current_year].astype(float) - df_CPI_merged_with_Regions[prev_year].astype(float)) / df_CPI_merged_with_Regions[prev_year].astype(float)) * 100

# Join the inflation data with the main DataFrame
df_CPI_merged_with_Regions = df_CPI_merged_with_Regions.join(inflation_data)

# Initialize a DataFrame to hold aggregated data
columns = ['Continent', 'Average_Inflation', 'Max_Inflation_Value', 'Max_Inflation_Country', 'Max_Inflation_Year', 'Min_Inflation_Value', 'Min_Inflation_Country', 'Min_Inflation_Year']
aggregated_data = pd.DataFrame(columns=columns)

# Iterate over each continent
for continent in df_CPI_merged_with_Regions['Kontinent'].unique():
    continent_data = df_CPI_merged_with_Regions[df_CPI_merged_with_Regions['Kontinent'] == continent]

    # Calculate the mean inflation for the continent
    mean_inflation = continent_data[inflation_data.columns].mean().mean()

    # Initialize variables to hold the max and min inflation details
    max_inflation_value = -float('inf')
    min_inflation_value = float('inf')
    max_inflation_country = None
    max_inflation_year = None
    min_inflation_country = None
    min_inflation_year = None

    # For each inflation column, find the max and min values along with their corresponding country and year
    for column in inflation_data.columns:
        max_value = continent_data[column].max()
        min_value = continent_data[column].min()
        if max_value > max_inflation_value:
            max_inflation_value = max_value
            max_inflation_country = continent_data[continent_data[column] == max_value]['Land'].iloc[0]
            max_inflation_year = column.split('_')[1]
        if min_value < min_inflation_value:
            min_inflation_value = min_value
            min_inflation_country = continent_data[continent_data[column] == min_value]['Land'].iloc[0]
            min_inflation_year = column.split('_')[1]

    # Prepare a new DataFrame for the row and use pd.concat to add it to the aggregated_data DataFrame
    new_row_df = pd.DataFrame([{
        'Continent': continent,
        'Average_Inflation': mean_inflation,
        'Max_Inflation_Value': max_inflation_value,
        'Max_Inflation_Country': max_inflation_country,
        'Max_Inflation_Year': max_inflation_year,
        'Min_Inflation_Value': min_inflation_value,
        'Min_Inflation_Country': min_inflation_country,
        'Min_Inflation_Year': min_inflation_year
    }])

    aggregated_data = pd.concat([aggregated_data, new_row_df], ignore_index=True)

# Display the final aggregated data
print(aggregated_data)

def get_top_bottom_inflation(continent_data, inflation_columns):
    valid_columns = [col for col in inflation_columns if col in continent_data.columns]
    
    if len(continent_data) == 0 or len(valid_columns) == 0:
        return pd.DataFrame(), pd.DataFrame()  # Return empty DataFrames if no valid data

    data_to_analyze = continent_data[['Land'] + valid_columns].dropna(subset=valid_columns, how='all')

    if data_to_analyze.empty:
        return pd.DataFrame(), pd.DataFrame()  # Return empty DataFrames if filtered data is empty

    # Ensure there's at least one row after filtering to avoid IndexError
    if len(data_to_analyze) > 0:
        top_3 = data_to_analyze.nlargest(3, valid_columns, keep='all')
        bottom_3 = data_to_analyze.nsmallest(3, valid_columns, keep='all')
    else:
        top_3 = pd.DataFrame()
        bottom_3 = pd.DataFrame()

    return top_3, bottom_3

# Then, when you call this function, ensure to handle the case where the returned DataFrames are empty:
for continent in df_CPI_merged_with_Regions['Kontinent'].unique():
    continent_data = df_CPI_merged_with_Regions[df_CPI_merged_with_Regions['Kontinent'] == continent]
    top_3, bottom_3 = get_top_bottom_inflation(continent_data, inflation_data.columns.tolist())

    if not top_3.empty and not bottom_3.empty:
        # Process top_3 and bottom_3
        pass
    else:
        # Handle the case where there's no data (e.g., by skipping this continent or noting the lack of data)
        pass