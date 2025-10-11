import os, requests, xmltodict

API_KEY = os.getenv("YT_API_KEY")
CHANNEL_FILE = "data/spor.txt"
XML_PATH = "xml/spor.xml"

def read_channels(path):
    ids = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                ids.append(line.split()[0])
    return ids

def get_live_videos(channel_id):
    url = (
        f"https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"
    )
    r = requests.get(url)
    data = r.json()
    results = []
    for item in data.get("items", []):
        vid = item["id"]["videoId"]
        title = item["snippet"]["title"]
        thumb = item["snippet"]["thumbnails"]["high"]["url"]
        results.append({
            "title": title,
            "thumb": thumb,
            "type": "youtube",
            "src": vid
        })
    return results

def main():
    channels = read_channels(CHANNEL_FILE)
    media_items = []
    for cid in channels:
        media_items += get_live_videos(cid.strip())

    xml_data = {"media": {"media": media_items}}
    xml_str = xmltodict.unparse(xml_data, pretty=True)

    os.makedirs(os.path.dirname(XML_PATH), exist_ok=True)
    with open(XML_PATH, "w", encoding="utf-8") as f:
        f.write(xml_str)

if __name__ == "__main__":
    main()
