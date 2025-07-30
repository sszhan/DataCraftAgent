#gui.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from pathlib import Path


#import patient generator
import generator

def flatten_patient_for_csv(patient):
    """flattens a complicated patient record for CSV export"""
    base_info = {
        "patient_id": patient["patient_id"],
        "age": patient["age"],
        "sex": patient["sex"],
        "ethnicity": patient["ethnicity"],
        "trial_eligible": patient["trial_eligible"],
        "ineligibility_reasons": "; ".join(patient["ineligibility_reasons"]),
        "record_type": "", "name": "", "code": "", "details": ""
    }

    if not any([patient["conditions"], patient["medications"],
                patient["lab_results"]]):
        #if patient has no sub records, yield a single line for demographics
        yield base_info
        return
    
    for cond in patient["conditions"]:
        row = base_info.copy()
        row.update({
            "record_type": "Condition",
            "name": cond["condition_name"],
            "code": cond["icd_10_code"],
            "details": f"Diagnosed: {cond['date_of_diagnosis']}"
        })
        yield row

    for med in patient["medications"]:
        row = base_info.copy()
        row.update({
            "record_type": "Medication",
            "name": med["medication_name"],
            "code": med["rx_norm_code"],
            "details": f"{med['dosage']}, {med['frequency']}"
        })
        yield row

    for lab in patient["lab_results"]:
        row = base_info.copy()
        row.update({
            "record_type": "Lab Result",
            "name": lab["test_name"],
            "code": lab["loinc_code"],
            "details": f"Value: {lab['values']} {lab['units']}"
        })
        yield row

class GeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Synthetic Patient Data Generator")
        self.geometry("450x300")

        #UI elements
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.main_frame, text="Number of Patients to Generate:").grid(row=0, column=0, sticky="w", pady=5)
        self.num_patients_var = tk.StringVar(value="100")
        self.num_patients_entry = ttk.Entry(self.main_frame, textvariable=self.num_patients_var, width=10)
        self.num_patients_entry.grid(row=0, column=1, sticky="w", pady=5)
        ttk.Label(self.main_frame, text="Output Directory:").grid(row=1, column=0, sticky="w", pady=5)
        self.output_dir_var = tk.StringVar(value=str(Path("synthetic_data").resolve()))
        self.output_dir_entry = ttk.Entry(self.main_frame, textvariable=self.output_dir_var, width=40)
        self.output_dir_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=2)
        self.browse_button = ttk.Button(self.main_frame, text = "Browse...", command=self.browse_directory)
        self.browse_button.grid(row=2, column=2, padx=5)

        self.generate_button = ttk.Button(self.main_frame, text="Generate Data", command=self.run_generation)
        self.generate_button.grid(row=3, column=0, columnspan=3, pady=20)

        self.status_label = ttk.Label(self.main_frame, text="Ready")
        self.status_label.grid(row=4, column=0, columnspan=3, sticky="w")
        
    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
    def run_generation(self):
        try:
            num_patients = int(self.num_patients_var.get())
            output_dir = Path(self.output_dir_var.get())
            output_dir.mkdir(parents=True, exist_ok=True)
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid input. Please check number of patients and directory path")
            return
        
        self.status_label.config(text=f"Generating {num_patients}...")
        self.update_idletasks()

        patients_data = []
        for i in range(num_patients):
            pid = f"P{i:04d}"
            patient = generator.generate_patient_record(pid)
            patients_data.append(patient)

        #save to JSON
        json_path = output_dir / "patients_detailed.json"
        with open(json_path, "w") as f:
            json.dump(patients_data, f, indent=2)

        #save to CSV
        csv_path = output_dir / "patients_flattened.csv"
        csv_headers = [
            "patient_id", "age", "sex", "ethnicity", "trial_eligible", "ineligibility_reasons", "record_type", "name", "code", "details"
        ]
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            for patient in patients_data:
                for flat_row in flatten_patient_for_csv(patient):
                    writer.writerow(flat_row)
        
        self.status_label.config(text=f"Sucess! Saved data to {output_dir}")
        messagebox.showinfo("Success", f"Generated {num_patients} patient records.\n\nJSON: {json_path}\nCSV: {csv_path}")

if __name__ == "__main__":
    app = GeneratorApp()
    app.mainloop()
