
# coding: utf-8

# In[ ]:


import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


# In[ ]:


# filepath = '/data/'
# filename = 'EU_RenewableEng_Prod_05-16.csv'
# df = pd.read_csv(filepath, filename)
filename_path1 = '../data/EU_RenewableEng_Prod_05-16.csv'
df1 = pd.read_csv(filename_path1)


# In[ ]:


df1.head()


# In[ ]:


filename_path2 = '../data/CO2Emm_Global_1970-16.csv'

df2 = pd.read_csv(filename_path2)


# In[ ]:


df2.head()


# In[ ]:


df = pd.merge(df1, df2, how='left', left_on=['Country', 'Year'], right_on=['ISO_NAME', 'Year'])


# In[ ]:


df.head()


# In[ ]:


df.Country.unique()


# In[ ]:


df.ISO_NAME.unique()


# In[ ]:


df_Ireland = df.loc[(df['Country']=='Ireland') & (df['Product']=='Renewable energies')]


# In[ ]:


df_Ireland.head()


# In[ ]:


df_Ireland.Year.dtype


# In[ ]:


df_Ireland.Value.dtype


# In[ ]:


#dataframe is copy of a slice? correct error
df_Ire = df_Ireland.copy()
df_Ire['Value']= df_Ire.Value.apply(pd.to_numeric)
df_Ire.head()


# In[ ]:


# sns.set_style("darkgrid")
# sns.set_palette("pastel")

# sns.lineplot(data=df_Ire, x='Year', y='Value' )
# sns.lineplot(data=df_Ire, x='Year', y='CO2/cap' )


# In[ ]:


fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('Year')
ax1.set_ylabel('Renewable energy generation', color=color)
ax1.plot(df_Ire.Year, df_Ire.Value, color=color)
ax1.tick_params(axis='y', labelcolor=color)

color = 'tab:blue'
ax2 = ax1.twinx()
ax2.set_ylabel('CO2/capita', color=color)
ax2.plot(df_Ire.Year, df_Ire['CO2/cap'], color=color)
ax2.tick_params(axis='y', labelcolor=color)


# In[ ]:


#Ultimately, to create a prediction model that uses renewable energy generation to predict CO2 for countries that do not have CO2 information

#Let's create the necessary dataframe
# check column headings, keep only ones we want and adapt names, then plot graphs for every country

df.columns 


# In[ ]:


df = df.drop(['Units', 'Indicator', 'ISO_CODE', 'ISO_NAME'], axis=1)

df.rename(columns={'Year':'year',
                  'Country':'country',
                  'Product':'renew_typ',
                  'Value':'renew_ene',
                  'GHG per capita emissions':'ghg',
                  'CO2/cap':'co2'}, inplace='True')


# In[ ]:


df.head()


# In[ ]:


df.dtypes


# In[ ]:


df['renew_ene'] = pd.to_numeric(df.renew_ene, errors='coerce')
df['renew_ene'] = df.renew_ene.apply(pd.to_numeric)


# In[ ]:


df.dtypes


# In[ ]:


renewabledf = df[df.co2.notnull()]


# In[ ]:


renew_countries = renewabledf.country.unique()


# In[ ]:


def two_yaxis(ax1, x, y1, y2, c1, c2, title):
    ax2 = ax1.twinx()
    ax1.plot(x, y1, color=c1)
#     ax1.set_xlabel('Year')
#     ax1.set_ylabel('renewable generation (TOE)')
    ax1.set_title(title)
    ax2.plot(x, y2, color=c2)
#     ax2.set_ylabel('CO2/per capita')


# In[ ]:


ax = plt.subplot(2,1,1)
two_yaxis(ax, df.year, df.renew_ene, df.co2, 'r', 'b', 'all countries')


# In[ ]:


#do subplot for every country
fig = plt.figure(figsize=(16,13))
ax_axis = fig.add_subplot(111)#big subplot for common axis label

ax_axis.set_ylabel('renewable generation (TOE)', color='b')
ax_axis.set_xlabel('Year')
ax_axis.spines['top'].set_color('none')
ax_axis.spines['bottom'].set_color('none')
ax_axis.spines['left'].set_color('none')
ax_axis.spines['right'].set_color('none')
ax_axis.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)


ax_axis2 = ax_axis.twinx()
ax_axis2.set_ylabel('CO2 per capita', color='r')
ax_axis2.spines['top'].set_color('none')
ax_axis2.spines['bottom'].set_color('none')
ax_axis2.spines['left'].set_color('none')
ax_axis2.spines['right'].set_color('none')
ax_axis2.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

fig.subplots_adjust(hspace=1, wspace=1)



for i in range(len(renew_countries)):
    temp = renewabledf[(renewabledf.country==renew_countries[i]) & (renewabledf.renew_typ=='Renewable energies')]
    ax = fig.add_subplot(5,6,i+1)
    two_yaxis(ax, temp.year, temp.renew_ene, temp.co2, 'b', 'r', renew_countries[i])






# plt.show()


# In[ ]:


y_max = renewabledf.renew_ene.max()
y_max

