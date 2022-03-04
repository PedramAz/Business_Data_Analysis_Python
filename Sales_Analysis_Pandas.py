#!/usr/bin/env python
# coding: utf-8

# In[250]:


import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')


# In[251]:


path = os.getcwd()
print(path)


# In[252]:


os.chdir("C:/Users/azimz/Desktop/Technical_Practice_working files/Python_Pandas/Pandas-Data-Science-Tasks-master/SalesAnalysis")


# #### Task-1_Merge the 12 months of sales data into a single CSV file 

# In[253]:


df = pd.read_csv("./Sales_Data/Sales_April_2019.csv")

files = [file for file in os.listdir("./Sales_Data")]

all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv("./Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data, df])
all_months_data.head()
all_months_data.to_csv("all_data.csv", index=False)


# In[254]:


all_data = pd.read_csv("all_data.csv")
all_data.head()


# ### Clean up the data 

# In[255]:


nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()


# In[256]:


all_data = all_data.dropna(how ='all')
all_data.head()


# In[257]:


all_data = all_data[all_data['Order Date'].str[0:2]!='Or']


# #### Convert columns to correst type

# In[258]:


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])


# In[ ]:





# In[ ]:





# #### Augment the data with additional columns 

# #### Task-2_ Add month column

# In[259]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# #### Task-3_ Add a sales column 

# In[260]:


all_data['Sales'] = all_data['Quantity Ordered']*all_data['Price Each']
all_data.head()


# In[ ]:





# #### Question_1: What was the best month for sales? How much was earned that month?

# In[261]:


Month_sales = all_data.groupby('Month').sum()['Sales']
Month_sales


# In[262]:


months = range(1,13)
plt.bar(months, Month_sales)
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.show()


# In[263]:


#### Task_4: Create a city and a state column


# In[264]:


all_data['City'] = all_data['Purchase Address'].str.split(",")
all_data['City'] = all_data['City'].str[1]

all_data['State'] = all_data['Purchase Address'].str.split(",")
all_data['State'] = all_data['State'].str[2]

all_data['City'] = all_data[['City', 'State']].apply(lambda x: ''.join(x), axis=1)
all_data = all_data.drop('State', 1)

def get_city(address):
    return address.split(' ')[1]
def get_state(address): 
    return address.split(' ')[2]

all_data['City'] = all_data['City'].apply(lambda x:get_city(x) + ' ' + get_state(x))

all_data.head()


# ### Question_2: What city had the highest number of sales?

# In[265]:


City_sales = all_data.groupby('City').sum()['Sales']
City_sales


# In[266]:


City_names = [City for City, df in all_data.groupby('City')]
City_names


# In[267]:


plt.barh(City_names, City_sales)
plt.show()


# ### Question_3: What time should we display advertisements to maximize likelihood of customer's buying product?

# In[268]:


all_data['Time'] = all_data['Order Date'].str.split(" ")
all_data['Time'] = all_data['Time'].str[1]
all_data['Time'] = all_data['Time'].str.split(":")
all_data['Time'] = all_data['Time'].str[0]
all_data.head()


# In[269]:


Time_hours = [time for time, df in all_data.groupby('Time')]
City_sales = all_data.groupby('Time').sum()['Sales']


# In[270]:


plt.bar(Time_hours, City_sales)
plt.show()
plt.plot(Time_hours, City_sales)
plt.show()


# #### Question_4: What products are most often sold together?

# In[271]:


df = all_data[all_data['Order ID'].duplicated(keep=False)]
df.head()


# In[272]:


df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df = df[['Order ID', 'Grouped']].drop_duplicates()
df.head()


# In[273]:


df['Grouped'].value_counts().head(20)


# #### What product sold the most? Why do you think it sold the most?

# In[274]:


df2 = all_data['Product'].value_counts()


# In[275]:


pd.DataFrame({'Products':df2.index, 'Total Number Sold':df2.values})


# In[301]:


df2.plot.bar(x='Products', y='Total Number Sold', rot=90)
plt.xlabel('Products')
plt.ylabel('Quantity Ordered')


# In[285]:


df3 = all_data.groupby('Product').mean()['Price Each']
df3


# In[286]:


pd.DataFrame({'Products':df3.index, 'Average Price':df3.values})


# In[308]:


df3.plot(x='Products', y='Average Price', kind = 'line', rot = 90)
plt.show()


# In[330]:


df_23 = pd.concat([df2, df3], axis=1, join='inner')
df_23.index.name = 'Product Name'
df_23.reset_index(inplace=True)
df_23


# In[333]:


df_23.rename(columns={'Product Name':'Products', 'Product':'Total Number Sold', 'Price Each':'Average Price'}, inplace=True)
df_23.head()


# In[346]:


dd=df_23.plot(x='Products', y=["Total Number Sold",  "Average Price"], secondary_y=[ "Average Price"], rot=45)
fig = plt.gcf()
fig.set_size_inches(15, 10.5)
fig.savefig('test2png.png', dpi=100)

