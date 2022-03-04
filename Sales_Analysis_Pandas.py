#!/usr/bin/env python
# coding: utf-8

# In[85]:


import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')


# In[72]:


path = os.getcwd()
print(path)


# In[73]:


os.chdir("SalesAnalysis")


# #### Task-1_Merge the 12 months of sales data into a single CSV file 

# In[74]:


df = pd.read_csv("./Sales_Data/Sales_April_2019.csv")

files = [file for file in os.listdir("./Sales_Data")]

all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv("./Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data, df])
all_months_data.head()
all_months_data.to_csv("all_data.csv", index=False)


# In[75]:


all_data = pd.read_csv("all_data.csv")
all_data.head()


# ### Clean up the data 

# In[76]:


nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()


# In[77]:


all_data = all_data.dropna(how ='all')
all_data.head()


# In[80]:


all_data = all_data[all_data['Order Date'].str[0:2]!='Or']


# #### Convert columns to correst type

# In[81]:


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])


# In[ ]:





# In[ ]:





# #### Augment the data with additional columns 

# #### Task-2_ Add month column

# In[82]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# #### Task-3_ Add a sales column 

# In[83]:


all_data['Sales'] = all_data['Quantity Ordered']*all_data['Price Each']
all_data.head()


# In[ ]:





# #### Question_1: What was the best month for sales? How much was earned that month?

# In[110]:


Month_sales = all_data.groupby('Month').sum()['Sales']
Month_sales


# In[109]:


months = range(1,13)
plt.bar(months, Month_sales)
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.show()


# In[93]:


#### Task_4: Create a city and a state column


# In[151]:


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

# In[158]:


City_sales = all_data.groupby('City').sum()['Sales']
City_sales


# In[169]:


City_names = [City for City, df in all_data.groupby('City')]
City_names


# In[170]:


plt.barh(City_names, City_sales)
plt.show()


# ### What time should we display advertisements to maximize likelihood of customer's buying product?

# In[183]:


all_data['Time'] = all_data['Order Date'].str.split(" ")
all_data['Time'] = all_data['Time'].str[1]
all_data['Time'] = all_data['Time'].str.split(":")
all_data['Time'] = all_data['Time'].str[0]
all_data.head()


# In[187]:


Time_hours = [time for time, df in all_data.groupby('Time')]
City_sales = all_data.groupby('Time').sum()['Sales']


# In[191]:


plt.bar(Time_hours, City_sales)
plt.show()
plt.plot(Time_hours, City_sales)
plt.show()
