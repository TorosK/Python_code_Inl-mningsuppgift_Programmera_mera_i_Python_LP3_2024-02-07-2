# C:\Users\TorosKutlu\Desktop\Borås Programmera mera i Python\Inlämningsuppgift_Programmera_mera_i_Python_LP3_2024-02-07-2\Python_code_Inlämningsuppgift_Programmera_mera_i_Python_LP3_2024-02-07-2\S2311150_solutions_2024_LP3-1.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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
# Uppgift 2 b
# Skriv ett program där man först anger landet som ska analyseras. Beräkna därefter förändringen av inflationen från ett år till ett annat under tidsperioden 1960-2022. Använd formeln för förändringsfaktorn FF(år) enligt formeln: 
    # 𝐹𝐹(å𝑟)=((𝑖𝑛𝑓𝑙𝑎𝑡𝑖𝑜𝑛(å𝑟)−𝑖𝑛𝑓𝑙𝑎𝑡𝑖𝑜𝑛(å𝑟−1))/(𝑖𝑛𝑓𝑙𝑎𝑡𝑖𝑜𝑛(å𝑟−1)))*100. 
# Plotta förändringsfaktorerna i ett stapeldiagram...
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# Function to calculate the change factor for inflation
def calculate_change_factors(df, country):
    # Filter the DataFrame for the selected country
    country_data = df[df['Land'] == country].iloc[:, 3:]  # Exclude non-year columns
    change_factors = []
    
    # Calculate the change factor for each year
    for year in range(1961, 2023):  # Start from 1961 as we need the previous year's data
        if pd.notna(country_data[str(year)]).all() and pd.notna(country_data[str(year - 1)]).all():
            inflation_current = country_data[str(year)].values[0]
            inflation_previous = country_data[str(year - 1)].values[0]
            if inflation_previous != 0:
                change_factor = ((inflation_current - inflation_previous) / inflation_previous)
                change_factors.append(change_factor)
            else:
                change_factors.append(None)
        else:
            change_factors.append(None)
            
    return change_factors

# Function to plot the change factors with every year displayed
def plot_change_factors(change_factors, country):
    years = list(range(1961, 2023))
    plt.figure(figsize=(10, 5))  # Set a larger figure size to accommodate all years
    plt.bar(years, change_factors, color='blue')
    plt.xlabel('Year')
    plt.ylabel('Change Factor (%)')
    plt.title(f'{country} - Change in inflation compared to the previous year (1960-2022)')
    plt.grid(True)  # This will enable both horizontal and vertical grid lines

    # Set x-axis major tick on each year
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))  # Set a tick for every year
    plt.xticks(rotation=90, ha='center')  # Rotate the x ticks vertically

    plt.tight_layout()  # Adjusts plot to ensure everything fits without overlapping
    plt.show()

# Main function to run the program
def main():
    country = input('Enter the name of the country to analyze: ')
    change_factors = calculate_change_factors(df_CPI_merged_with_Regions, country)
    plot_change_factors(change_factors, country)

# Run the program
if __name__ == '__main__':
    main()