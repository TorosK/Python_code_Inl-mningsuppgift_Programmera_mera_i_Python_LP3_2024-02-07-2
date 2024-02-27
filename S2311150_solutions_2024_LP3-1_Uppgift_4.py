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
print("printing df_Regions.head()", '\n')
print(df_Regions.head(), '\n')

print("printing df_Inflation.head()", '\n')
print(df_Inflation.head(), '\n')

print("printing df_CPI.head()", '\n')
print(df_CPI.head(), '\n')

# Display the first few rows of the merged DataFrame to verify it's correct
print("printing df_CPI_merged_with_Regions.head()", '\n')
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

# Define the function for finding top and bottom inflations
def top_bottom_inflation(df, n=3):
    top = df.nlargest(n, 'Inflation')[['Land', 'Year', 'Inflation']]
    bottom = df.nsmallest(n, 'Inflation')[['Land', 'Year', 'Inflation']]
    return pd.concat([top, bottom])

# Instead of using apply, you can use a for loop and collect the results in a list,
# which you then concatenate at the end
extremes_list = []

for name, group in df_melted.groupby('Kontinent', group_keys=False):
    grouped_extremes = top_bottom_inflation(group)
    grouped_extremes['Kontinent'] = name  # Add the continent name to the results
    extremes_list.append(grouped_extremes)

# Concatenate all the results into a single DataFrame
inflation_extremes = pd.concat(extremes_list).reset_index(drop=True)

# Display the result
print('printing: continent_mean_inflation\n')
print(continent_mean_inflation, '\n')
print('printing: inflation_extremes\n')
print(inflation_extremes, '\n')

''''''

# Function to print formatted inflation data by continent
def print_inflation_data(continent_means, inflation_extremes):
    # Print header for average inflation
    print("="*81)
    print("Different Continents average inflation during the time period year 1960 to year 2022")
    print("-"*65)
    print("{:<20} {:<40}".format("Continent", "Average inflation 1960-2022:"))
    print("-"*65)
    
    # Loop through each continent's average inflation and print
    for index, row in continent_means.iterrows():
        print("{:<20} {:<40}".format(row['Kontinent'], row['average_yearly_inflation_for_period_1960_2022']))
        
        # Filter the extremes for the current continent
        continent_extremes = inflation_extremes[inflation_extremes['Kontinent'] == row['Kontinent']]
        
        # Print header for highest and lowest inflation
        print("\nCountry\t\t\t Highest inflation (%)\t Year")
        print("-"*65)
        
        # Print the top 3 inflations
        for _, top_row in continent_extremes.nlargest(3, 'Inflation').iterrows():
            print("{:<20} {:<20} {:<15}".format(top_row['Land'], top_row['Inflation'], top_row['Year']))
        
        # Print header for lowest inflation
        print("\nCountry\t\t\t Lowest inflation (%)\t Year")
        print("-"*65)
        
        # Print the bottom 3 inflations
        for _, bottom_row in continent_extremes.nsmallest(3, 'Inflation').iterrows():
            print("{:<20} {:<20} {:<15}".format(bottom_row['Land'], bottom_row['Inflation'], bottom_row['Year']))
        
        # Print a separator for the next continent
        print("\n" + "="*65 + "\n")

# Call the function with the continent mean inflation and extremes dataframes
print_inflation_data(continent_mean_inflation, inflation_extremes)