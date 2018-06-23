from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class YoutubeResult:
    def __init__(self, title, result_type, description, result_id):
        self.title = title
        self.result_type = result_type
        self.description = description
        self.result_id = result_id
        self.url = "https://youtu.be/" + result_id

def youtube_search(search_term, max_results, api_key, search_type="video"):
    """Searches YouTube and returns max_results in a list. Adapted from the YouTube GitHub example.\n
    search_term: string to search for\n
    max_results: number of results to return\n
    api_key: Google API key with access to YouTube Data API\n
    search_type: string with type of content (video, channel, playlist)"""
    client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)

    search_response = client.search().list(q=search_term, part="id,snippet", maxResults=max_results, type=search_type).execute()

    results = []
    for result in search_response.get("items", []):
        title = result["snippet"]["title"]
        result_type = result["id"]["kind"].replace("youtube#", "")
        description = result["snippet"]["description"]
        if result_type == "video":
            result_id = result["id"]["videoId"]
        elif result_type == "channel":
            result_id = result["id"]["channelId"]
        elif result_type == "playlist":
            result_id = result["id"]["playlistId"]
        results.append(YoutubeResult(title, result_type, description, result_id))

    return results

if __name__ == "__main__":
    results = youtube_search("furries", 10, "api_key")
    for result in results:
        print("%s, %s, %s, %s, %s\n" %(result.title, result.result_type, result.description, result.result_id, result.url))