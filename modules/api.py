import requests
import json

url = "https://fa-synapseanalytics-qa.azurewebsites.net/api/ActivoDigitalHome?code=/X29yWB8oQYBTAwskjc6hr5I/ZSj9B3bXd7tBrilcogHXywrWxhEng%3D%3D&userID=10306617"



response = requests.get(url)

print(response.text)
