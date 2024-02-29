# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# Skapa DataFrame-objekten df_cpi, df_regions och df_inflation som innehåller en kopia av innehållet i csv-filerna cpi.csv, regions.csv och inflation.csv. Innehållet i dessa DataFrame-objekt ska du sedan använda för att lösa nedanstående uppgifter.------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# I've imported pandas as pd because I need to work with DataFrames, which are a key feature of pandas.
# DataFrames allow me to easily read, manipulate, and analyze structured data, such as the contents of csv files.
import pandas as pd

# I've imported matplotlib.pyplot as plt because I need to create and customize visualizations,
# specifically line plots for this task. Matplotlib is a comprehensive library for creating static,
# animated, and interactive visualizations in Python.
import matplotlib.pyplot as plt

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
    # Before modifying the inflation values, I use .copy() to explicitly create a copy of the DataFrame slices.
    # This ensures that the original DataFrame is not affected by the modifications made to these slices.
    lowest_inflation = df_sorted.head(6).copy()
    # Use .copy() and sort highest_inflation in ascending order to ensure it's displayed from lowest to highest.
    highest_inflation = df_sorted.tail(6).copy().sort_values(by=year, ascending=True)

    # Now that lowest_inflation and highest_inflation are explicitly copied,
    # I can safely round the inflation values to one decimal place without triggering a warning.
    lowest_inflation.loc[:, year] = lowest_inflation[year].round(1)
    highest_inflation.loc[:, year] = highest_inflation[year].round(1)

    # Plotting
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
    # Formatting and printing the table
    # Print a line of equal signs.
    print("="*85)

    # Print the title of the table, centered between two sets of tab characters.
    print("\t\tCOUNTRIES WITH THE HIGHEST AND LOWEST INFLATION")

    # Print the year being analyzed, formatted within the title
    print(f"\t\t\t\tYEAR {year}")

    # Print a line of dashes
    print("-"*85)

    # The use of tab characters and spaces ensures that the headers are aligned with the corresponding data columns.
    print("\tLowest\t\t\t\t\t\t\tHighest")

    # Print sub-headers for each category ('Lowest' and 'Highest'), with 'Country' and 'inflation [%]' as column titles.
    print("\t------\t\t\t\t\t\t\t-------")
    print("Country\t\tinflation [%]\t\tCountry\t\t\t\tinflation[%]")

    # Iterate over the rows of the 'lowest_inflation' and 'highest_inflation' DataFrames simultaneously using zip().
    # 'iterrows()' is used to iterate through DataFrame rows as (index, Series) pairs, providing access to each row's data.
    for low, high in zip(lowest_inflation.iterrows(), highest_inflation.iterrows()):
        # For each pair of rows, print the country name and inflation rate, formatted to align with the table headers.
        # The '<' character in the format specification aligns the text to the left, ensuring a tidy columnar display.
        # Numbers within the curly braces denote the minimum field width, providing consistent spacing between columns.
        print(f"{low[1]['Land']:<15}{low[1][year]:<25}{high[1]['Land']:<32}{high[1][year]:<15}")

# Execute
analyze_inflation(df_CPI_merged_with_Regions)