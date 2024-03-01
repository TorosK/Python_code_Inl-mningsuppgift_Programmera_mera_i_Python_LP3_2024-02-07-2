# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# Skapa DataFrame-objekten df_cpi, df_regions och df_inflation som innehåller en kopia av innehållet i csv-filerna cpi.csv, regions.csv och inflation.csv. Innehållet i dessa DataFrame-objekt ska du sedan använda för att lösa nedanstående uppgifter.------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# I've imported pandas as pd because I need to work with DataFrames, which are a key feature of pandas.
# DataFrames allow me to read, manipulate, and analyze structured data, such as the contents of csv files.
import pandas as pd

# I've imported matplotlib.pyplot as plt because I need to create and customize visualizations,
# specifically line plots for this task. Matplotlib is a library for creating interactive visualizations in Python.
import matplotlib.pyplot as plt

# I've imported matplotlib.dates as mdates because I will be working with date data on my plots.
# This submodule provides a way to format dates on the x-axis of my plots.
import matplotlib.dates as mdates

# Import necessary for custom legend entries
import matplotlib.lines as mlines

# Import for accessing a set of predefined colors
import matplotlib.colors as mcolors  

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
# Uppgift 5
# Skapa ett program där man först väljer ett land (COUNTRY) och därefter ett av de möjliga alternativen kolumnerna 'SUBJECT', 'FREQUENCY' och 'MEASURE' och därefter plottar inflationen under åren 1956–2023 i en linjediagram. De fem (5) år under tidsperioden som hade minst-, respektive högst inflation ska visas i grafen som fyllda cirklar. Diagrammet ska skapas med modulen matplotlib.
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# Enhance df_Inflation by adding a 'COUNTRY' column. This is achieved by leveraging df_Regions
# to map country codes ('Landskod') to their corresponding country names.
df_Inflation_With_Country_From_Regions = pd.merge(df_Inflation, df_Regions.rename(columns={'Land': 'COUNTRY'}),
                                                  left_on='LOCATION', right_on='Landskod', how='left')

# Consolidate the enhanced dataframe by including all original columns from df_Inflation plus
# the newly added 'COUNTRY' column, for geographical context.
df_Inflation_With_Country_From_Regions = df_Inflation_With_Country_From_Regions[['COUNTRY'] + list(df_Inflation.columns)]

# Display the first few rows of the updated dataframe as a check to ensure the merge
# and column addition were performed correctly.
print("printing df_Inflation_With_Country_From_Regions.head()", '\n')
print(df_Inflation_With_Country_From_Regions.head(), '\n')

def plot_inflation(df):
    # Request user input for country, subject, frequency, and measure to specify the scope of the analysis.
    country = input("Ange vilket land som ska analyseras: ").strip()
    subject = input("Ange vilken subject du vill analysera: ").strip()
    frequency = input("Ange vilken frequency du vill analysera: ").strip()
    measure = input("Ange vilken measure du vill analysera: ").strip()

    # Filter the DataFrame based on user input to isolate data relevant to the specified analysis parameters: user's chosen country, subject, frequency, and measure.
    filtered_df = df[(df['COUNTRY'].str.upper() == country.upper()) &
                     (df['SUBJECT'].str.upper() == subject.upper()) &
                     (df['FREQUENCY'].str.upper() == frequency.upper()) &
                     (df['MEASURE'].str.upper() == measure.upper())]

    # Check if the filtered DataFrame is empty, indicating no data matches the user's criteria.
    # If so, inform the user and exit the function to prevent plotting an empty chart.
    if filtered_df.empty:
        print("Inga data tillgängliga med angivna parametrar.")
        return

    filtered_df = filtered_df.copy()

    # Convert the 'TIME' column to datetime format to enable proper time-series plotting.
    filtered_df['TIME'] = pd.to_datetime(filtered_df['TIME'], format='%Y')

    # Initialize the plot with a specified figure size and plot the inflation data as a line chart.
    plt.figure(figsize=(12, 6))
    plt.plot(filtered_df['TIME'], filtered_df['Value'], marker='', linestyle='-', color='blue')

    # Identify the five years with the lowest and highest inflation rates in the filtered dataset.
    min_values = filtered_df.nsmallest(5, 'Value')
    max_values = filtered_df.nlargest(5, 'Value')

    # Define a list of unique colors, using a predefined palette from matplotlib
    unique_colors = list(mcolors.TABLEAU_COLORS.values())

    # Initialize an empty list to store custom legend entries
    legend_elements = []

    # Iterate over the minimum and maximum values, assigning a unique color to each and adding a marker
    # to the chart. This loop also creates custom legend entries for each highlighted year, indicating
    # whether it represents a minimum or maximum inflation rate.
    for i, (_, row) in enumerate(min_values.iterrows()):
        color = unique_colors[i % len(unique_colors)]  # Use modulo to cycle through colors if there are more points than colors
        plt.plot(row['TIME'], row['Value'], marker='o', color=color, markersize=8)
        plt.text(row['TIME'], row['Value'], f"{row['TIME'].year} (min)", fontsize=9, ha='right')
        legend_elements.append(mlines.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=8, label=f"{row['TIME'].year} (min)"))

    # Loop over maximum values and assign unique colors, continuing from where the min values left off
    for j, (_, row) in enumerate(max_values.iterrows(), start=i + 1):
        color = unique_colors[j % len(unique_colors)]
        plt.plot(row['TIME'], row['Value'], marker='o', color=color, markersize=8)
        plt.text(row['TIME'], row['Value'], f"{row['TIME'].year} (max)", fontsize=9, ha='right')
        legend_elements.append(mlines.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=8, label=f"{row['TIME'].year} (max)"))

    # Finalize the chart by setting the title, axis labels, and legend, and by applying formatting.
    plt.title(f'Inflation för {country} ({subject}, {frequency}, {measure})')
    plt.xlabel('År')
    plt.ylabel('Inflation (%)')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.xticks(rotation=90)
    plt.legend(handles=legend_elements, loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Execute the function based on user-defined parameters.
plot_inflation(df_Inflation_With_Country_From_Regions)