import json, requests

def handler(event, context):
    params = event.get("queryStringParameters") or {}
    video_url = params.get("url")
    quality = params.get("quality", "480")

    if not video_url:
        return { "statusCode": 400, "body": json.dumps({"error": "Missing 'url' parameter"}) }

    api_url = "https://api.easydownloader.app/api-extract/"
    payload = { "video_url": video_url, "pagination": False, "key": "175p86550h7m5r3dsiesninx194" }

    try:
        resp = requests.post(api_url, json=payload)
        data = resp.json()
        video = data.get("final_urls", [{}])[0]
        for link in video.get("links", []):
            url = link.get("link_url", "")
            if quality in link.get("file_quality", "") and url.endswith(".mp4"):
                return { "statusCode": 302, "headers": { "Location": url }, "body": "" }

        return { "statusCode": 404, "body": json.dumps({"error": f"No .mp4 found for {quality}p"}) }

    except Exception as e:
        return { "statusCode": 500, "body": json.dumps({"error": str(e)}) }
