from pydantic import BaseModel, field_validator
from datetime import date
import json

with open("Neighbourhood_158.json") as f:
    raw_158 = json.load(f)
    Neighbourhood_158 = set(name.replace("–", "-").replace("—", "-") for name in raw_158)

alias_corrections = {
    "Wexford/Maryvale (119)": "Wexford-Maryvale (119)",
    "St.Andrew-Windfields (40)": "St. Andrew-Windfields (40)",
    "Cabbagetown-South St.James Town (71)": "Cabbagetown-South St. James Town (71)",
    "Yonge-St.Clair (97)": "Yonge-St. Clair (97)",
    "Oakdale-Beverley Heights (154)": "Oakdale–Beverly Heights (154)",  

}
with open("Primary_Offence.json") as f:
    Primary_Offence = set(json.load(f))

with open("Division.json") as f:
    Division = set(json.load(f))

with open("Location_type.json") as f:
    Location_type = set(json.load(f))

class HateCrimes(BaseModel):
    occurrence_date: date #must be of the form yyyy-mm-dd
    reported_date: date #must be of the form yyyy-mm-dd
    division: str #must be a string
    location_type: str #must be a string
    primary_offence: str #must be a string
    neighbourhood: str #must be a string
    arrest: str # Must be yes or no

    @field_validator("division")
    def reject_na_division(cls,v):
        not_allowed = {"NA"}
        if v in not_allowed:
            raise ValueError(f'"{v}" is not an allowed value for divison')
        return v
    @field_validator("division")
    def included_division(cls,v):
        if v not in Division:
            raise ValueError(f'"{v}" is not one of the allowed values for division')
        return v
    @field_validator("location_type")
    def reject_na_location_type(cls,v):
        not_allowed = {"NA"}
        if v in not_allowed:
            raise ValueError(f'"{v}" is not an allowed value for location_type')
        return v
    @field_validator("location_type")
    def included_location(cls,v):
        if v not in Location_type:
            raise ValueError(f'"{v}" is not one of the allowed values for location_type')
        return v
    @field_validator("primary_offence")
    def reject_na_primary_offence(cls,v):
        not_allowed = {"NA", "This should be removed"}
        if v in not_allowed:
            raise ValueError(f'"{v}" is not an allowed value for primary_offence')
        return v
    @field_validator("primary_offence")
    def included_division(cls,v):
        if v not in Primary_Offence:
            raise ValueError(f'"{v}" is not one of the allowed values for primary_offence')
        return v
    @field_validator("neighbourhood")
    def reject_na_neighbourhood(cls,v):
        not_allowed = {"NSA"}
        if v in not_allowed:
            raise ValueError(f'"{v}" is not an allowed value for neighbourhood')
        return v
    @field_validator("neighbourhood")
    def included_neighbourhood(cls,v):
        v = alias_corrections.get(v, v) 
        v_clean = (
            v.replace("–", "-")
            .replace("—", "-")
            .replace("/", "-")
            .replace("St.", "St. ") 
            .replace("  ", " ")      
            .strip()
        )
        if v not in Neighbourhood_158:
            raise ValueError(f'"{v}" is not one of the allowed values for neighbourhoods')
    
