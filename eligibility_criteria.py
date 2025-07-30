#eligibility_criteria.py

#define inclusion and exclusion criteria for the clinical trial
#this makes the logic clear and easy to modify

inclusion_criteria = {
    "min_age" : 40,
    "max_age": 65,
    "min_hba1c": 6.5,
    "required_condition": "Type 2 Diabetes"
}

exclusion_criteria = {
    "max_bmi": 40,
    "prohibited_medication": "Insulin"
}

def check_eligibility(patient_profile):
    """checks if a patient meets the trial eligibility criteria"""

    ineligibility_reasons = []

    #check inclusion criteria
    if not (inclusion_criteria["min_age"] <= patient_profile["age"] <=inclusion_criteria["max_age"]):
        ineligibility_reasons.append(f"Age {patient_profile["age"]} outside range [{inclusion_criteria["min_age"]}-{inclusion_criteria["max_age"]}]")

    if patient_profile["hba1c"] < inclusion_criteria["min_hba1c"]:
        ineligibility_reasons.append(f"Hba1c {patient_profile["hba1c"]}% is below minimum of {inclusion_criteria['min_hba1c']}%")
    
    if inclusion_criteria["required_condition"] not in patient_profile["conditions"]:
        ineligibility_reasons.append(f"Missing required condition: {inclusion_criteria['required_condition']}")

    if "max_bmi" in exclusion_criteria:
        if patient_profile["bmi"] > exclusion_criteria["max_bmi"]:
            ineligibility_reasons.append(f"BMI {patient_profile['bmi']} exceeds maximum of {exclusion_criteria['max_bmi']}")
    
    if "prohibited_medication" in exclusion_criteria:
        prohibited_med = exclusion_criteria["prohibited_medication"]
        if prohibited_med in patient_profile["medications"]:
            ineligibility_reasons.append(f"Patient is taking a prohibited medication: {prohibited_med}")
         

    is_eligible = len(ineligibility_reasons) == 0

    return is_eligible, ineligibility_reasons
