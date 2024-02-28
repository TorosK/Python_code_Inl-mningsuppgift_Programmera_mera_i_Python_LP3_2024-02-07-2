# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# Skapa DataFrame-objekten df_cpi, df_regions och df_inflation som innehåller en kopia av innehållet i csv-filerna cpi.csv, regions.csv och inflation.csv. Innehållet i dessa DataFrame-objekt ska du sedan använda för att lösa nedanstående uppgifter.------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# I've imported pandas as pd because I need to work with DataFrames, which are a key feature of pandas.
# DataFrames allow me to easily read, manipulate, and analyze structured data, such as the contents of csv files.
import pandas as pd

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
# Uppgift 4
# I denna uppgift ska du analysera inflationen som har uppmätts per kontinent under tidsperioden 1960-2022 enligt den uppdelning som finns i kolumnen Kontinent i df_region. Skriv ett program som använder informationen i df_cpi och df_region och som skapar en tabell som dels presenterar medelinflationen per kontinent under tidsperioden 1960-2022 samt de 3 högsta- och de 3 lägsta förekommande inflationerna per kontinent under tidsperioden och i vilka länder dessa inflationer uppmättes...------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# Aggregate inflation data per continent over the period 1960-2022.
# This involves transforming the DataFrame from wide to long format to facilitate group-wise operations.
df_melted = df_CPI_merged_with_Regions.melt(id_vars=['Land', 'Landskod', 'Kontinent'], var_name='Year', value_name='Inflation')

# Calculate the average inflation for each continent across the entire period.
# This provides a high-level overview of inflation trends on a continental basis.
continent_mean_inflation = df_melted.groupby('Kontinent')['Inflation'].mean().reset_index()
continent_mean_inflation.rename(columns={'Inflation': 'average_yearly_inflation_for_period_1960_2022'}, inplace=True)

# Define a function to identify the extremes in inflation data.
# This function helps in pinpointing the highest and lowest inflation instances, which are critical for economic analysis.
def top_bottom_inflation(df, n=3):
    top = df.nlargest(n, 'Inflation')[['Land', 'Year', 'Inflation']]
    bottom = df.nsmallest(n, 'Inflation')[['Land', 'Year', 'Inflation']]
    return pd.concat([top, bottom])

# Collect extreme inflation values for each continent.
# This loop iterates over each continent, applying the top_bottom_inflation function to extract significant data points.
extremes_list = []

for name, group in df_melted.groupby('Kontinent', group_keys=False):
    grouped_extremes = top_bottom_inflation(group)
    grouped_extremes['Kontinent'] = name  # Associate the continent name with its corresponding extremes for clarity.
    extremes_list.append(grouped_extremes)

# Combine all extreme inflation data into a single DataFrame for analysis and presentation.
inflation_extremes = pd.concat(extremes_list).reset_index(drop=True)

# Display the calculated average inflation and the extremes.
# These print statements serve to present the aggregated data in a readable format to the user.
print('printing: continent_mean_inflation\n')
print(continent_mean_inflation, '\n')
print('printing: inflation_extremes\n')
print(inflation_extremes, '\n')

# Function to format and print the inflation data organized by continent.
# This function enhances the readability of the data by structuring it in a clear, tabular format.
def print_inflation_data(continent_means, inflation_extremes):
    # Print headers and formatting for average inflation data.
    print("="*81)
    print("Different Continents average inflation during the time period year 1960 to year 2022")
    print("-"*65)
    print("{:<20} {:<40}".format("Continent", "Average inflation 1960-2022:"))
    print("-"*65)
    
    # Iterate through the average inflation data, printing each continent's information.
    for index, row in continent_means.iterrows():
        print("{:<20} {:<40}".format(row['Kontinent'], row['average_yearly_inflation_for_period_1960_2022']))
        
        # Extract and print the highest and lowest inflations for the current continent.
        continent_extremes = inflation_extremes[inflation_extremes['Kontinent'] == row['Kontinent']]
        print("\nCountry\t\t\t Highest inflation (%)\t Year")
        print("-"*65)
        
        # Display the top 3 highest inflations for insight into peak inflation scenarios.
        for _, top_row in continent_extremes.nlargest(3, 'Inflation').iterrows():
            print("{:<20} {:<20} {:<15}".format(top_row['Land'], top_row['Inflation'], top_row['Year']))
        
        # Display the bottom 3 lowest inflations to highlight instances of minimal inflation or deflation.
        print("\nCountry\t\t\t Lowest inflation (%)\t Year")
        print("-"*65)
        
        for _, bottom_row in continent_extremes.nsmallest(3, 'Inflation').iterrows():
            print("{:<20} {:<20} {:<15}".format(bottom_row['Land'], bottom_row['Inflation'], bottom_row['Year']))
        
        # Separator for clarity between continents' data.
        print("\n" + "="*65 + "\n")

# Execute the function to display structured inflation data by continent.
print_inflation_data(continent_mean_inflation, inflation_extremes)