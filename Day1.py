import pandas as pd #importing pandas to read data and manipulate it

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
