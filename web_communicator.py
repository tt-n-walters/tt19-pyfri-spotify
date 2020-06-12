import requests


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


class APIAuthentication:
    def __init__(self, endpoint, id, secret):
        self.endpoint = endpoint
        self.id = id
        self.secret = secret


if __name__ == "__main__":

    http_test = WebCommunicator("https://httpbin.org/", "text")
    # print(http_test.download_everything())

    spotify = APIAuthentication(
        "https://api.spotify.com/v1/search?q=levels&type=album",
        "f5df0d5cf24d49a59daafcb0156d79a6",
        "45a8c35e9b96490b875def5288a6ebac")

    http_test.authenticate(spotify)
    