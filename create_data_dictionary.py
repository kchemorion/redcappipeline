import pandas as pd
import os
import re

def infer_redcap_field_type(series):
    """Infer REDCap field type from a pandas series."""
    if pd.api.types.is_integer_dtype(series):
        return 'text', 'integer', str(series.min()), str(series.max()) if not series.empty else ''
    elif pd.api.types.is_float_dtype(series):
        return 'text', 'number', '', ''
    elif pd.api.types.is_datetime_dtype(series):
        return 'date', 'date', '', ''
    elif pd.api.types.is_string_dtype(series):
        return 'text', '', '', ''
    return 'text', '', '', ''

def clean_name(name, seen_names, prefix):
    """Ensure names are valid for REDCap and unique, adding a prefix to handle special cases."""
    cleaned_name = re.sub(r'[^\w]', '_', name).lower()
    if cleaned_name[0].isdigit() or cleaned_name[0] == '_':
        cleaned_name = prefix + cleaned_name
    # Ensure uniqueness
    original_cleaned_name = cleaned_name
    count = 1
    while cleaned_name in seen_names:
        cleaned_name = f"{original_cleaned_name}_{count}"
        count += 1
    seen_names.add(cleaned_name)
    return cleaned_name

def adjust_csv_headers(csv_directory, seen_names):
    """Adjust CSV headers to conform to REDCap naming conventions."""
    for filename in os.listdir(csv_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(csv_directory, filename)
            df = pd.read_csv(file_path)
            new_columns = [clean_name(col, seen_names, 'hdr_') for col in df.columns]
            df.columns = new_columns
            df.to_csv(file_path, index=False)  # Overwrite the original file with cleaned headers

def generate_data_dictionary(csv_directory):
    """Generate a REDCap data dictionary from all CSV files in a directory."""
    data_dictionary = []
    seen_variables = set()
    seen_fields = set()

    adjust_csv_headers(csv_directory, seen_fields)  # Clean headers first

    for filename in os.listdir(csv_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(csv_directory, filename)
            if not os.access(file_path, os.R_OK):
                print(f"Warning: '{filename}' cannot be accessed. Skipping.")
                continue

            try:
                df = pd.read_csv(file_path)
                if df.empty:
                    print(f"Warning: '{filename}' is empty. Skipping.")
                    continue

                form_name = filename.replace('.csv', '').replace('_', ' ').capitalize()

                for column in df.columns:
                    variable_name = clean_name(column, seen_variables, 'var_')
                    field_name = clean_name(column, seen_fields, 'field_')

                    field_type, validation_type, val_min, val_max = infer_redcap_field_type(df[column])

                    data_dictionary.append({
                        'Variable / Field Name': variable_name,
                        'Form Name': form_name,
                        'Section Header': '',
                        'Field Type': field_type,
                        'Field Label': field_name,
                        'Choices, Calculations, OR Slider Labels': '',
                        'Field Note': '',
                        'Text Validation Type OR Show Slider Number': validation_type,
                        'Text Validation Min': val_min,
                        'Text Validation Max': val_max,
                        'Identifier?': '',
                        'Branching Logic (Show field only if)': '',
                        'Required Field?': 'y',
                        'Custom Alignment': '',
                        'Question Number (surveys only)': '',
                        'Matrix Group Name': '',
                        'Matrix Ranking?': '',
                        'Field Annotation': ''
                    })
            except pd.errors.EmptyDataError:
                print(f"Warning: No data to parse in '{filename}' - file may be empty or improperly formatted.")
            except Exception as e:
                print(f"Error reading '{filename}': {e}")

    return pd.DataFrame(data_dictionary)

# Example usage:
csv_directory = '.'
data_dict_df = generate_data_dictionary(csv_directory)
data_dict_df.to_csv('redcap_data_dictionary.csv', index=False)
print("Data dictionary saved to redcap_data_dictionary.csv")
