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
    """
    Analyzes and displays countries with the highest and lowest inflation rates for a given year.
    Excludes countries without reported inflation data for the year.
    Presents results in both tabular and graphical (bar chart) formats.
    """
    # Request year input from the user for analysis.
    year = input("Enter the year to analyze: ").strip()
    
    # Verify the presence of the requested year in the data; if absent, notify the user and exit the function.
    if year not in df.columns:
        print(f"Data for the year {year} is not available.")
        return
    
    # Create a DataFrame copy to ensure modifications do not affect the original data.
    df_year = df.copy()

    # Remove entries without reported inflation data for the selected year to ensure accurate analysis.
    df_year.dropna(subset=[year], inplace=True)
    
    # Convert inflation data to numeric, ensuring calculations can be performed; non-convertible data is set to NaN.
    df_year.loc[:, year] = pd.to_numeric(df_year[year], errors='coerce')
    
    # Remove any entries that could not be converted to numeric, ensuring the remaining dataset is clean.
    df_year.dropna(subset=[year], inplace=True)
    
    # Sort the cleaned dataset by inflation rate to easily identify the highest and lowest values.
    df_sorted = df_year.sort_values(by=year)
    
    # Extract the six countries with the lowest and highest inflation rates for detailed analysis.
    lowest_inflation = df_sorted.head(6)
    highest_inflation = df_sorted.tail(6)
    
    # Combine the two subsets for a consolidated view, facilitating comparison in a single visualization.
    combined_inflation = pd.concat([lowest_inflation, highest_inflation])
    
    # Visualize the selected data as a bar chart, providing a clear graphical representation of the extremes.
    plt.figure(figsize=(10, 5))
    plt.bar(combined_inflation['Land'], combined_inflation[year], color='blue')
    plt.xlabel('Country')
    plt.ylabel('Change [%]')
    plt.title(f'The lowest and highest inflation rates measured in {year}')
    plt.xticks(rotation=45, ha='right')  # Improve label readability.
    plt.tight_layout()  # Ensure the plot is neatly arranged without label cut-offs.
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Enhance plot readability with a grid.
    plt.show()
    
    # Present the analysis results in a table format, offering a clear, concise textual representation.
    print("\nCOUNTRIES WITH THE HIGHEST AND LOWEST INFLATION")
    print(f"Year {year}\n")
    print("Lowest:")  # Display the countries with the lowest inflation rates.
    print(lowest_inflation[['Land', year]].to_string(index=False))
    print("\nHighest:")  # Display the countries with the highest inflation rates.
    print(highest_inflation[['Land', year]].to_string(index=False))

analyze_inflation(df_CPI_merged_with_Regions)