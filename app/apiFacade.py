import googleapiclient.discovery

class YoutubeHelper:
    _api_service_name = "youtube"
    _api_version = "v3"

    def __init__(self, key):
        self.auth_key = key

    def get_client(self):
        self.youtube = googleapiclient.discovery.build(
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
        # Request execution
        response = request.execute()
        return response