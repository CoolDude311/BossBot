import googlesearch
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import urllib.request

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class YoutubeSearch:
    """An object that can be used to search YouTube for content.\n
    Logs in using the provided API key when the object is initialized, and remains logged in until the object is deleted."""
    def __init__(self, api_key):
        self.client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key, cache_discovery=False)
        print("YoutubeSearch initialized")
    
    def search(self, search_term, max_results, search_type=["video", "channel", "playlist"]):
        search_response = self.client.search().list(q=search_term, part="id,snippet", maxResults=max_results, type=search_type).execute()

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

    def video_search(self, search_term, max_results):
        """Search YouTube for video(s). Returns a list of YoutubeResult objects\n
        search_term: string to search for\n
        max_results: maximum number of results to add to return list"""
        return self.search(search_term, max_results, ["video"])

    def channel_search(self, search_term, max_results):
        """Search YouTube for channel(s). Returns a list of YoutubeResult objects\n
        search_term: string to search for\n
        max_results: maximum number of results to add to return list"""
        return self.search(search_term, max_results, ["channel"])

    def playlist_search(self, search_term, max_results):
        """Search YouTube for playlist(s). Returns a list of YoutubeResult objects\n
        search_term: string to search for\n
        max_results: maximum number of results to add to return list"""
        return self.search(search_term, max_results, ["playlist"])

class YoutubeResult:
    def __init__(self, title, result_type, description, result_id):
        self.title = title
        self.result_type = result_type
        self.description = description
        self.result_id = result_id
        self.url = "https://youtu.be/" + result_id

def replace_spaces(string):
    """Replace spaces with %20 to be used in API calls\n
    string: a string with spaces in it"""
    final_string = ""
    for character in string:
        if character == " ":
            final_string += "%20"
        else:
            final_string += character
    print(final_string)
    return final_string

def google_search(search_term, num_results=1):
    """Search Google for search_term and return a list of resulting URLs\n
    search_term: string to search for\n
    num_results: number of results to return"""
    results = []
    for url in googlesearch.search(search_term, start=1, stop=1+num_results, num=1):
        results.append(url)
    return results

def youtube_search(search_term, max_results, api_key, search_type="video"):
    """Searches YouTube and returns max_results in a list. Adapted from the YouTube GitHub example.\n
    search_term: string to search for\n
    max_results: number of results to return\n
    api_key: Google API key with access to YouTube Data API\n
    search_type: string with type of content (video, channel, playlist)"""
    client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key, cache_discovery=False)

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

    search_term = replace_spaces(search_term)

    #get page id
    request_id = urllib.request.Request("https://en.wikipedia.org/w/api.php?action=query&titles=%s&format=json" %search_term, headers={"User-Agent":"BossBot/v1.5"})
    request_id = json.loads(urllib.request.urlopen(request_id).read())
    page_id = list(request_id["query"]["pages"].keys())[0]

    #get actual url
    request_page = urllib.request.Request("https://en.wikipedia.org/w/api.php?action=query&prop=info&pageids=%s&inprop=url&format=json" %page_id, headers={"User-Agent":"BossBot/v1.5"})
    request_page = json.loads(urllib.request.urlopen(request_page).read())
    return request_page["query"]["pages"][str(page_id)]["fullurl"]

if __name__ == "__main__":
    client = YoutubeSearch("api_key")
    print(client.video_search("furries", 1)[0].url)
    print(client.channel_search("rebeltaxi", 1)[0].url)
    print(client.channel_search("xenu's prophet", 1)[0].url)
    print(client.playlist_search("hover revolt of gamers ost", 1)[0].url)