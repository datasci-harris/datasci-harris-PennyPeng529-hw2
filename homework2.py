"""
Write your answers in the space between the questions, and commit/push only
this file (homework2.py) and countries.csv to your repo. Note that there can 
be a difference between giving a "minimally" right answer, 
and a really good answer, so it can pay to put thought into your work. 

This is a much longer project than those you've done in class - remember to use
comments to help readers navigate your work!

To answer these questions, you will use the two csv files provided in the repo.
The file named gdp.csv contains the per capita GDP of many countries in and 
around Europe in 2023 US dollars. The file named population.csv contains 
estimates of the population of many countries.
"""

"""
QUESTION 1

Short: Open the data

Long: Load the GDP data into a dataframe. Specify an absolute path using the Python 
os library to join filenames, so that anyone who clones your homework repo 
only needs to update one string for all loading to work.
"""
import pandas as pd
import os

data_dir="/Users/pengjingtong/Downloads"
filename="gdp.csv"
file_path=os.path.join(data_dir, filename)
gdp_data=pd.read_csv(file_path)
print(gdp_data.head())
"""
QUESTION 2

Short: Clean the data

Long: There are numerous issues with the data, on account of it having been 
haphazardly assembled from an online table. To start with, the column containing
country names has been labeled TIME. Fix this.

Next, trim this down to only member states of the European Union. To do this, 
find a list of members states (hint: there are 27 as of Apr 2024) and manually 
create your own CSV file with this list. Name this file countries.csv. Load it 
into a dataframe. Merge the two dataframes and keep only those rows with a 
match.

(Hint: This process should also flag the two errors in naming in gdp.csv. One 
 country has a dated name. Another is simply misspelt. Correct these.)
"""
#Rename the column labeled "TIME" to "Country"
gdp_data.rename(columns={"TIME": "Country"},inplace=True)

#replace incorrect country names
gdp_data['Country']=gdp_data["Country"].replace({'Czechia': 'Czech Republic', 'Itly':'Italy'})

#define the list of EU member states
eu_countries = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary",
    "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
    "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"]

#create a dataframe with the list of EU state
df_eu_countries=pd.DataFrame(eu_countries, columns=['Country'])

#save the DataFrame to a CSV file
csv_path="/Users/pengjingtong/Downloads/countries.csv"
df_eu_countries.to_csv(csv_path, index=False)

#Merge the GDP data with the EU countries
df_filtered_gdp=pd.merge(gdp_data, df_eu_countries, on='Country')

print(df_filtered_gdp.head())

"""
QUESTION 3

Short: Reshape the data

Long: Convert this wide data into long data with columns named year and gdp.
The year column should contain int datatype objects.

Remember to convert GDP from string to float. (Hint: the data uses ":" instead
of NaN to denote missing values. You will have to fix this first.) 
"""
#Replace ":" with NaN to denote missing values
gdp_data.replace(":", pd.NA, inplace=True)
#Reshape the dataframe from wide to long format
gdp_long=pd.melt(gdp_data,id_vars=["Country"],var_name="year", value_name="gdp")
gdp_long["year"]=gdp_long["year"].str.extract(r'(\d+)').astype(int)
gdp_long["gdp"]=pd.to_numeric(gdp_long["gdp"], errors="coerce")
print(gdp_long)
"""
QUESTION 4

Short: Repeat this process for the population data.

Long: Load population.csv into a dataframe. Rename the TIME columns. 
Merge it with the dataframe loaded from countries.csv. Make it long, naming
the resulting columns year and population. Convert population and year into int.
"""
import os
import pandas as pd
data_dir="/Users/pengjingtong/Downloads"
filename="population.csv"
file_path=os.path.join(data_dir, filename)
df=pd.read_csv(file_path)

df.rename(columns={"TIME":"Country"}, inplace=True)
df_eu_countries=pd.read_csv('countries.csv')
#Merge population DataFrame with countries DataFrame
df_merged=pd.merge(df, df_eu_countries, on="Country")
df_long_2=df_merged.melt(id_vars="Country", var_name="year", value_name="population")
df_long_2["year"]=df_long_2["year"].str.extract('(\d+)').astype(int)
df_long_2["population"]=pd.to_numeric(df_long_2["population"], errors="coerce").fillna(0).astype(int)
print(df_long_2.head())
"""
QUESTION 5

Short: Merge the two dataframe, find the total GDP

Long: Merge the two dataframes. Total GDP is per capita GDP times the 
population.
"""
import pandas as pd
#Merge the two DataFrames on 'Country' and 'year'
df_merged= pd.merge(gdp_long, df_long_2, on=["Country", "year"])
#Calculate total GDP by multiplying 'gdp' and 'population'
df_merged["total_gdp"]=df_merged["gdp"]* df_merged["population"]
print(df_merged.head())

"""
QUESTION 6

Short: For each country, find the annual GDP growth rate in percentage points.
Round down to 2 digits.

Long: Sort the data by name, and then year. You can now use a variety of methods
to get the gdp growth rate, and we'll suggest one here: 

1. Use groupby and shift(1) to create a column containing total GDP from the
previous year. We haven't covered shift in class, so you'll need to look
this method up. Using groupby has the benefit of automatically generating a
missing value for 2012; if you don't do this, you'll need to ensure that you
replace all 2012 values with missing values.

2. Use the following arithematic operation to get the growth rate:
    gdp_growth = (total_gdp - total_gdp_previous_year) * 100 / total_gdp
"""
#1
df_merged_sorted=df_merged.sort_values(by=["Country", "year"])
#Create a new column containing the total GDP from privious year
df_merged_sorted["total_gdp_previous_year"]=df_merged_sorted.groupby("Country")["total_gdp"].shift(1)
print(df_merged_sorted.head())

#2 get the growth rate
df_merged_sorted["gdp_growth_rate"]=(
    (df_merged_sorted["total_gdp"] - df_merged_sorted["total_gdp_previous_year"]
                                      )*100)/df_merged_sorted["total_gdp"]
#Drop rows with missing values in the "gdp_growth_rate"
df_merged_sorted.dropna(subset=["gdp_growth_rate"], inplace=True)
#Round the values in "gdp_grwoth_rate" to two decimal places
df_merged_sorted["gdp_growth_rate"]=df_merged_sorted["gdp_growth_rate"].round(2)
print(df_merged_sorted[["Country", "year", "gdp_growth_rate"]].head())
"""
QUESTION 7

Short: Which country has the highest total gdp (for the any year) in the EU? 

Long: Do not hardcode your answer! You will have to put the automate putting 
the name of the country into a string called country_name and using the following
format string to display it:

print(f"The largest country in the EU is {country_name}")
"""
#Find the largest country in the EU
largest_gdp_row= df_merged.loc[df_merged["total_gdp"].idxmax()]
largest_country= largest_gdp_row["Country"]
print(f"The largest country in the EU is {largest_country}")

"""
QUESTION 8

Create a dataframe that consists only of the country you found in Question 7

In which year did this country have the most growth in the period 2012-23?

In which year did this country have the least growth in the peroid 2012-23?

Do not hardcode your answer. You will have to use the following format strings 
to show your answer:

print(f"Their best year was {best_year}")
print(f"Their worst year was {worst_year}")
"""
#Filter the DataFrame for the specific country
country_df=df_merged_sorted[df_merged_sorted["Country"]==largest_country]
#Filter for the years 2012 to 2023
country_df=country_df[(country_df["year"]>=2012) & (country_df["year"]<=2023)]
best_year =country_df.loc[country_df["gdp_growth_rate"].idxmax(), "year"]
worst_year =country_df.loc[country_df["gdp_growth_rate"].idxmin(),"year"]
#Print the results using f-strings
print(f"Their best year was {best_year}")
print(f"Their worst year was {worst_year}")