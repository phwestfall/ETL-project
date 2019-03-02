#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import pandas as a dependency
import pandas as pd


# In[2]:


# import csv into a dataframe
geo_df = pd.read_csv("census_block.csv", encoding='latin 1')


# In[3]:


# show me what you got
geo_df.head()


# In[4]:


# add preceding zeros to the columns in order to create a 12 digits census block group code

geo_df['State'] = geo_df['State'].apply(lambda x: '{0:0>2}'.format(x))
geo_df['County'] = geo_df['County'].apply(lambda x: '{0:0>3}'.format(x))
geo_df['Tract'] = geo_df['Tract'].apply(lambda x: '{0:0>6}'.format(x))


# In[5]:


# create census block group
geo_df['Census_Block_Group'] = geo_df['State'].astype(str) + geo_df['County'].astype(str) + geo_df['Tract'].astype(str) + geo_df['Block_Group'].astype(str)


# In[6]:


# show me what you got
geo_df.head()


# In[7]:


# create 5 digit FIPS code

geo_df['FIPS'] = geo_df['State'].astype(str) + geo_df['County'].astype(str)


# In[8]:


geo_df.head()


# In[9]:


# create 11 digit census tract

geo_df['Census_Tract'] = geo_df['State'].astype(str) + geo_df['County'].astype(str) + geo_df['Tract'].astype(str)


# In[10]:


# show me what you got
geo_df.head()


# In[11]:


# create columns with no preceding zeros (some data sources omit the preceding zero with FIPS, CBG, and Census Tract)
geo_df['No_Zero_FIPS'] = [x.lstrip("0") for x in geo_df['FIPS']]
geo_df['No_Zero_CBG'] = [x.lstrip("0") for x in geo_df['Census_Block_Group']]
geo_df['No_Zero_Census_Tract'] = [x.lstrip("0") for x in geo_df['Census_Tract']]


# In[ ]:





# In[12]:


# replace Puerto Rico Commonwewealth with Puerto Rico for a later merge

geo_df.replace({'Puerto Rico Commonwealth': 'Puerto Rico'})


# In[13]:


# clean up and re-order columns

geo_df = geo_df[['State', 'State_name', 'County', 'County_name',
                  'FIPS', 'No_Zero_FIPS', 'Tract', 'Census_Tract',
                  'No_Zero_Census_Tract', 'Census_Block_Group', 'No_Zero_CBG',
                  'Block_Group']]


# In[ ]:





# In[14]:


# URL to scrape to add state abbreviations
url = 'https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations'


# In[15]:


# scrape the URL
tables = pd.read_html(url)


# In[16]:


#locate the correct table and set it to a dataframe
df_state = tables[0]


# In[17]:


# remove the first rows because of unnecessary data
df_state = df_state.drop(df_state.index[0:12])
df_state.head()


# In[ ]:





# In[18]:


# rename numbered columns to match the table columns from the wikipedia
df_state.rename(columns={ df_state.columns[0]: "State",
                        df_state.columns[2]: "ISO",
                        df_state.columns[3]: "ANSI",
                        df_state.columns[5]: "USPS",
                        df_state.columns[6]: "USCG",
                        df_state.columns[7]: "GPO",
                        df_state.columns[8]: "AP",}, inplace=True)


# In[19]:


df_state.head(5)


# In[20]:


# mass remove columns from dataframe with unnecessary or null data
cols = [1,4,9,10,11,12,13,14]
df_state.drop(df_state.columns[cols],axis=1,inplace=True)


# In[21]:


# reset the index
df_state = df_state.reset_index(drop=True)


# In[22]:


# remove rows for non-states and reset the index so that puerto rico doesn't look out of place
df_state = df_state.drop(df_state.index[55:85])
df_state = df_state.drop(df_state.index[51:54])
df_state = df_state.reset_index(drop=True)


# In[23]:


df_state.head()


# In[ ]:





# In[24]:


# merge geo_df with state_df

merge_df = geo_df.merge(df_state, left_on='State_name', right_on='State')


# In[25]:


merge_df.head()


# In[26]:


# rename original state_x as state and dropping the duplicate state_y column

merge_df = merge_df.rename(columns={'State_x': 'State'})
merge_df = merge_df.drop(['State_y'], axis=1)


# In[27]:


merge_df.head()


# In[ ]:




