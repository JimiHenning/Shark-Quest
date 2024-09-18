import pandas as pd
import numpy as np
import re

#### Setup ####
url = ("C:/Users/Utilizador/Desktop/IRONHACK/Project 2/Shark-Quest/GSAF5.xls")
shark_attacks = pd.read_excel(url)

print("Original shape: ", shark_attacks.shape)

pd.set_option('display.max_rows', 8000)
pd.set_option('display.max_columns', 19)
pd.set_option('display.max_colwidth', 20)

shark_attacks.columns = [col.strip().replace(" ", "_").replace(".", "").lower() for col in shark_attacks.columns]
#print(shark_attacks.columns)

#### Linh's functions

def strip_func(df):
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df

df_cleaned = strip_func(shark_attacks)

df_cleaned['location'] = df_cleaned['location'].astype(str)

def clean_data(location):
    location = re.sub(r'\d{1,2}º[NS],\s*\d{1,3}º[EW]', '', location)
    location = re.sub(r'\(.*?\)', '', location)
    location = re.sub(r'\s+', ' ', location)
    return location.title()

shark_attacks['location'] = df_cleaned['location'].apply(clean_data)

#### Henning's Function

def categorize_activity(activity):

    if pd.isna(activity):
        return "Invalid"
    

    activity = activity.lower()
    
def merge_values(row, arg1, *args):
    if row in args:
        return arg1
    else:
        return row
    
shark_attacks['type'] = shark_attacks['type'].apply(merge_values, args=("Invalid", "Questionable", "Unconfirmed", "?", 'Unverified', 'Under investigation'))
shark_attacks['type'] = shark_attacks['type'].apply(merge_values, args=("Provoked", " Provoked"))
shark_attacks['type'] = shark_attacks['type'].apply(merge_values, args=("Watercraft", "Boat"))

shark_attacks['activity'] = df_cleaned['activity'].apply(categorize_activity)


#### JP's Functions

# replacements
replacements_test_species = [
    (r'^.*([Tt]iger).*$', 'TIGER SHARK'),
]

replacements_test_dates = [
    (r'^(.*)(\d{2})(.*)(\w{3})(.*)(\d{4})(.*)', r'\2-\4-\6'),
    (r'^(.*)(\w{3})(.*)(\d{4})(.*)', r'01-\2-\4'),
    (r'-(uly|une)', r'-J\1'),
]

replacements_test_time = [
    (r'^.*((0[0-2]|23)h|([nN]ight|[dD]ark)).*$', 'NIGHT'),
    (r'^.*((0[3-6])h|([dD]awn|[sS]unrise|[dD]aybreak)).*$', 'DAWN'),
    (r'^.*((0[7-9]|10)h.*$|([mM]orning|^[aA]\.?[mM])).*$', 'MORNING'),
    (r'^.*((1[1-4])h.*$|([nN]oon|[mM]idday|[lL]unch)).*$', 'NOON'),
    (r'^.*((1[5-8])h.*$|([aA]fternoon|^[pP]\.?[mM])).*$', 'AFTERNOON'),
    (r'^.*((19|2[0-2])h.*$|([dD]usk|[sS]unset|[eE]vening)).*$', 'DUSK'),
]

def replace_string_patterns(value, replacements):

    if isinstance(value, str):

        for pattern, target in replacements:
            value = re.sub(pattern, target, value)
        return value
    
    else:
        
        return value

species_replace = shark_attacks['species'].apply(replace_string_patterns, replacements = replacements_test_species)
#print(species_replace)

#DATE TEST
date_replace_test = shark_attacks['date'].apply(replace_string_patterns, replacements = replacements_test_dates)
date_test = pd.to_datetime(date_replace_test, errors='coerce') #format-mixed can give errors, omitted

formatted_dates = date_test.dt.strftime('%d-%m-%Y')
shark_attacks["date"] = formatted_dates.astype('datetime64[ns]')

#TIME TEST
#print(shark_attacks['time'].value_counts())
time_replace_test = shark_attacks['time'].apply(replace_string_patterns, replacements = replacements_test_time,)
#print(time_replace_test.value_counts())
shark_attacks["time"]=time_replace_test

#### Ricardo's Functon

def repnan(series, keys, value=np.nan):
    # takes a list of values, replace with value OR <NaN> if no value is provided
    series.replace(keys, value, inplace=True)

# Converts country to lowercase    
shark_attacks["country"] = shark_attacks["country"].apply(lambda x: x.lower() if isinstance(x,str) else x)

# introduces country sheet. Converts into a list  ### Convert into dictionary, pass it through repnan or JP's
country_list = pd.read_csv("C:/Users/Utilizador/Desktop/IRONHACK/Project 2/countries.csv")
country_list = country_list["English Name"]
country_list = [x.lower() for x in country_list]
repnan(shark_attacks["country"], ["england","scotland"], "united kingdom")
repnan(shark_attacks["country"], ["usa", "hawaii"], "united states of america")
repnan(shark_attacks["country"], ["reunion"], "france")
repnan(shark_attacks["country"], ["columbia"], "colombia")
repnan(shark_attacks["country"], ["new guinea"], "papua new guinea")

# unify country, converts all low value "country" ocorrences into <NA>. Also sets Country as string-type
shark_attacks["country"] = shark_attacks["country"].where(shark_attacks["country"].isin(country_list)).astype("string")

#### Column cleaner ####

# Drop useless columns
shark_attacks.drop("original_order", axis=1, inplace=True)
shark_attacks.drop("unnamed:_21", axis=1, inplace=True)
shark_attacks.drop("unnamed:_22", axis=1, inplace=True)
shark_attacks.drop("unnamed:_11", axis=1, inplace=True)

####  Simple dupe cleaner  ####

# Filters all relevant columns for empty data:
business_relevant_columns = ['date','type','country','state','location','activity','injury','time']
all_nan_rows = shark_attacks[shark_attacks[business_relevant_columns].isna().all(axis=1)].index

# Drops all empty rows   
shark_attacks.drop(all_nan_rows, axis=0, inplace=True)

#Filter for rows with lots ( > 3) NaN's
filtered = shark_attacks[shark_attacks[['date', 'type', 'country', 'activity', 'injury', 'time']].isna().sum(axis=1) > 3]
shark_attacks.drop(filtered.index, axis=0, inplace=True)

print("Simple cleaner shape: ", shark_attacks.shape)

#### Fuzzy Dupe cleaner ####

#print(shark_attacks[['date', 'type', 'country', 'activity', 'time']][1:100])
a= shark_attacks[shark_attacks[['date', 'type', 'country', 'activity', 'injury', 'time', "href"]].duplicated(keep=False)]
print(a)

