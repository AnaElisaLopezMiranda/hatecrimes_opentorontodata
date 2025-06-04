#### Preamble ####
# Purpose: Simulates a dataset of hate crimes
# Author: Ana Elisa Lopez-Miranda
# Date: 22 May 2025
# Contact: a.lopez.miranda@mail.utoronto.ca
# License: MIT
# Pre-requisites:
# - Add `polars`: uv add polars
# - Add `numpy`: uv add numpy
# - Add `datetime`: uv add datetime



#### Workspace setup ####
import polars as pl
import numpy as np
from datetime import date, timedelta
import json

with open("Neighbourhood_158.json") as f:
    Neighbourhood_158 = json.load(f)

with open("Primary_Offence.json") as f:
    Primary_Offence = json.load(f)

with open("Division.json") as f:
    Division = json.load(f)

with open("Location_type.json") as f:
    Location_type = json.load(f)

rng_occurrence = np.random.default_rng(seed=853)
rng_reported = np.random.default_rng(seed=123)


#### Simulate data ####
# Simulate 20 offences with occurence data, occurence time, reported date, division, location_type, bias, primary offence, neighbourhood, and arrest
bias_choice = ["AGE_BIAS", "MENTAL_OR_PHYSICAL_DISABILITY", "RACE_BIAS", "ETHNICITY_BIAS", "LANGUAGE_BIAS", "RELIGION_BIAS", "SEXUAL_ORIENTATION_BIAS", "GENDER_BIAS"]
bias = np.random.choice(bias_choice, size=20, replace=True)
arrest_choice = ["Yes", "No"]
arrest = np.random.choice(arrest_choice, size=20, replace=True)
division = np.random.choice(Division, size = 20, replace = True)
location_type = np.random.choice(Location_type, size=20, replace=True)
neighbourhood_158 = np.random.choice(Neighbourhood_158, size=20, replace = True)
primary_offence = np.random.choice(Primary_Offence, size=20, replace=True)
start_date = date(2018, 1,1)
end_date = date(2024, 12, 31)
range_date=(end_date-start_date).days
random_days_o = rng_occurrence.integers(0, range_date+1, size=20)
random_dates_o = [start_date +timedelta(days=int(d)) for d in random_days_o]
date_o = [d.isoformat() for d in random_dates_o]
random_days_r = rng_reported.integers(0, range_date+1, size=20)
random_dates_r = [start_date +timedelta(days=int(d)) for d in random_days_r]
date_r = [d.isoformat() for d in random_dates_r]
hate_crimes_df = pl.DataFrame(
    {
        "occurrence_date": date_o,
        "reported_date": date_r,
        "division": division,
        "location_type": location_type,
        "bias" :bias,
        "primary_offence": primary_offence,
        "neighbourhood": neighbourhood_158,
        "arrest": arrest
    }
)

hate_crimes_df.write_csv("simulated_data.csv")


