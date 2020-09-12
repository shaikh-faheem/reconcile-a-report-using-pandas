# --------------
# 1.Loading data & Calculating the total amount of all the users for the month of jan, feb and Mar and also the grand total.
# Code starts here

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(path)

# Converting States in Lower Case.
df['state'] = df['state'].apply(lambda x: x.lower())

# Total amount in the first quarter of the financial year
df['total'] = df['Jan'] + df['Feb'] + df['Mar']

sum_row = df[['Jan','Feb','Mar','total']].sum()

df_final = df.append(sum_row, ignore_index = True)
print(df_final)


# --------------
# 2. Scraping data from the web and cleaning it.
# Code starts here

import requests

url = 'https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations'

response = requests.get(url)

df1 = pd.read_html(response.content)[0]

df1.drop(index = [0,1,2,3,4,5,6,7,8,9,10],inplace = True)

df1 = df1.rename(columns =df1.iloc[0,:]).iloc[1:,:]

df1['United States of America'] = df1['United States of America'].apply(lambda x: x.replace(" ",""))

print(df1.head())


# --------------
# 3.Mapping abbreviation to the name of states.
# Code starts here

df1['United States of America'] = df1['United States of America'].astype(str).apply(lambda x: x.lower())
df1['US'] = df1['US'].astype(str)

# Mapping
mapping = df1.set_index('United States of America')['US'].to_dict()
df_final.insert(6, 'abbr', np.nan)
df_final['abbr'] = df_final['state'].map(mapping)


# --------------
# 4. Filling some missing values manually.
# Code stars here

df_mississipi = df_final[df_final['state'] == 'mississipi'].replace(np.nan, 'MS')
df_tenessee  = df_final[df_final['state'] == 'tenessee'].replace(np.nan, 'TN')
df_final.replace(df_final.iloc[6],df_mississipi,inplace = True)
df_final.replace(df_final.iloc[10],df_tenessee,inplace = True)


# --------------
#5. Introducing units('$')
# Code starts here

# Calculate the total amount
df_sub = df_final.groupby('abbr')[['Jan','Feb','Mar','total']].sum()
# Add the $ symbol
formatted_df = df_sub.applymap(lambda x: str(x) + '$') 


# --------------
# 6.We will append a row to the data frame which will give us information about the total amount of the various regions in Jan, Feb and march and also the grand total.
# Code starts here.

# Calculate the sum
sum_row = df[['Jan','Feb','Mar','total']].sum()
df_sub_sum = sum_row.transpose()

#apply $ to the sum
df_sub_sum = df_sub_sum.apply(lambda x : "$" + str(x))

print(df_sub_sum)
# append the sum
final_table = formatted_df.append(df_sub_sum,ignore_index=True) 
# rename the index
final_table.rename(index={13: "Total"})


# --------------
#7. Having prepared all the data now its time to present the results visually.
# Code starts here

# Calculate the total
df_sub['total'] = df_sub['total'].sum()

# Plot the pie chart   
df_sub['total'].plot.pie(figsize=(5, 5))

# Code ends here
