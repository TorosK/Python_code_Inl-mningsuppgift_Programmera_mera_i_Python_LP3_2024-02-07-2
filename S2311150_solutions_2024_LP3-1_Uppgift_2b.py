# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# Skapa DataFrame-objekten df_cpi, df_regions och df_inflation som innehåller en kopia av innehållet i csv-filerna cpi.csv, regions.csv och inflation.csv. Innehållet i dessa DataFrame-objekt ska du sedan använda för att lösa nedanstående uppgifter.------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# I've imported pandas as pd because I need its powerful data manipulation capabilities to work with DataFrames.
# These DataFrames help me manage the data from the csv files I'm dealing with, such as 'cpi.csv', 'regions.csv',
# and 'inflation.csv'. Using pandas, I can easily read, clean, and transform this data for my analysis.
import pandas as pd

# I've imported matplotlib.pyplot as plt because it's essential for my data visualization tasks.
# With matplotlib, I can create various types of plots, including the bar chart needed for this assignment.
# It's a versatile library that allows me to customize plots to effectively communicate the data insights.
import matplotlib.pyplot as plt

# I've imported matplotlib.ticker as ticker because I need more control over the ticks on the axes of my plots,
# particularly for the x-axis in the bar chart of inflation change factors. The ticker module provides classes
# and functions to customize tick locations and formats, enabling me to make the plot's x-axis more readable
# by setting a specific interval for the ticks, which is crucial for displaying each year distinctly.
import matplotlib.ticker as ticker

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
# Uppgift 2 b
# Skriv ett program där man först anger landet som ska analyseras. Beräkna därefter förändringen av inflationen från ett år till ett annat under tidsperioden 1960-2022. Använd formeln för förändringsfaktorn FF(år) enligt formeln: 
    # 𝐹𝐹(å𝑟)=((𝑖𝑛𝑓𝑙𝑎𝑡𝑖𝑜𝑛(å𝑟)−𝑖𝑛𝑓𝑙𝑎𝑡𝑖𝑜𝑛(å𝑟−1))/(𝑖𝑛𝑓𝑙𝑎𝑡𝑖𝑜𝑛(å𝑟−1)))*100. 
# Plotta förändringsfaktorerna i ett stapeldiagram...
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# This function calculates the annual inflation change factors for a given country.
def calculate_change_factors(df, country):
    # Filter the data for the specified country, focusing on columns representing years.
    country_data = df[df['Land'] == country].iloc[:, 3:]  # Columns from the fourth onward represent years.

    change_factors = []  # Initialize a list to store calculated change factors.

    # Loop through the years 1961-2022. The first year for calculating a change factor is 1961
    # as it requires the previous year's data for comparison.
    for year in range(1961, 2023):
        # Ensure the current and previous year's data are not missing before calculation.
        if pd.notna(country_data[str(year)]).all() and pd.notna(country_data[str(year - 1)]).all():
            # Retrieve inflation rates for the current and previous years.
            inflation_current = country_data[str(year)].values[0]
            inflation_previous = country_data[str(year - 1)].values[0]

            # Calculate the change factor only if the previous year's inflation rate is non-zero to avoid division by zero.
            if inflation_previous != 0:
                change_factor = ((inflation_current - inflation_previous) / inflation_previous)
                change_factors.append(change_factor)  # Append the calculated change factor to the list.
            else:
                change_factors.append(None)  # Append None if the previous year's inflation rate is zero.
        else:
            change_factors.append(None)  # Append None if data for the current or previous year is missing.
            
    return change_factors  # Return the list of change factors.

# This function plots the annual change factors for the specified country.
def plot_change_factors(change_factors, country):
    years = list(range(1961, 2023))  # Define the range of years for the x-axis.
    plt.figure(figsize=(10, 5))  # Set the figure size to ensure clarity and readability.

    # Create a bar plot of change factors over the years, using blue color for bars.
    plt.bar(years, change_factors, color='blue')
    plt.xlabel('Year')  # Label for the x-axis.
    plt.ylabel('Change Factor (%)')  # Label for the y-axis.
    plt.title(f'{country} - Change in inflation compared to the previous year (1960-2022)')  # Plot title with the country's name.

    plt.grid(True)  # Enable grid lines for better readability of the plot.

    # Customize the x-axis to show a tick for every year for detailed analysis.
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))  # Ensures a tick is displayed for every year.
    plt.xticks(rotation=90, ha='center')  # Rotate the x-axis labels vertically for better readability.

    plt.tight_layout()  # Adjust the layout to make sure everything fits without overlapping.
    plt.show()  # Display the plot.

# Main function to initiate the analysis.
def main():
    country = input('Enter the name of the country to analyze: ')  # Prompt user to enter a country name.
    change_factors = calculate_change_factors(df_CPI_merged_with_Regions, country)  # Calculate change factors for the entered country.
    plot_change_factors(change_factors, country)  # Plot the calculated change factors.

# Entry point of the program.
if __name__ == '__main__':
    main()  # Execute the main function.