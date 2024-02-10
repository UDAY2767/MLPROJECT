#!/usr/bin/env python
# coding: utf-8

# # DATA EXPLORATORY ANALSIS FOR CREDIT CARD DATA

# #Business Problem:
# 
# In order to effectively produce quality decisions in the modern credit card industry, knowledge must be gained through effective data analysis and modelling. Through the use of dynamic data-driven decision-making tools and procedures, information can be gathered to successfully evaluate all aspects of credit card operations. PSPD Bank has banking operations in more than 50 countries across the globe. Mr. Jim Watson, CEO, wants to evaluate areas of bankruptcy, fraud and collections, respond to customer requests for help with proactive offers and services.

# # IMPORT THE NECESSARY LIBRARIES

# In[80]:


import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import os


# # IMPORT THE DATASETS

# In[81]:


customer = pd.read_csv(r"C:\Users\udayu\Downloads\archive (2)\CustomerAcqusition.csv",usecols=["Customer","Age","City","Product","Limit","Company","Segment"])


# In[82]:


repay=pd.read_csv(r"C:\Users\udayu\Downloads\archive (2)\Repayment.csv",usecols = ["Customer","Month","Amount"])


# In[83]:


spend=pd.read_csv(r"C:\Users\udayu\Downloads\archive (2)\spend.csv",usecols=["Customer","Month","Type","Amount"])


# In[84]:


customer.head()


# In[85]:


repay.head()


# In[86]:


spend.head()


# # EXPLORATORY DATA ANALYSIS

# In[87]:


print(customer.shape)
print(repay.shape)
print(spend.shape)


# In[88]:


customer.dtypes


# In[89]:


repay.dtypes


# In[90]:


spend.dtypes


# In[91]:


spend.isnull().sum()


# In[92]:


customer.isnull().sum()


# In[93]:


repay.isnull().sum()


# In[94]:


#Dropping null values present in 'repay' dataset
repay.dropna(inplace=True)


# In[95]:


repay.isnull().sum()


# # (1) in the above dataset,
# 
# 
# (a) in case age is less than 18, replace it with mean of age values

# In[96]:


mean_original=customer["Age"].mean()


# In[97]:


print("The mean of age column is :", mean_original)


# In[98]:


#repalce age less than 18 with mean of age values
customer.loc[customer["Age"]<18,"Age"] =customer["Age"].mean()


# In[99]:


mean_new=customer["Age"].mean()


# In[100]:


print("The new mean of age column is:", mean_new)


# In[101]:


customer.loc[customer["Age"]<18,"Age"]


# ALL THE CUSTOMER WHO HAVE AGE IS LESS THAN 18 YEARS HAVE BEEN REPLACED BY MEAN OF AGE COLUMN

# # (B) IN CASE SPEND AMOUNT IS MORE THAN THE LIMIT, REPALCE IT WITH 50% OF CUSTOMER'S LIMIT.(CUSTOMER'S LIMIT PROVEDED IN ACQUISITION TABLE IS THE PER TRANSACTION LIMIT ON HIS CARD)

# In[102]:


customer.head(2)


# In[103]:


spend.head(2)


# In[104]:


# merging customer and spend table on the basis of"customer" column
customer_spend=pd.merge(left=customer,right=spend,on="Customer",how="inner")


# In[105]:


customer_spend.head()


# In[106]:


customer_spend.shape


# In[107]:


#all the custmors whose spend amount is more than the limit, repalacing with 50% of that customers limit
customer_spend[customer_spend["Amount"]>customer_spend['Limit']]


# In[108]:


#if customer's spend amount is more than the limit,replacing with 50% of that customer’s limit
customer_spend.loc[customer_spend["Amount"] > customer_spend["Limit"],"Amount"] = (50 * customer_spend["Limit"]).div(100)


# In[109]:


#there are no customers left whose spend amount is more than the limit
customer_spend[customer_spend["Amount"] > customer_spend['Limit']]


# # (C) incase the repayment amount is more than the limit, replace the repayment with the limit.

# In[110]:


customer.head(1)


# In[111]:


repay.head(1)


# In[112]:


#merge customer and spend table on the baisi of "customer"column
customer_repay=pd.merge(left=repay,right=customer,on="Customer",how="inner")


# In[113]:


customer_repay.head()


# In[114]:


#all the customers where repayment amount is more than the limit.
customer_repay[customer_repay["Amount"] > customer_repay["Limit"]]


# In[115]:


#customers where repayment amount is more than the limit, replacing the repayment with the limit.
customer_repay.loc[customer_repay["Amount"] > customer_repay["Limit"],"Amount"] = customer_repay["Limit"]

#there are no customers left where repayment amount is more than the limit.
customer_repay[customer_repay["Amount"] > customer_repay["Limit"]]


# # 2 FROM THE ABOVE DATASET CREATE THE FOLLOWING SUMMARIES:

# A. HOW THE MANY DISTINCT CUSTOMERS EXIST?

# In[116]:


distinct_customers=customer["Customer"].nunique()


# In[117]:


print("NUMBER OF DISTINCT CUSTOMERS ARE :" , distinct_customers)


# B. HOW MANY DISTINCT CATEGORIES EXIST?

# In[118]:


#CUSTOMER FROM DIFFERENT SEGMENTS
customer["Segment"].value_counts()


# In[122]:


plt.figure(figsize=(8, 6))
sns.countplot(x='Segment', data=customer)
plt.show()


# In[123]:


print("We can see from the countplot that number of distinct categories are", len(customer["Segment"].value_counts()))


# # C. WHAT IS THE AVARAGE MONTHLY SPEND BY CUSTOMERS?

# In[124]:


spend.head()


# In[129]:


#converting month column of "spend" table to data format 
spend["Month"]=pd.to_datetime(spend["Month"])


# In[130]:


spend.head()


# In[133]:


#creating new columns which show "Month" and "Year"
spend['Monthly'] = spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))
spend['Yearly'] = spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))


# In[134]:


spend.head()


# In[136]:


# Assuming 'Amount' is a numeric column
spend['Amount'] = pd.to_numeric(spend['Amount'], errors='coerce')  # Convert to numeric, handle errors

# Grouping by 'Yearly' and 'Monthly' and calculating the mean of 'Amount'
customer_spend_group = round(spend.groupby(['Yearly', 'Monthly'])['Amount'].mean(), 2)


# In[137]:


customer_spend_group


# # D. WHAT IS THE AVERAGE MONTHLY REPAYMENT BY CUSTOMERS?

# In[138]:


repay.head()


# In[146]:


#converting "Month" column to date time format
repay["Month"] = pd.to_datetime(repay["Month"], format="%Y-%m")


# In[147]:


repay.head()


# In[148]:


repay.dtypes


# In[149]:


#creating new columns which show "Month" and "Year"
repay['Monthly'] = repay['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))
repay['Yearly'] = repay['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))


# In[161]:


# Assuming 'Amount' is a numeric column
repay['Amount'] = pd.to_numeric(repay['Amount'], errors='coerce')  # Convert to numeric, handle errors

# Grouping by 'Yearly' and 'Monthly' and calculating the mean of 'Amount'
customer_repay_group = round(repay.groupby(['Yearly', 'Monthly'])['Amount'].mean(), 2)


# In[162]:


customer_repay_group


# # E. IF THE MONTHLY RATE OF INTREST IS 2.9%,WHAT IS THE PROFIT FOR THE BANK FOR EACH MONTHS?

# In[164]:


#merging all the three tables. Alreaady merged customer and spend table in 'customer_spend'. Using "customer_spend" and "repay"
#table to form the final "customer_spend_repay" table
customer_spend_repay = pd.merge(left=customer_spend,right=repay,on="Customer",how="inner")


# In[165]:


customer_spend_repay.head()


# In[166]:


# renaming the columns for clearity
customer_spend_repay.rename(columns={"Amount_x":"Spend_Amount","Amount_y":"Repay_Amount"},inplace=True)


# In[167]:


customer_spend_repay.head()


# In[ ]:





# In[169]:


# Grouping the data based on "Yearly", "Monthly" columns to get the 'Spend_Amount' and 'Repay_Amount'
interest_group = customer_spend_repay.groupby(["Yearly", "Monthly"])[['Spend_Amount', 'Repay_Amount']].sum()


# In[170]:


interest_group


# In[171]:


# Monthly Profit = Monthly repayment – Monthly spend.
interest_group['Monthly Profit'] = interest_group['Repay_Amount'] - interest_group['Spend_Amount']


# In[172]:


interest_group


# In[173]:


#interest earned is 2.9% of Monthly Profit
interest_group['Interest Earned'] = (2.9* interest_group['Monthly Profit'])/100


# In[174]:


interest_group


# # F. WHAT ARE THE TOP 5 PRODUCT TYPES?

# In[175]:


spend.head()


# In[176]:


spend['Type'].value_counts().head()


# In[177]:


spend['Type'].value_counts().head(5).plot(kind='bar')
plt.show()


# # G. WHICH CITY IS HAVING MAXIMUM SPEND?

# In[179]:


customer_spend.head()


# In[180]:


city_spend = customer_spend.groupby("City")["Amount"].sum().sort_values(ascending=False)


# In[181]:


city_spend


# In[182]:


plt.figure(figsize=(5,10))
city_spend.plot(kind="pie",autopct="%1.0f%%",shadow=True,labeldistance=1.0,explode=[0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
plt.title("Amount spent on credit card by customers from different cities")
plt.show()


# In[184]:


print("FROM ABOVE PIE CHART WE CAN SEE THAT COCHIN IS HAVING MAXIMUM SPEND.")


# # H. WHICH AGE GROUP IS SPENDING MORE MONEY?

# In[185]:


#creating new column "Age Group" with 8 bins between 18 to 88 
customer_spend["Age Group"] =  pd.cut(customer_spend["Age"],bins=np.arange(18,88,8),labels=["18-26","26-34", "34-42" ,"42-50" ,"50-58","58-66","66-74","74-82"],include_lowest=True)


# In[186]:


customer_spend.head()


# In[187]:


#grouping data based on "Age Group" and finding the amount spend by each age group and arranging in descending oreder
age_spend = customer_spend.groupby("Age Group")['Amount'].sum().sort_values(ascending=False)


# In[188]:


age_spend


# In[189]:


plt.figure(figsize=(5,10))
age_spend.plot(kind = "pie",autopct="%1.0f%%",explode=[0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0],shadow=True)
plt.show()


# In[190]:


print("From the pie chart shown above we can say that age group 42 - 50 is spending more money")


# # I. WHO ARE THE TOP 10 CUSTOMERS IN TERMS OF REPAYMENTS?

# In[191]:


customer_repay.head()


# In[192]:


#grouping based on "Customer" column to find top 10 customers
customer_repay.groupby("Customer")[["Amount"]].sum().sort_values(by="Amount",ascending=False).head(10)


# # 3. CALCULATE THE CITY WISE SPEND ON EACH PRODUCT ON YEARLY BASIS. ALSO INCLUDE A GRAPHICAL REPRESENTATION FOR THE SAME.

# In[194]:


customer_spend.head()


# In[196]:


#converting "Month" column to date time 
customer_spend["Month"] = pd.to_datetime(customer_spend["Month"],format="%y-%m")


# In[197]:


#creating new column "year" 
customer_spend['Year'] = customer_spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))


# In[198]:


customer_spend.head()


# In[199]:


customer_spend_pivot = pd.pivot_table(data = customer_spend,index=["City","Year"],columns='Product',aggfunc="sum",values="Amount")


# In[200]:


customer_spend_pivot


# In[201]:


customer_spend_pivot.plot(kind="bar",figsize=(18,5),width=0.8)
plt.ylabel("Spend Amount")
plt.title("Amount spended by customers according to year and city")
plt.show()


# # 4. CREATE GRAPHS FOR

# # A. MONTHLY COMPARISON OF TOTAL SPENDS, CITY WISE

# In[202]:


customer_spend.head()


# In[203]:


#creating new column "Monthly" 
customer_spend['Monthly'] = customer_spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))


# In[204]:


customer_spend.head()


# In[205]:


#grouping data based on "Monthly" and "City" columns
month_city = customer_spend.groupby(["Monthly","City"])[["Amount"]].sum().sort_index().reset_index()


# In[206]:


#creating pivot table based on "Monthly" and "City" columns
month_city =pd.pivot_table(data=customer_spend,values='Amount',index='City',columns='Monthly',aggfunc='sum')


# In[207]:


month_city


# In[208]:


month_city.plot(kind="bar",figsize=(18,6),width=0.8)
plt.show()


# # B. COMPARISON OF YEARLY SPEND ON AIR TICKETS

# In[209]:


customer_spend.head()


# In[210]:


air_tickets = customer_spend.groupby(["Year","Type"])[["Amount"]].sum().reset_index()


# In[211]:


filtered = air_tickets.loc[air_tickets["Type"]=="AIR TICKET"]


# In[212]:


filtered


# In[213]:


plt.bar(filtered["Year"],height=filtered["Amount"],color="orange")
plt.xlabel("Year")
plt.ylabel("Amount Spent")
plt.title("Comparison of yearly spend on air tickets")
plt.show()


# # C. COMPARISION OF MONTHLY SPEND FOR EACH PRODUCT (LOOK FOR ANY SEASONALITY THAT EXIST IN TERMS OF SPEND)

# In[215]:


customer_spend.head()


# In[216]:


#creating pivot table based on "Monthly" and "Product" columns
product_wise = pd.pivot_table(data=customer_spend,index='Product',columns='Monthly',values='Amount',aggfunc='sum')


# In[217]:


product_wise


# In[218]:


product_wise.plot(kind="bar",figsize=(18,6),width=0.8)
plt.ylabel("Amount Spend")
plt.title("Amount spent monthly on different products")
plt.show()


# # We can see from the above graph that the sales are high for all the Products during the months:
# 
# January,
# February,
# March,
# April,
# May
# Out of these months,highest sales are in January

# # 5.  Write user defined PYTHON function to perform the following analysis: You need to find top 10 customers for each city in terms of their repayment amount by different products and by different time periods i.e. year or month. The user should be able to specify the product (Gold/Silver/Platinum) and time period (yearly or monthly) and the function should automatically take these inputs while identifying the top 10 customers.

# In[219]:


customer_repay.head()


# In[221]:


# converting 'Month' column to date time format
customer_repay['Month'] = pd.to_datetime(customer_repay['Month'],format="%y-%m")


# In[222]:


#creating new column "Monthly" and "Yearly" using already existing 'Month' column
customer_repay['Monthly'] = customer_repay['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))
customer_repay['Yearly'] = customer_repay['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))


# In[223]:


def summary_report(product,timeperiod):
    print('Give the product name and timeperiod for which you want the data')
    if product.lower()=='gold' and timeperiod.lower()=='monthly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Monthly',aggfunc='sum',values='Amount')
        result = pivot.loc[('Gold',['BANGALORE','COCHIN','CALCUTTA','BOMBAY','CHENNAI','TRIVANDRUM','PATNA','DELHI']),:]
    elif product.lower()=='gold' and timeperiod.lower()=='yearly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Yearly',aggfunc='sum',values='Amount')
        result = pivot.loc[('Gold',['BANGALORE','COCHIN','CALCUTTA','BOMBAY','CHENNAI','TRIVANDRUM','PATNA','DELHI']),:]
    elif product.lower()=='silver' and timeperiod.lower()=='monthly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Monthly',aggfunc='sum',values='Amount')
        result = pivot.loc[('Silver',['BANGALORE','COCHIN','CALCUTTA','BOMBAY','CHENNAI','TRIVANDRUM','PATNA','DELHI']),:]
    elif product.lower()=='silver' and timeperiod.lower()=='yearly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Yearly',aggfunc='sum',values='Amount')
        result = pivot.loc[('Silver',['BANGALORE','COCHIN','CALCUTTA','BOMBAY','CHENNAI','TRIVANDRUM','PATNA','DELHI']),:]
    if product.lower()=='platinum' and timeperiod.lower()=='monthly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Monthly',aggfunc='sum',values='Amount')
        result = pivot.loc[('Platinum',['BANGALORE','COCHIN','CALCUTTA','BOMBAY','CHENNAI','TRIVANDRUM','PATNA','DELHI']),:]
    elif product.lower()=='platinum' and timeperiod.lower()=='yearly':
        pivot = customer_repay.pivot_table(index=['Product','City','Customer'],columns='Yearly',aggfunc='sum',values='Amount')
        result = pivot.loc[('Platinum',['BANGALORE','COCHIN','CALCUTTA','BOMBAY','CHENNAI','TRIVANDRUM','PATNA','DELHI']),:]
    return result


# In[224]:


summary_report('gold','monthly')


# # THE PROJECT IS COMPLETED 
