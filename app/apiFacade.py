import googleapiclient.discovery
import json

class YoutubeHelper:
    _api_service_name = "youtube"
    _api_version = "v3"

    def __init__(self, key):
        self.auth_key = key
        self.youtube = googleapiclient.discovery.build(\
            self._api_service_name, self._api_version, developerKey = self.auth_key)

    def search(self):
        request = self.youtube.search().list(
            part="id,snippet",
            type='video',
            q="Spider-Man",
            videoDuration='short',
            videoDefinition='high',
            maxResults=1
        )

        response = request.execute()
        return response
    
    def get_video_details(self, ids):
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=ids
        )
        response = request.execute()
        return response
    
        # TODO: just testing code, this should output response
        with open("sample.json", "w") as outfile:
            json.dump(response, outfile)

    def get_video_category(self, region):
        request = self.youtube.videoCategories().list(
            part="snippet",
            regionCode=region
        )
        response = request.execute()
        return response

# TODO: just for testing
if __name__ == "__main__":
    yth = YoutubeHelper("<API_KEY>")
    # yth.get_video_details("b5EoidxBSTE,KIhKho9ZYiQ,W6mRkmbn7Kk,N-etpkOVBMM,E_KbZOJp7Vw,zzs9uoTy3pg")
    # print(yth.get_video_category("US"))
