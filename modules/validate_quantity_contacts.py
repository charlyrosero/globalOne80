import pandas as pd
import warnings
import glob
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

#cleanFiles

import glob, os, os.path

filelist = glob.glob(os.path.join("C:\Personal\Global80One\data\output", "*"))
for f in filelist:
    os.remove(f)

warnings.simplefilter("ignore")

#quickbooks Contacts
quickbooks_contacts='C:\Personal\Global80One\data\Global+One80_Donor+Contact+List.xlsx'
df_quickbooks_contacts = pd.read_excel(quickbooks_contacts, engine="openpyxl")

#replace nan values
df_quickbooks_contacts.fillna('', inplace=True)
#drop trash columns
df_quickbooks_contacts.drop(columns=df_quickbooks_contacts.columns[0], inplace=True)
#drop trash rows
df_quickbooks_contacts.drop(labels=[0,1,2,3], axis=0,inplace=True)
#drop trash last 3 rows
df_quickbooks_contacts.drop(df_quickbooks_contacts.tail(3).index,inplace=True)

#rename cols
df_quickbooks_contacts.rename(columns={
                                        "Unnamed: 1": "Donor", 
                                        "Unnamed: 2": "Phone Numbers", 
                                        "Unnamed: 3": "Email",
                                        "Unnamed: 4": "Full Name",
                                        "Unnamed: 5": "Billing Address",
                                        "Unnamed: 6":"Shipping Address"}
                            , inplace=True)

df_quickbooks_contacts.replace('Mr. ', '', regex=True, inplace=True)
df_quickbooks_contacts.replace('Pastor ', '', regex=True, inplace=True)
df_quickbooks_contacts.replace('Ms. ', '', regex=True, inplace=True)
df_quickbooks_contacts.replace('Ms ', '', regex=True, inplace=True)
df_quickbooks_contacts.replace('Mrs. ', '', regex=True, inplace=True)
df_quickbooks_contacts.replace('Rev. ', '', regex=True, inplace=True)
df_quickbooks_contacts.replace('Sr. ', '', regex=True, inplace=True)
df_quickbooks_contacts.replace('Sra. ', '', regex=True, inplace=True)
df_quickbooks_contacts.replace('Dr. ', '', regex=True, inplace=True)
df_quickbooks_contacts.replace('Mr ', '', regex=True, inplace=True)


#Donor with Full Name Different to Sales Force Full Name
df_quickbooks_contacts.replace('Kaleo Grays Harbor', 'Kaleo Kaleo Grays Harbor', regex=True, inplace=True)
df_quickbooks_contacts.replace('Network for God', 'Network for Network for God', regex=True, inplace=True)
df_quickbooks_contacts.replace('Francois Bateaux', 'Bateaux Francois', regex=True, inplace=True)
df_quickbooks_contacts.replace('Main Street Baptist Church', 'Main Street Baptist Church Main Street Baptist Church', regex=True, inplace=True)
df_quickbooks_contacts.loc[(df_quickbooks_contacts.Donor == 'Paypal Fundation'),'Full Name']='Paypal Fundation'


#Sakesforce Contacts

salesforce_contacts='C:\Personal\Global80One\data\Custom_Report_Contacts_2022-02-12_1337.csv'
df_salesforce_contacts = pd.read_csv(salesforce_contacts)



#Sakesforce Contacts

# specifying the path to csv files
path = "C:\Personal\Global80One\data"

# csv files in the path
files = glob.glob(f'{path}/*.csv')

print(files)

# defining an empty list to store 
# content
df_salesforce_contacts = pd.DataFrame()
content = []
  
# checking all the csv files in the 
# specified path
for filename in files:
    
    # reading content of csv file
    # content.append(filename)
    df_salesforce_contacts = pd.read_csv(filename)
    


#replace nan values
df_salesforce_contacts.fillna('', inplace=True)

print('Salesforce Contacts = ' + str(df_salesforce_contacts[df_salesforce_contacts.columns[0]].count()))
print('QuickBooks Contacts = ' + str(df_quickbooks_contacts[df_quickbooks_contacts.columns[0]].count()))

total_merge = df_quickbooks_contacts.merge(df_salesforce_contacts, on='Full Name', how='outer', indicator=True)

news_quickbooks_contacts= total_merge[total_merge['_merge']=='left_only']



df_output_csv = pd.DataFrame(columns = ['First Name','Last Name','Display name as','Print on check as','Greeting','Personal Email','Preferred Email','Business Phone','Correspondence Preference','Frequency of Newsletter Reception','Language Preference','Mailing Street','Mailing City','Mailing State/Province','Mailing Zip/Postal Code','Mailing Country','Contact Reason','Committ'])

for index, row in news_quickbooks_contacts.iterrows():
    
    data = {
            'First Name': row['Full Name'],
            'Last Name':row['Full Name'],
            'Display name as':row['Full Name'],
            'Print on check as':row['Full Name'],
            'Greeting':row['Full Name'],
            'Personal Email':row['Email_x'],
            'Preferred Email':'Personal',
            'Business Phone':row['Phone Numbers'],
            'Correspondence Preference':'Email and Regular Mail',
            'Frequency of Newsletter Reception':'Monthly',
            'Language Preference':'English',
            'Mailing Street':row['Billing Address'],
            'Mailing City':row['Billing Address'],
            'Mailing State/Province':row['Billing Address'],
            'Mailing Zip/Postal Code':row['Billing Address'],
            'Mailing Country':row['Billing Address'],
            'Contact Reason':'Curent Donor',
            'Committ':'Uncommited'
        }
    df_output_csv = df_output_csv.append(data,ignore_index = True)
    
    
df_output_csv.to_csv(f'C:\\Personal\\Global80One\\data\\output\\New Donors_{timestr}.csv', encoding='utf-8', index=False,header=True)

