import requests
import os
import json
from dotenv import load_dotenv
from pathlib import Path

# Load API secrets from .env file
load_dotenv()

def download_data(access_token, out_file):
    url = 'https://api.ouraring.com/v2/usercollection/sleep' 
    params={ 
        'start_date': '2021-11-01', 
        'end_date': '2024-12-01' 
    }
    headers = { 
        'Authorization': f'Bearer {access_token}' 
    }

    response = requests.request('GET', url, headers=headers, params=params) 

    if response.status_code == 200:
        data = response.json()

        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, 'w') as f:
            f.write(json.dumps(data['data'], indent=4))
        print(f"Downloaded data successfully!")
        
    else:
        print('Failed to download data with {response.status_code}')

def main():
    access_token = os.getenv('API_KEY')
    download_data(access_token, Path('data/interim/sleep_data.json'))

if __name__ == '__main__':
    main()