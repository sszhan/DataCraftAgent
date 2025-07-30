#analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

#Source: https://www.cdc.gov/diabetes/php/data-research/index-1.html
#Stats for US adults age 18+ with diagosed diabetes

real_world_benchmarks = {
    "sex": {
        "Male": 0.52,
        "Female": 0.48
    },
    "ethnicity": {
        "White": 0.61,
        "Black": 0.15,
        "Hispanic": 0.16,
        "Asian": 0.06,
        "Other": 0.02
    },
    "age": {
        "mean": 52.1,
        "std_dev": 14.6
    },
    "clinical": {
        "bmi": {
            "mean": 34.6,
        }
    }
}

def load_and_prepare_data(csv_path):
    """loads flattened CSV and prepares it for analysis"""

    if not csv_path.exists():
        print(f"Error: Data file not found at {csv_path}")
        print("Please run the generator GUI first to create 'patients_flattened.csv'")
        return None, None
    df = pd.read_csv(csv_path)

    #create dataframe for demographic analysis
    patient_df = df.drop_duplicates(subset='patient_id').copy()
    print(f"Loaded and prepared demographics for {len(patient_df)} unique patient records")

    #create dataframe for lab analysis
    lab_df = df[df['record_type'] == 'Lab Result'].copy()
    #extract numeric value from 'details' column
    lab_df['value'] = lab_df['details'].str.extract(r'Value: ([\d.]+)').astype(float)
    print(f"Loaded and prepared {len(lab_df)} lab records")

    return patient_df, lab_df

def plot_categorical_distribution(df, column, benchmarks, ax):
    """creates overlapping density plot for a categorical variable"""

    synthetic_dist = df[column].value_counts(normalize=True).rename('Percentage').reset_index()
    synthetic_dist['DataSource'] = 'Synthetic'

    benchmark_dist = pd.DataFrame(list(benchmarks.items()), columns = [column, 'Percentage'])
    benchmark_dist['DataSource'] = 'Benchmark'

    combined = pd.concat([synthetic_dist, benchmark_dist])

    sns.barplot(data=combined, x=column, y='Percentage', hue='DataSource', ax=ax)
    ax.set_title(f'Distribution of {column.title()}')
    ax.set_ylabel('Proportion')
    ax.tick_params(axis='x', rotation=30)

def plot_continuous_distribution(series, name, benchmarks, ax):
    """creates overlapping density plot for a continuous variable"""

    sns.kdeplot(series, ax=ax, fill=True, label='Synthetic', color='blue')
    ax.axvline(benchmarks['mean'], color='red', linestyle='--', label=f"Benchmark Mean ){benchmarks['mean']})")
    ax.set_title(f'Distribution of {name}')
    ax.set_xlabel(name)
    ax.legend()

def run_analysis():
    """main function to run analysis and plotting workflow"""

    data_dir = Path('synthetic_data')
    csv_file = data_dir / "patients_flattened.csv"
    patient_df, lab_df = load_and_prepare_data(csv_file)

    if patient_df is None:
        return  #stop if data wasn't loaded
    
    #create plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Synthetic Data vs Real-World Benchmarks (CDC/NHANES)', fontsize=18, y=0.98)

    #plot sex distributions
    plot_categorical_distribution(patient_df, 'sex', real_world_benchmarks['sex'], axes[0, 0])

    #plot ethnicity distributions
    plot_categorical_distribution(patient_df, 'ethnicity', real_world_benchmarks['ethnicity'], axes[0, 1])

    #plot age distribution
    plot_continuous_distribution(patient_df['age'], 'Age', real_world_benchmarks['age'], axes[1, 0])

    #plot bmi distribution
    bmi_series = lab_df[lab_df['name'] == 'Body Mass Index']['value']
    plot_continuous_distribution(bmi_series, 'BMI', real_world_benchmarks['clinical']['bmi'], axes[1, 1])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    output_plot_path = data_dir / "comparison_dashboard.png"
    plt.savefig(output_plot_path)
    print(f"\nSucess! Comparison dashboard saved to: {output_plot_path}")
    plt.show()


if __name__ == "__main__":
    run_analysis()

    