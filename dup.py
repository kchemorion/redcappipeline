import pandas as pd

# Assuming 'data_dict_df' is your DataFrame loaded from the 'redcap_data_dictionary.csv'
data_dict_df = pd.read_csv('redcap_data_dictionary.csv')

# Filter for field names that may have issues with trailing zeros
fields_with_zeros = data_dict_df['Variable / Field Name'].apply(lambda x: '0' in x.split('__')[-1] if '__' in x else '0' in x.split('_')[-1])

# Get unique field names that include a zero pattern
unique_fields_with_zeros = data_dict_df[fields_with_zeros]['Variable / Field Name'].unique()

# Print out the list of affected fields
for field in unique_fields_with_zeros:
    print(field)

# Create a mapping of field names without zeros to check for potential duplicates
mapped_names = {name: name.rstrip('0').rstrip('_') for name in unique_fields_with_zeros}

# Print potential duplicates by removing trailing zeros
potential_duplicates = set()
for original, mapped in mapped_names.items():
    if mapped in data_dict_df['Variable / Field Name'].values:
        potential_duplicates.add((original, mapped))

# Output potential duplicates
print("Potential Duplicates:")
for dup in potential_duplicates:
    print(dup)
