import requests
import base64
import json

def get_spotify_token():
    # Spotify API credentials
    client_id = "79739c5371df43a4b955af5f24560590"
    client_secret = "84f4caa9d1154f0696a3290fca96438e"
    
    # Encode credentials in base64
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    # Request headers
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Request body
    data = {
        'grant_type': 'client_credentials'
    }
    
    try:
        # Make request to Spotify token endpoint
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers=headers,
            data=data
        )
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access_token']
            print(f"✅ Spotify token obtained successfully!")
            print(f"Token: {access_token}")
            return access_token
        else:
            print(f"❌ Failed to get token. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting Spotify token: {str(e)}")
        return None

# Execute the function
if __name__ == "__main__":
    get_spotify_token()

