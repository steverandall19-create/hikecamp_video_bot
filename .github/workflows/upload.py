import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_video():
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")
    
    # Updated defaults for HikeCamp
    title = os.environ.get("VIDEO_TITLE", "UK Trail & Camping Guide")
    description = os.environ.get("VIDEO_DESCRIPTION", "Explore this amazing UK outdoor destination!")
    
    # Clean standard title
    full_title = title
    
    # Updated hashtags for HikeCamp
    full_description = f"{description}\n\n#HikeCamp #UKHiking #WildCamping #GlampingUK #GetOutside"

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token"
    )

    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": full_title[:100], 
            "description": full_description[:5000],
            # Updated SEO tags for the new site
            "tags": ["HikeCamp", "UK Hiking", "Camping UK", "Outdoors", "Glamping"],
            "categoryId": "19" # Category 19 is Travel & Events
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload("output.mp4", chunksize=-1, resumable=True)

    print("Uploading main video to YouTube...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    print(f"Upload complete! Video ID: {response.get('id')}")

if __name__ == "__main__":
    upload_video()
