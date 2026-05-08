import pandas as pd

# 1. Load the raw dataset
# Drop any completely blank rows at the end of the file to ensure clean data
df = pd.read_csv('Project2_dataset.csv')
df = df.dropna(subset=['Departure Airport Name', 'Arrival Airport Name'])

# ---------------------------------------------------------
# STEP 1: Extract Airport Nodes
# ---------------------------------------------------------
# We extract both departure and arrival airports, rename columns to match 
# our intended Neo4j properties, combine them, and drop duplicates.

dep_airports = df[['Departure Airport Name', 'Departure Airport City', 'Departure Airport Country/Region']].rename(columns={
    'Departure Airport Name': 'name',
    'Departure Airport City': 'city',
    'Departure Airport Country/Region': 'country'
})

arr_airports = df[['Arrival Airport Name', 'Arrival Airport City', 'Arrival Airport Country/Region']].rename(columns={
    'Arrival Airport Name': 'name',
    'Arrival Airport City': 'city',
    'Arrival Airport Country/Region': 'country'
})

airports_df = pd.concat([dep_airports, arr_airports]).drop_duplicates(subset=['name', 'city', 'country']).dropna(subset=['name'])

airport_duplicate_name = airports_df[airports_df.duplicated(subset=['name'], keep=False)].sort_values(by='name')

#print every row in airport_duplicate_name
for index, row in airport_duplicate_name.iterrows():
    print(row)

print(airport_duplicate_name.shape)

    # 1. Define the correct countries for the problematic airports
# (You can adjust these mappings based on your specific project requirements)
corrections = {
    'Alberto Carnevalli Airport': 'Venezuela',
    'Charles M. Schulz Sonoma County Airport': 'United States',
    'Cheddi Jagan International Airport': 'Guyana',
    'Cibao International Airport': 'Dominican Republic',
    'Comodoro Arturo Merino Benitez International Airport': 'Chile', 
    'Eugene F. Correira International Airport': 'Guyana',
    'El Alto International Airport': 'Bolivia',
    'F. D. Roosevelt Airport': 'Netherlands Antilles',
    'Futuna Airport': 'Vanuatu',
    'General Jose Antonio Anzoategui International Airport': 'Venezuela',
    'JAGS McCartney International Airport': 'Turks and Caicos Islands',
    'London City Airport': 'United Kingdom',
    'London Gatwick Airport': 'United Kingdom',
    'London Heathrow Airport': 'United Kingdom',
    'London Luton Airport': 'United Kingdom',
    'London Stansted Airport': 'United Kingdom',
    'Luis Munoz Marin International Airport': 'Puerto Rico',
    'Mayor Buenaventura Vivas International Airport': 'Venezuela',
    'Norman Manley International Airport': 'Jamaica',
    'Norman Y. Mineta San Jose International Airport': 'United States',
    'Northwest Florida Beaches International Airport': 'United States',
    'Presidente Joao Batista Figueiredo Airport': 'Brazil',
    'St Petersburg Clearwater International Airport': 'United States',
    'St Pierre Airport': 'Saint Pierre and Miquelon',    
    'Sydney Kingsford Smith International Airport': 'Australia',
    
    'Albany Airport': 'Australia', 
    'Alexandria International Airport': 'United States',
    'Atlas Brasil Cantanhede Airport': 'Brazil',
    'Arturo Michelena International Airport': 'Venezuela',
    'Birmingham-Shuttlesworth International Airport': 'United States',
    'Cochin International Airport': 'India',
    'Florence Regional Airport': 'United States',
    'Fort Smith Regional Airport': 'United States',
    'Richmond Airport': 'United States',
    'San Jose Airport': 'Costa Rica',
    'Santa Ana Airport': 'United States',
    'Santa Fe Municipal Airport': 'United States',
    'Santa Rosa International Airport': 'Argentina',
    'Tri-Cities Regional TN/VA Airport': 'United States',
    'Victoria Regional Airport': 'Canada',
    'Waterloo Regional Airport': 'Canada'
}

# 2. Loop through the dictionary and overwrite the country for both Departure and Arrival
for airport, correct_country in corrections.items():
    
    # Fix Departure Airports
    df.loc[
        df['Departure Airport Name'].str.startswith(airport, na=False), 
        'Departure Airport Country/Region'
    ] = correct_country
    
    # Fix Arrival Airports
    df.loc[
        df['Arrival Airport Name'].str.startswith(airport, na=False), 
        'Arrival Airport Country/Region'
    ] = correct_country

print("Geographical errors successfully corrected!")