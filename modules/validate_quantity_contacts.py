from numpy import dtype
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
quickbooks_contacts='C:\Personal\Global80One\data\customer.xls'
df_quickbooks_contacts = pd.read_excel(quickbooks_contacts)

df_quickbooks_contacts = df_quickbooks_contacts[~df_quickbooks_contacts["Donor"].str.contains('(deleted)')]

#drop trash columns
df_quickbooks_contacts.drop(columns=['Company','Donor Type','Attachments','Currency','Open Balance','Notes','Facebook URL','Partner Number'], inplace=True)

#replace nan values
df_quickbooks_contacts.fillna('', inplace=True)

#clone column for validation
df_quickbooks_contacts['quickbooks_Donor'] = df_quickbooks_contacts['Donor']

#rename cols QUICKBOOKS DONOR == FULLNAME
df_quickbooks_contacts.rename(columns={"Donor": "Full Name"}, inplace=True)

df_quickbooks_contacts.drop(df_quickbooks_contacts[(df_quickbooks_contacts['Full Name'] =='Iglesia Experimenta Vida:Heart of Mesa Remodeling')].index, inplace=True)

#Sakesforce Contacts

#salesforce_contacts='C:\Personal\Global80One\data\Custom_Report_Contacts_2022-03-20_1336.csv'
#df_salesforce_contacts = pd.read_csv(salesforce_contacts)

path='C:\Personal\Global80One\data'

all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

df_salesforce_contacts = pd.concat(li, axis=0, ignore_index=True)


#Sakesforce Contacts

# specifying the path to csv files
path = "C:\Personal\Global80One\data"

# csv files in the path
files = glob.glob(f'{path}/*.csv')


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
#drop columns
df_salesforce_contacts.drop(columns=['Contact ID'], inplace=True)

#clone column for validation
df_salesforce_contacts['salesforce_displayname'] = df_salesforce_contacts['Display name as']

#rename cols SalesForce DisplayName == FULLNAME
df_salesforce_contacts.rename(columns={"Display name as": "Full Name"}, inplace=True)

print('Salesforce Contacts = ' + str(df_salesforce_contacts[df_salesforce_contacts.columns[0]].count()))
print('QuickBooks Contacts = ' + str(df_quickbooks_contacts[df_quickbooks_contacts.columns[0]].count()))

total_merge = df_quickbooks_contacts.merge(df_salesforce_contacts, on='Full Name', how='outer', indicator=True)

news_quickbooks_contacts= total_merge[total_merge['_merge']=='left_only']
#news_quickbooks_contacts= total_merge[total_merge['_merge']=='right_only']

print(news_quickbooks_contacts)

df_output_csv = pd.DataFrame(columns = ['First Name','Last Name','Display name as','Print on check as','Greeting','Personal Email','Preferred Email','Business Phone','Correspondence Preference','Frequency of Newsletter Reception','Language Preference','Mailing Street','Mailing City','Mailing State/Province','Mailing Zip/Postal Code','Mailing Country','Contact Reason','Committ'])

for index, row in news_quickbooks_contacts.iterrows():
    
    prefered_email="Personal"
    if not row['Email']:
        prefered_email=""


    data = {
            'First Name': row['Full Name'],
            'Last Name':row['Full Name'],
            'Display name as':row['Full Name'],
            'Print on check as':row['Full Name'],
            'Greeting':row['Full Name'],            
            'Personal Email':row['Email'],
            'Preferred Email':prefered_email,
            'Business Phone':row['Phone'],
            'Correspondence Preference':'Email and Regular Mail',
            'Frequency of Newsletter Reception':'Monthly',
            'Language Preference':'English',
            'Mailing Street':row['Street Address'],
            'Mailing City':row['City'],
            'Mailing State/Province':row['State'],
            'Mailing Zip/Postal Code':row['Zip'],
            'Mailing Country':row['Country'],
            'Contact Reason':'Current Donor',
            'Committ':'Uncommitted'
        }


    
    df_output_csv = df_output_csv.append(data,ignore_index = True)
    
    
df_output_csv.to_csv(f'C:\\Personal\\Global80One\\data\\output\\New Donors_{timestr}.csv', encoding='utf-8', index=False,header=True)

