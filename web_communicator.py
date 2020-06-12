import requests
import base64

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
        auth.token = response["token"]
        auth.token_type = response["token_type"]
    

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
    
    encoded = property(_get_encoded)


if __name__ == "__main__":

    http_test = WebCommunicator("https://httpbin.org/", "text")
    # print(http_test.download_everything())

    spotify = APIAuthentication(
        "https://accounts.spotify.com/api/token",
        "f5df0d5cf24d49a59daafcb0156d79a6",
        secret)

    http_test.authenticate(spotify)
    
    