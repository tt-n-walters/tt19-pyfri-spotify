import requests
import base64
import time
from pprint import pprint

secret = open(".env").read()

class WebCommunicator:
    def __init__(self, url, media_type):
        self.url = url
        self.media_type = media_type

    def download_everything(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            if self.media_type == "text":
                return response.text
            elif self.media_type == "image":
                return response.content
    

    def authenticate(self, auth):
        headers = {
            "Authorization": "Basic " + auth.encoded
        }
        data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(auth.endpoint, data=data, headers=headers)
        response = response.json()
        auth.token = response["access_token"]
        auth.token_type = response["token_type"]
        auth.time_limit = time.time() + response["expires_in"]
    

    def api(self, api, arguments):
        headers = {
            "Authorization": api.token_type + " " + api.token
        }
        response = requests.get(api.endpoint, params=arguments, headers=headers)
        return response.json()


class APIAuthentication:
    def __init__(self, endpoint, id, secret):
        self.endpoint = endpoint
        self.id = id
        self.secret = secret
    
    def _get_encoded(self):
        authorisation = self.id + ":" + self.secret
        encoded = authorisation.encode("utf-8")
        b64 = base64.b64encode(encoded).decode("utf-8")
        print(b64)
        return b64
    

    def _get_token(self):
        current = time.time()
        if current > self.time_limit:
            input("Token expired. Please restart the program.")
            exit()
        else:
            return self._token


    def _set_token(self, token):
        self._token = token
    
    encoded = property(_get_encoded)
    token = property(_get_token, _set_token)



class Spotify:
    def __init__(self, web_comminicator, api):
        self.web_comminicator = web_comminicator
        self.api = api
    
    def search_artist(self, artist):
        self.api.endpoint = "https://api.spotify.com/v1/search"
        arguments = {
            "q": artist,
            "type": "artist"
        }
        response = self.web_comminicator.api(self.api, arguments)

        items = response["artists"]["items"]
        custom_response = []
        for item in items:
            custom_response.append({
                "name": item["name"],
                "link": item["external_urls"]["spotify"]
            })
        return custom_response
    
    def search_track(self, track):
        self.api.endpoint = "https://api.spotify.com/v1/search"
        arguments = {
            "q": track,
            "type": "track"
        }
        response = self.web_comminicator.api(self.api, arguments)
        print(response)
        items = response["tracks"]["items"]
        custom_response = []
        for item in items:
            custom_response.append({
                "name": item["name"],
                "link": item["external_urls"]["spotify"]
            })
        return custom_response



if __name__ == "__main__":

    communicator = WebCommunicator("https://httpbin.org/", "text")

    spotify_api = APIAuthentication(
        "https://accounts.spotify.com/api/token",
        "f5df0d5cf24d49a59daafcb0156d79a6",
        secret)

    communicator.authenticate(spotify_api)

    spotify = Spotify(communicator, spotify_api)
    for result in spotify.search_track("Don't stop me now"):
        print(result)

    
    