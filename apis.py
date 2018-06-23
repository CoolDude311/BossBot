import google
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import urllib.request

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class YoutubeResult:
    def __init__(self, title, result_type, description, result_id):
        self.title = title
        self.result_type = result_type
        self.description = description
        self.result_id = result_id
        self.url = "https://youtu.be/" + result_id

def google_search(search_term, num_results=1):
    """Search Google for search_term and return a list of resulting URLs\n
    search_term: string to search for\n
    num_results: number of results to return"""
    results = []
    for url in google.search(search_term, start=1, stop=1+num_results, num=1):
        results.append(url)
    return results

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

def wikipedia_search(search_term):
    """Search Wikipedia for term and return the first hit. If no matches, return -1\n
    search_term: string to search for"""

    #get page id
    request_id = urllib.request.Request("https://en.wikipedia.org/w/api.php?action=query&titles=%s&format=json" %search_term, headers={"User-Agent":"BossBot/v1.5"})
    request_id = json.loads(urllib.request.urlopen(request_id).read())
    page_id = list(request_id["query"]["pages"].keys())[0]

    #get actual url
    request_page = urllib.request.Request("https://en.wikipedia.org/w/api.php?action=query&prop=info&pageids=%s&inprop=url&format=json" %page_id, headers={"User-Agent":"BossBot/v1.5"})
    request_page = json.loads(urllib.request.urlopen(request_page).read())
    return request_page["query"]["pages"][str(page_id)]["fullurl"]

if __name__ == "__main__":
    print(wikipedia_search("xenon"))