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

# I've imported matplotlib.dates as mdates because I will be working with date data on my plots.
# This submodule provides a convenient way to format dates on the x-axis of my plots, which is essential
# for clear and effective time-series visualization.
import matplotlib.dates as mdates

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
# Uppgift 5
# Skapa ett program där man först väljer ett land (COUNTRY) och därefter ett av de möjliga alternativen kolumnerna 'SUBJECT', 'FREQUENCY' och 'MEASURE' och därefter plottar inflationen under åren 1956–2023 i en linjediagram. De fem (5) år under tidsperioden som hade minst-, respektive högst inflation ska visas i grafen som fyllda cirklar. Diagrammet ska skapas med modulen matplotlib.
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# Enhance df_Inflation by adding a 'COUNTRY' column. This is achieved by leveraging df_Regions
# to map country codes ('Landskod') to their corresponding country names. This step enriches the
# inflation data with readable country names, making the dataset more user-friendly and interpretable.
df_Inflation_With_Country_From_Regions = pd.merge(df_Inflation, df_Regions.rename(columns={'Land': 'COUNTRY'}),
                                                  left_on='LOCATION', right_on='Landskod', how='left')

# Consolidate the enhanced dataframe by including all original columns from df_Inflation plus
# the newly added 'COUNTRY' column. This ensures the dataframe remains comprehensive with the
# addition of meaningful geographical context.
df_Inflation_With_Country_From_Regions = df_Inflation_With_Country_From_Regions[['COUNTRY'] + list(df_Inflation.columns)]

# Display the first few rows of the updated dataframe as a sanity check to ensure the merge
# and column addition were performed correctly, confirming the data's integrity.
print("printing df_Inflation_With_Country_From_Regions.head()", '\n')
print(df_Inflation_With_Country_From_Regions.head(), '\n')

def plot_inflation(df):
    # Prompt user input for detailed analysis parameters. This interactive approach allows users
    # to tailor the inflation analysis to specific countries, subjects, frequencies, and measures,
    # making the function versatile and adaptable to various analytical needs.
    country = input("Ange vilket land som ska analyseras: ").strip()
    subject = input("Ange vilken subject du vill analysera: ").strip()
    frequency = input("Ange vilken frequency du vill analysera: ").strip()
    measure = input("Ange vilken measure du vill analysera: ").strip()

    # Filter the dataframe based on user inputs to isolate the data relevant to the user's
    # specified criteria. This step ensures that the analysis and resulting plot are focused
    # and pertinent to the user's inquiry.
    filtered_df = df[(df['COUNTRY'].str.upper() == country.upper()) &
                     (df['SUBJECT'].str.upper() == subject.upper()) &
                     (df['FREQUENCY'].str.upper() == frequency.upper()) &
                     (df['MEASURE'].str.upper() == measure.upper())]

    # In case the filtered dataframe is empty, notify the user, indicating that there are no
    # records matching their specified criteria. This feedback loop enhances user experience
    # by providing immediate and clear communication regarding data availability.
    if filtered_df.empty:
        print("Inga data tillgängliga med angivna parametrar.")
        return

    # To avoid potential warnings and ensure data integrity when modifying the dataframe,
    # create an explicit copy of the filtered dataframe before any alterations.
    filtered_df = filtered_df.copy()

    # Convert the 'TIME' column to datetime format to facilitate time-series plotting. This
    # step is crucial for accurate temporal representation and analysis in the resulting plot.
    filtered_df['TIME'] = pd.to_datetime(filtered_df['TIME'], format='%Y')

    # Set up the plot with appropriate dimensions and plot the inflation trend over time.
    # This visual representation allows for an intuitive understanding of inflation dynamics
    # within the specified parameters.
    plt.figure(figsize=(12, 6))
    plt.plot(filtered_df['TIME'], filtered_df['Value'], marker='', linestyle='-', color='blue')

    # Identify and highlight the top 5 minimum and maximum inflation values within the filtered
    # dataset. This emphasis on extreme values provides additional insights into significant
    # inflation fluctuations over the selected period.
    min_values = filtered_df.nsmallest(5, 'Value')
    max_values = filtered_df.nlargest(5, 'Value')

    # Annotate the plot with markers and labels for minimum inflation values, offering a clear
    # visual cue to the user regarding periods of lowest inflation, enhancing interpretability.
    for _, row in min_values.iterrows():
        plt.plot(row['TIME'], row['Value'], marker='o', color='red', markersize=8)
        plt.text(row['TIME'], row['Value'], f"{row['TIME'].year} (min)", fontsize=9, ha='right')

    # Similarly, annotate the plot with markers and labels for maximum inflation values to
    # underscore periods of highest inflation, providing a comprehensive view of inflation trends.
    for _, row in max_values.iterrows():
        plt.plot(row['TIME'], row['Value'], marker='o', color='green', markersize=8)
        plt.text(row['TIME'], row['Value'], f"{row['TIME'].year} (max)", fontsize=9, ha='right')

    # Finalize the plot with titles, axis labels, and a custom legend, crafting a fully
    # informative and visually appealing graphical representation of the inflation analysis.
    plt.title(f'Inflation för {country} ({subject}, {frequency}, {measure})')
    plt.xlabel('År')
    plt.ylabel('Inflation (%)')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.xticks(rotation=45)  # Improve readability of the x-axis labels by rotating them.
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Minsta Inflation'),
                       plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=8, label='Högsta Inflation')]
    plt.legend(handles=legend_elements, loc='upper left')
    plt.grid(True)  # Enhance plot readability by adding a grid.
    plt.tight_layout()  # Adjust the layout to ensure everything fits without overlapping.
    plt.show()  # Display the final plot, offering a comprehensive visual analysis of inflation trends.

# execute
plot_inflation(df_Inflation_With_Country_From_Regions)