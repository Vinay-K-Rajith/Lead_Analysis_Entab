import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define number of rows
n_rows = 1000

# Generate random data for each column
data = {
    'location_score': np.random.randint(40, 100, n_rows),
    'how_you_know_us_score': np.random.randint(50, 90, n_rows),
    'sibling_in_school_score': np.random.choice([0, 50, 100], n_rows, p=[0.4, 0.3, 0.3]),
    'previous_school_name_score': np.random.randint(60, 95, n_rows),
    'class_applied_for_score': np.random.randint(65, 90, n_rows),
    'last_class_percentage_score': np.random.randint(60, 100, n_rows),
    'communication_email_different_score': np.random.choice([0, 25, 50, 75, 100], n_rows, p=[0.3, 0.2, 0.2, 0.2, 0.1]),
    'whatsapp_number_different_score': np.random.choice([0, 25, 50, 75, 100], n_rows, p=[0.3, 0.2, 0.2, 0.2, 0.1])
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('lead_scoring_sample_1000.csv', index=False)

print("Generated CSV file 'lead_scoring_sample_1000.csv' with 1000 rows.")
