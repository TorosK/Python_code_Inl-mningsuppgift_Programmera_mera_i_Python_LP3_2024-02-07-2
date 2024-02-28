# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# Skapa DataFrame-objekten df_cpi, df_regions och df_inflation som innehåller en kopia av innehållet i csv-filerna cpi.csv, regions.csv och inflation.csv. Innehållet i dessa DataFrame-objekt ska du sedan använda för att lösa nedanstående uppgifter.------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# I've imported pandas as pd because I need to work with DataFrames, which are a key feature of pandas.
# DataFrames allow me to easily read, manipulate, and analyze structured data, such as the contents of csv files.
import pandas as pd

# Explanation: The code below reads CSV files into pandas DataFrames. Each DataFrame represents a different set of data: Consumer Price Index (CPI), regional information, and inflation rates, respectively. These DataFrames will be utilized to perform data analysis and visualization tasks.

# Load Consumer Price Index (CPI) data from a CSV file into a DataFrame.
# This DataFrame will be used to analyze changes in consumer prices over time across different countries.
df_CPI = pd.read_csv(r'C:\Users\TorosKutlu\Desktop\Borås Programmera mera i Python\Inlämningsuppgift_Programmera_mera_i_Python_LP3_2024-02-07-2\cpi.csv', delimiter=';', encoding='ISO-8859-1')

# Load regional information from a CSV file into a DataFrame.
# This DataFrame enriches the CPI data with geographical context, enabling regional analysis.
df_Regions = pd.read_csv(r'C:\Users\TorosKutlu\Desktop\Borås Programmera mera i Python\Inlämningsuppgift_Programmera_mera_i_Python_LP3_2024-02-07-2\regions.csv', delimiter=';', encoding='ISO-8859-1')

# Load inflation rate data from a CSV file into a DataFrame.
# This DataFrame provides additional economic indicators that can be correlated with the CPI data for comprehensive analysis.
df_Inflation = pd.read_csv(r'C:\Users\TorosKutlu\Desktop\Borås Programmera mera i Python\Inlämningsuppgift_Programmera_mera_i_Python_LP3_2024-02-07-2\inflation.csv', encoding='utf-8')

# Merge the regional information into the CPI DataFrame using the country code as a key.
# This operation enriches the CPI data with 'Country' and 'Continent' columns, allowing for more detailed regional analysis.
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