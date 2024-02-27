import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# Lägg till en 'COUNTRY' kolumn i df_Inflation genom att matcha landskoder med df_Regions
# Notera att vi döper om 'Land' till 'COUNTRY'
df_Inflation_With_Country_From_Regions = pd.merge(df_Inflation, df_Regions.rename(columns={'Land': 'COUNTRY'}), left_on='LOCATION', right_on='Landskod', how='left')

# Behåll alla kolumner från df_Inflation och lägg till 'COUNTRY'
df_Inflation_With_Country_From_Regions = df_Inflation_With_Country_From_Regions[['COUNTRY'] + list(df_Inflation.columns)]

# Visa de första raderna för att kontrollera att allt ser korrekt ut
print("printing df_Inflation_With_Country_From_Regions.head()", '\n')
print(df_Inflation_With_Country_From_Regions.head(), '\n')

''''''
def plot_inflation(df):
    country = input("Ange vilket land som ska analyseras: ").strip()
    subject = input("Ange vilken subject du vill analysera: ").strip()
    frequency = input("Ange vilken frequency du vill analysera: ").strip()
    measure = input("Ange vilken measure du vill analysera: ").strip()

    filtered_df = df[(df['COUNTRY'].str.upper() == country.upper()) &
                     (df['SUBJECT'].str.upper() == subject.upper()) &
                     (df['FREQUENCY'].str.upper() == frequency.upper()) &
                     (df['MEASURE'].str.upper() == measure.upper())]

    if filtered_df.empty:
        print("Inga data tillgängliga med angivna parametrar.")
        return

    filtered_df['TIME'] = pd.to_datetime(filtered_df['TIME'], format='%Y')

    plt.figure(figsize=(12, 6))
    plt.plot(filtered_df['TIME'], filtered_df['Value'], marker='o', linestyle='-', color='blue')

    min_values = filtered_df.nsmallest(5, 'Value')
    max_values = filtered_df.nlargest(5, 'Value')
    plt.scatter(min_values['TIME'], min_values['Value'], color='red', s=50, label='Minsta Inflation')
    plt.scatter(max_values['TIME'], max_values['Value'], color='green', s=50, label='Högsta Inflation')

    plt.title(f'Inflation för {country} ({subject}, {frequency}, {measure})')
    plt.xlabel('År')
    plt.ylabel('Inflation (%)')

    # Ange x-axeln för att visa varje år
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())

    plt.xticks(rotation=45)  # Roterar datumetiketterna för bättre läsbarhet
    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Justerar subplotparametrar för att ge angivet padding
    plt.show()

plot_inflation(df_Inflation_With_Country_From_Regions)