import pandas as pd #importing pandas to read data and manipulate it
import matplotlib.pyplot as plt #importing matplotlib for visualization
import seaborn as sns #importing seaborn for advanced visualization

df=pd.read_csv(r"apy.csv") #initializing a variable in which we can read the csv file

print("Checking if dataset is being read properly or not\n")
print(df.head()) #using head() function to see if the file is being read properly
print("\nInformation about dataset:\n")
print(df.info()) #using info() function to know what columns dataset is having
print("\nDescription about dataset:\n")
print(df.describe()) #using describe function to know mean,median,standard deviation,etc.. about the dataset

# Check for missing values
print("\nMissing values in each column:\n")
print(df.isnull().sum())

# Count rows before dropping
rows_before = df.shape[0]

# Drop rows with missing Production and copy
df_cleaned = df.dropna(subset=['Production']).copy()

# Count rows after dropping
rows_after = df_cleaned.shape[0]

# Display how many rows were dropped
print(f"\nRows before dropping NAs in 'Production': {rows_before}")
print(f"Rows after dropping NAs in 'Production' : {rows_after}")
print(f"Total rows dropped                      : {rows_before - rows_after}")

# Strip whitespace from string columns using .loc
for col in df_cleaned.select_dtypes(include='object'):
    df_cleaned.loc[:, col] = df_cleaned[col].str.strip()


# Unique values in each categorical column
print("\nUnique States:", df_cleaned['State_Name'].nunique())
print("Unique Districts:", df_cleaned['District_Name'].nunique())
print("Unique Crops:", df_cleaned['Crop'].nunique())
print("Unique Seasons:", df_cleaned['Season'].nunique())

# Production range by crop
print("\nTop 5 crops by total production:")
print(df_cleaned.groupby('Crop')['Production'].sum().sort_values(ascending=False).head())

# Objective 1: Most Productive Crops in Each State and District

# -------------------------------
# Objective: Top Crops by State
# -------------------------------
top_crop_by_state = (
    df_cleaned.groupby(['State_Name', 'Crop'])['Production']
    .sum()
    .reset_index()
    .sort_values(['State_Name', 'Production'], ascending=[True, False])
)
top_crop_by_state = top_crop_by_state.groupby('State_Name').first().reset_index()

# -------------------------------
# Objective: Top Crops by District
# -------------------------------
top_crop_by_district = (
    df_cleaned.groupby(['District_Name', 'Crop'])['Production']
    .sum()
    .reset_index()
    .sort_values(['District_Name', 'Production'], ascending=[True, False])
)
top_crop_by_district = top_crop_by_district.groupby('District_Name').first().reset_index()

# Set Seaborn theme for cleaner plots
sns.set_theme(style="whitegrid")

# ------------------------------------------------
# Custom Color Palettes for More Color Variation
# ------------------------------------------------
state_colors = sns.color_palette("tab20", n_colors=top_crop_by_state['Crop'].nunique())
district_colors = sns.color_palette("Paired", n_colors=top_crop_by_district['Crop'].nunique())

# -----------------------------------------------
# Visualization: Top 10 Crops by Production State
# -----------------------------------------------
top_crop_by_state_plot = top_crop_by_state.sort_values(by='Production', ascending=False).head(10)

plt.figure(figsize=(14, 7))
sns.barplot(
    data=top_crop_by_state_plot,
    x='Production',
    y='State_Name',
    hue='Crop',
    palette=state_colors,
    dodge=False
)
plt.title('🌾 Top 10 Crops by Production in States', fontsize=16, fontweight='bold')
plt.xlabel('Total Production', fontsize=12)
plt.ylabel('State', fontsize=12)
plt.legend(title='Crop', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# -------------------------------------------------
# Visualization: Top 10 Crops by Production District
# -------------------------------------------------
top_crop_by_district_plot = top_crop_by_district.sort_values(by='Production', ascending=False).head(10)

plt.figure(figsize=(14, 7))
sns.barplot(
    data=top_crop_by_district_plot,
    x='Production',
    y='District_Name',
    hue='Crop',
    palette=district_colors,
    dodge=False
)
plt.title('Top 10 Crops by Production in Districts', fontsize=16, fontweight='bold')
plt.xlabel('Total Production', fontsize=12)
plt.ylabel('District', fontsize=12)
plt.legend(title='Crop', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()