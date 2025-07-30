#generator.py

import random 
#import json
#from pathlib import Path
from datetime import datetime, timedelta

#import custom/personal files
from data_mapping import conditions_map, medications_map, labs_map
from eligibility_criteria import check_eligibility
#define helper functions for lab values and conditions


#helper generation functions

def  generate_demographics():   
     return {
          "age": random.randint(40, 70),
          "sex": random.choice(["Male", "Female"]),
          "ethnicity": random.choice(["White", "Black", "Hispanic", "Asian", "Other"])
     }

def generate_raw_labs():
    return {
         "hba1c": round(random.uniform(5.0, 9.5), 1),
         "bmi": round(random.uniform(24.0, 40.0), 1)
    }

def generate_base_conditions():
     base_conditions = ["Type 2 Diabetes"]
     optional_conditions = ["Hypertension", "Hyperlipidemia", "Obesity"]
     #ensures some patients might not have the required condition
     if random.random() < 0.1:  #10% chance not having T2D
          base_conditions = []
     
     num_optional = random.randint(0, len(optional_conditions))
     return base_conditions + random.sample(optional_conditions, num_optional)

def generate_base_medications(conditions):
     meds = []
     if "Type 2 Diabetes" in conditions:
          meds.append("Metformin")
     if "Hypertension" in conditions:
          meds.append("Lisinopril")
     if "Hyperlipidemia" in conditions:
          meds.append("Atorvastatin")
     if "Obesity" in conditions:
          meds.append("Lifestyle Therapy")
     return meds

def generate_date(base_year):
     """generate a random date within the last few years"""
     start_date = datetime(base_year - random.randint(1, 5), 1, 1)
     end_date = datetime(base_year, 1, 1)
     random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
     return random_date.strftime("%Y-%m-%d")

#main generation function

def generate_patient_record(patient_id):
     """generates a single, detailed patient record conforming to target schema"""
     
     #generate base attributes
     demographics = generate_demographics()
     raw_labs = generate_raw_labs()
     base_conditions = generate_base_conditions()
     base_meds = generate_base_medications(base_conditions)

     #create temporary profile for eligibility check
     temp_profile = {
          **demographics,
          **raw_labs,
          "conditions" : base_conditions,
          "medications": base_meds
     }

     #check eligibility
     is_eligible, reasons = check_eligibility(temp_profile)

     #build final structured record
     patient_record = {
          "patient_id": patient_id,
          "age": demographics["age"],
          "sex": demographics["sex"],
          "ethnicity": demographics["ethnicity"],
          "trial_eligible": is_eligible,
          "ineligibility_reasons": reasons,
          "conditions": [],
          "medications": [],
          "lab_results": []
     }

     #make detailed conditions
     for cond_name in base_conditions:
          if cond_name in conditions_map:
               patient_record["conditions"].append({
                    "condition_name": cond_name,
                    "icd_10_code": conditions_map[cond_name]["icd_10_code"],
                    "date_of_diagnosis": generate_date(datetime.now().year - demographics["age"] + 30) #approx diagnosis date
               })
     
     #make detailed medications
     for med_name in base_meds:
          if med_name in medications_map:
               med_info = medications_map[med_name]
               patient_record["medications"].append({
                    "medication_name" : med_name,
                    "rx_norm_code": med_info["rx_norm_code"],
                    "dosage": med_info["dosage"],
                    "frequency": med_info["frequency"]
               })

     #make detailed lab results
     for lab_key, lab_value in raw_labs.items():
          if lab_key in labs_map:
               lab_info = labs_map[lab_key]
               patient_record["lab_results"].append({
                    "test_name": lab_info["test_name"],
                    "loinc_code": lab_info["loinc_code"],
                    "values": lab_value,
                    "units": lab_info["units"]
               })
     return patient_record