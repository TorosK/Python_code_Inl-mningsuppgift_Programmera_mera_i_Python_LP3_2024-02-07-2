# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# Skapa DataFrame-objekten df_cpi, df_regions och df_inflation som innehåller en kopia av innehållet i csv-filerna cpi.csv, regions.csv och inflation.csv. Innehållet i dessa DataFrame-objekt ska du sedan använda för att lösa nedanstående uppgifter.------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# I've imported pandas as pd because I need to work with DataFrames, which are a key feature of pandas.
# DataFrames allow me to easily read, manipulate, and analyze structured data, such as the contents of csv files.
import pandas as pd

# Load Consumer Price Index (CPI) data from a CSV file into a DataFrame.
df_CPI = pd.read_csv('cpi.csv', delimiter=';', encoding='ISO-8859-1')

# Load regional information from a CSV file into a DataFrame.
df_Regions = pd.read_csv('regions.csv', delimiter=';', encoding='ISO-8859-1')

# Load inflation rate data from a CSV file into a DataFrame.
df_Inflation = pd.read_csv('inflation.csv', encoding='utf-8')

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
# Uppgift 4
# I denna uppgift ska du analysera inflationen som har uppmätts per kontinent under tidsperioden 1960-2022 enligt den uppdelning som finns i kolumnen Kontinent i df_region. Skriv ett program som använder informationen i df_cpi och df_region och som skapar en tabell som dels presenterar medelinflationen per kontinent under tidsperioden 1960-2022 samt de 3 högsta- och de 3 lägsta förekommande inflationerna per kontinent under tidsperioden och i vilka länder dessa inflationer uppmättes...------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# Transforming the DataFrame to a long format to facilitate detailed inflation analysis by year and continent.
df_melted = df_CPI_merged_with_Regions.melt(id_vars=['Land', 'Landskod', 'Kontinent'], var_name='Year', value_name='Inflation')

# Calculating average inflation per continent.
continent_mean_inflation = df_melted.groupby('Kontinent')['Inflation'].mean().reset_index()
continent_mean_inflation.rename(columns={'Inflation': 'average_inflation'}, inplace=True)

# Defining a function to extract significant inflation values, enabling analysis on extreme inflation incidents.
def top_bottom_inflation(df, n=3):
    top = df.nlargest(n, 'Inflation')[['Land', 'Year', 'Inflation']]
    bottom = df.nsmallest(n, 'Inflation')[['Land', 'Year', 'Inflation']]
    return top, bottom  # Returns distinct DataFrames for highest and lowest inflations.

# Iterating over continents to identify inflation extremes.
extremes_list_top = []
extremes_list_bottom = []
for name, group in df_melted.groupby('Kontinent'):
    top, bottom = top_bottom_inflation(group)
    top['Kontinent'] = name  # Associating continent names with respective extreme values.
    bottom['Kontinent'] = name
    extremes_list_top.append(top)
    extremes_list_bottom.append(bottom)

# Aggregating identified inflation extremes into cohesive DataFrames.
inflation_extremes_top = pd.concat(extremes_list_top).reset_index(drop=True)
inflation_extremes_bottom = pd.concat(extremes_list_bottom).reset_index(drop=True)

# Custom function to neatly display inflation data.
def print_inflation_data(continent_means, inflation_extremes_top, inflation_extremes_bottom):
    header = "O L I K A   K O N T I N E N T E R S   I N F L A T I O N   U N D E R   T I D S P E R I O D E N   1 9 6 0 -- 2 0 2 2"
    print("=" * len(header))
    print(header)
    print("-" * len(header))
    print("{:<40} {:<15} {:<10} {:<15} {:<10} {:<20}".format("", "Högst", "", "Lägst", "", "Medel 1960-2022"))
    print("{:<40} {:<15} {:<10} {:<15} {:<10} {:<20}".format("Kontinent/Land", "Inf [%]", "År", "Inf [%]", "År", "Inf [%]"))
    print("-" * len(header))
    
    # Loop through each continent to display its average, highest, and lowest inflation values.
    for continent, group in continent_means.iterrows():
        print("{:<40} {:<15} {:<10} {:<15} {:<10} {:<20}".format(
            group['Kontinent'], "", "", "", "", "{:.1f}".format(group['average_inflation'])
        ))
        
        # Displaying top inflation values to highlight extremes.
        continent_data_top = inflation_extremes_top[inflation_extremes_top['Kontinent'] == group['Kontinent']]
        continent_data_bottom = inflation_extremes_bottom[inflation_extremes_bottom['Kontinent'] == group['Kontinent']]
        
        for _, row in continent_data_top.iterrows():
            print("    {:<36} {:<15} {:<10} {:<15} {:<10} {:<20}".format(
                row['Land'], "{:.1f}".format(row['Inflation']), row['Year'], "", "", ""
            ))
        
        # Displaying bottom inflation values to identify periods of highest deflation.
        for _, row in continent_data_bottom.iterrows():
            print("    {:<36} {:<15} {:<10} {:<15} {:<10} {:<20}".format(
                row['Land'], "", "", "{:.1f}".format(row['Inflation']), row['Year'], ""
            ))
        
        # Separating data for different continents.
        print("-" * len(header))

# Executing the function.
print_inflation_data(continent_mean_inflation, inflation_extremes_top, inflation_extremes_bottom)