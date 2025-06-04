from utils import HateCrimes
from pydantic import BaseModel, Field, ValidationError, field_validator
from datetime import date

import polars as pl

df = pl.read_csv("cleaned_hate_crimes.csv")

# Convert Polars DataFrame to a list of dictionaries for validation
data_dicts = df.to_dicts()

# Validate the dataset in batches
validated_data = []
errors = []

# Batch validation
for i, row in enumerate(data_dicts):
    try:
        validated_row = HateCrimes(**row)  # Validate each row
        validated_data.append(validated_row)
    except ValidationError as e:
        errors.append((i, e))

# Convert validated data back to a Polars DataFrame
validated_df = pl.DataFrame([row.dict() for row in validated_data])

# Display results
print("Validated Rows:")
print(validated_df)

if errors:
    print("\nErrors:")
    for i, error in errors:
        print(f"Row {i}: {error}")