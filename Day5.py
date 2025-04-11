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

# Objective 2: Analyze crop yield trends over the years

# --------------------------------------
# Analyze Crop Yield Trends Over Years
# --------------------------------------

# Get top 5 crops by total production
top_crops = df_cleaned.groupby('Crop')['Production'].sum().nlargest(5).index

# Filter to only those crops
filtered = df_cleaned[df_cleaned['Crop'].isin(top_crops)]

# Group and normalize
crop_trends = filtered.groupby(['Crop_Year', 'Crop'])['Production'].sum().reset_index()
crop_trends['Normalized_Production'] = crop_trends.groupby('Crop')['Production'].transform(
    lambda x: (x - x.min()) / (x.max() - x.min())
)

# Plot
plt.figure(figsize=(14, 7))
sns.lineplot(
    data=crop_trends,
    x='Crop_Year',
    y='Normalized_Production',
    hue='Crop',
    marker='o',
    palette='tab10'
)
plt.title('Crop Production Trends (Top 5 Crops)', fontsize=16, fontweight='bold')
plt.xlabel('Year')
plt.ylabel('Production (0-1)')
plt.legend(title='Crop', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# --------------------------------------------
# Objective 3: Best Season for Each Crop
# --------------------------------------------

# Find total production per crop per season
season_crop_prod = df_cleaned.groupby(['Crop', 'Season'])['Production'].sum().reset_index()

# Find the best season per crop (i.e., max production season for each crop)
best_season_per_crop = season_crop_prod.sort_values(['Crop', 'Production'], ascending=[True, False])
best_season_per_crop = best_season_per_crop.groupby('Crop').first().reset_index()

# ---------------------------
# 🧹 Filter Outliers (Top 5%)
# ---------------------------
threshold = best_season_per_crop['Production'].quantile(0.95)
filtered = best_season_per_crop[best_season_per_crop['Production'] <= threshold].copy()

# ----------------------------------
# Normalize using Lambda Function
# ----------------------------------
min_val = filtered['Production'].min()
max_val = filtered['Production'].max()

filtered['Normalized_Production'] = filtered['Production'].apply(
    lambda x: (x - min_val) / (max_val - min_val)
)

# -------------------
# Visualization
# -------------------
plt.figure(figsize=(14, 8))
sns.barplot(
    data=filtered.sort_values('Normalized_Production', ascending=False).head(20),
    x='Normalized_Production',
    y='Crop',
    hue='Season',
    dodge=False,
    palette='Set2'
)
plt.title('🌾 Best Season for Top 20 Crops by Normalized Production (Outliers Removed)', fontsize=16, fontweight='bold')
plt.xlabel('Normalized Production (0 to 1)')
plt.ylabel('Crop')
plt.legend(title='Season', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.5)

# ------------------------------------------------
# Objective 4: Evaluate Crop Yield Efficiency
# ------------------------------------------------

# --------------------------------------------
# Step 1: Clean and Compute Yield
# --------------------------------------------
df_yield = df_cleaned[(df_cleaned['Area'] > 0) & (~df_cleaned['Area'].isnull())].copy()
df_yield['Yield'] = df_yield['Production'] / df_yield['Area']

# --------------------------------------------
# Step 2: Remove Outliers using IQR
# --------------------------------------------
Q1 = df_yield['Yield'].quantile(0.25)
Q3 = df_yield['Yield'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df_yield_filtered = df_yield[(df_yield['Yield'] >= lower_bound) & (df_yield['Yield'] <= upper_bound)]

# --------------------------------------------
# Step 3: Normalize Yield using Min-Max Scaling (Manually)
# --------------------------------------------
min_yield = df_yield_filtered['Yield'].min()
max_yield = df_yield_filtered['Yield'].max()

# Avoid division by zero in case min == max
if max_yield != min_yield:
    df_yield_filtered['Yield_Normalized'] = (df_yield_filtered['Yield'] - min_yield) / (max_yield - min_yield)
else:
    df_yield_filtered['Yield_Normalized'] = 1  # or 0, since all values are the same

# --------------------------------------------
# Step 4: Compute Average Normalized Yield per Crop
# --------------------------------------------
avg_yield_crop_norm = df_yield_filtered.groupby('Crop')['Yield_Normalized'].mean().reset_index()
avg_yield_crop_norm = avg_yield_crop_norm.sort_values(by='Yield_Normalized', ascending=False)

# --------------------------------------------
# Step 5: Visualization
# --------------------------------------------
plt.figure(figsize=(14, 8))
sns.barplot(
    data=avg_yield_crop_norm.head(20),
    x='Yield_Normalized',
    y='Crop',
    palette='cubehelix'
)
plt.title('Top 20 Crops by Normalized Average Yield (Outliers Removed)', fontsize=16, fontweight='bold')
plt.xlabel('Normalized Average Yield')
plt.ylabel('Crop')
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.5)

# --------------------------------------------
# Step 6: Print Top 10 Crops
# --------------------------------------------
print("\nTop 10 Crops by Normalized Average Yield (after outlier removal):")
print(avg_yield_crop_norm.head(10))

# ------------------------------------------------
# Objective 5: Detect Anomalies in Crop Production
# ------------------------------------------------

# Calculate mean and std
mean_yield = df_yield_filtered['Yield'].mean()
std_yield = df_yield_filtered['Yield'].std()

# Assign Z-Score safely
df_yield_filtered.loc[:, 'Z_Score'] = (df_yield_filtered['Yield'] - mean_yield) / std_yield

# Filter anomalies
anomalies = df_yield_filtered[(df_yield_filtered['Z_Score'] > 3) | (df_yield_filtered['Z_Score'] < -3)]

# Show valid columns only
columns_to_show = [col for col in ['State_Name', 'District_Name', 'Crop', 'Season', 'Year', 'Area', 'Production', 'Yield', 'Z_Score'] if col in anomalies.columns]
print("\nAnomalies Detected in Crop Yield (Z-Score > 3 or < -3):")
print(anomalies[columns_to_show].sort_values(by='Z_Score', ascending=False))

# --------------------------------------------
# Visualize Z-Score Distribution as Histogram
# --------------------------------------------
plt.figure(figsize=(10, 6))
plt.hist(df_yield_filtered['Z_Score'], bins=100, color='cornflowerblue', edgecolor='black', alpha=0.8)

# Add threshold lines
plt.axvline(x=3, color='red', linestyle='--', linewidth=2, label='Upper Threshold (z = 3)')
plt.axvline(x=-3, color='red', linestyle='--', linewidth=2, label='Lower Threshold (z = -3)')

# Labels and title
plt.title('Histogram of Z-Scores for Crop Yields')
plt.xlabel('Z-Score')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
