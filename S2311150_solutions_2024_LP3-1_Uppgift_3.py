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
# Uppgift 3
# Skriv ett program där man först anger årtalet som ska analyseras och därefter beräknar programmet de 6 länder som hade lägst respektive högst inflation för året ifråga. Informationen ska presenteras i tabellform och i ett stapeldiagram... Vi bortser från de länder som inte rapporterat inflationen för året i fråga.------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

def analyze_inflation(df):
    # Prompt the user for the year
    year = input("Enter the year to analyze: ").strip()
    
    # Check if the year is in the DataFrame
    if year not in df.columns:
        print(f"Data for the year {year} is not available.")
        return
    
    # Create a copy of the DataFrame to avoid SettingWithCopyWarning
    df_year = df.copy()

    # Drop rows with missing values for the specified year
    df_year.dropna(subset=[year], inplace=True)
    
    # Convert the year column to numeric values, using .loc to avoid SettingWithCopyWarning
    df_year.loc[:, year] = pd.to_numeric(df_year[year], errors='coerce')
    
    # Drop rows that could not be converted to numeric values
    df_year.dropna(subset=[year], inplace=True)
    
    # Sort the DataFrame by the specified year's inflation rate
    df_sorted = df_year.sort_values(by=year)
    
    # Get the six countries with the lowest and highest inflation rates
    lowest_inflation = df_sorted.head(6)
    highest_inflation = df_sorted.tail(6)
    
    # Create a combined DataFrame for easy plotting
    combined_inflation = pd.concat([lowest_inflation, highest_inflation])
    
    # Plotting the bar chart with English labels
    plt.figure(figsize=(10, 5))
    plt.bar(combined_inflation['Land'], combined_inflation[year], color='blue')
    plt.xlabel('Country')
    plt.ylabel('Change [%]')
    plt.title(f'The lowest and highest inflation rates measured in {year}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()
    
    # Displaying the table with English descriptions
    print("\nCOUNTRIES WITH THE HIGHEST AND LOWEST INFLATION")
    print(f"Year {year}\n")
    print("Lowest:")
    print(lowest_inflation[['Land', year]].to_string(index=False))
    print("\nHighest:")
    print(highest_inflation[['Land', year]].to_string(index=False))

analyze_inflation(df_CPI_merged_with_Regions)