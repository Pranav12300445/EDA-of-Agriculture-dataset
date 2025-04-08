Day1.py output

Checking if dataset is being read properly or not

                    State_Name District_Name  Crop_Year       Season                 Crop    Area  Production
0  Andaman and Nicobar Islands      NICOBARS       2000  Kharif                  Arecanut  1254.0      2000.0
1  Andaman and Nicobar Islands      NICOBARS       2000  Kharif       Other Kharif pulses     2.0         1.0
2  Andaman and Nicobar Islands      NICOBARS       2000  Kharif                      Rice   102.0       321.0
3  Andaman and Nicobar Islands      NICOBARS       2000  Whole Year                Banana   176.0       641.0
4  Andaman and Nicobar Islands      NICOBARS       2000  Whole Year             Cashewnut   720.0       165.0

Information about dataset:

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 246091 entries, 0 to 246090
Data columns (total 7 columns):
 #   Column         Non-Null Count   Dtype
---  ------         --------------   -----
 0   State_Name     246091 non-null  object
 1   District_Name  246091 non-null  object
 2   Crop_Year      246091 non-null  int64
 3   Season         246091 non-null  object
 4   Crop           246091 non-null  object
 5   Area           246091 non-null  float64
 6   Production     242361 non-null  float64
dtypes: float64(2), int64(1), object(4)
memory usage: 13.1+ MB
None

Description about dataset:

           Crop_Year          Area    Production
count  246091.000000  2.460910e+05  2.423610e+05
mean     2005.643018  1.200282e+04  5.825034e+05
std         4.952164  5.052340e+04  1.706581e+07
min      1997.000000  4.000000e-02  0.000000e+00
25%      2002.000000  8.000000e+01  8.800000e+01
50%      2006.000000  5.820000e+02  7.290000e+02
75%      2010.000000  4.392000e+03  7.023000e+03
max      2015.000000  8.580100e+06  1.250800e+09

Missing values in each column:

State_Name          0
District_Name       0
Crop_Year           0
Season              0
Crop                0
Area                0
Production       3730
dtype: int64

Rows before dropping NAs in 'Production': 246091
Rows after dropping NAs in 'Production' : 242361
Total rows dropped                      : 3730

Day2.py output

Unique States: 33
Unique Districts: 646
Unique Crops: 124
Unique Seasons: 6

Top 5 crops by total production:
Crop
Coconut      1.299816e+11
Sugarcane    5.535682e+09
Rice         1.605470e+09
Wheat        1.332826e+09
Potato       4.248263e+08
Name: Production, dtype: float64

