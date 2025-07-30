#data_mapping.py

#mappings for conditions to ICD-10 codes
#source: https://www.icd10data.com/
conditions_map = {
    "Type 2 Diabetes": {"icd_10_code": "E11.9"},
    "Hypertension": {"icd_10_code": "I10"},
    "Hyperlipidemia": {"icd_10_code": "E78.5"},
    "Obesity": {"icd_10_code": "E66.9"}
}

#mappings for medications to RxNorm codes, with common dosages/frequencies
#source: https://mor.nlm.nih.gov/RxNav/
medications_map = {
    "Metaformin": {"rx_norm_code": "860975", "dosage": "500 mg", "frequency": "twice daily"},
    "Lisinopril": {"rx_norm_code": "314076", "dosage": "10 mg", "frequency": "once daily"},
    "Atorvastatin": {"rx_norm_code": "860364", "dosage": "20 mg", "frequency": "once daily"},
    "Lifestyle Therapy": {"rx_norm_code": "N/A", "dosage": "N/A", "frequency": "ongoing"}
}


#mappings for lab test to LOINC codes
#source: https://loinc.org/
labs_map = {
    "hba1c": {"test_name": "Hemoglobin A1c", "loinc_code": "4548-4", "units": "%"},
    "bmi": {"test_name": "Body Mass Index", "loinc_code": "39156-5", "units": "kg/m^2"}
}