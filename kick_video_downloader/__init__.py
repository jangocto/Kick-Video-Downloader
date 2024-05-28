import re, subprocess
import cloudscraper


API_URL = "https://kick.com/api/v1/video/"

def download_video(url, output_path=None) -> bool:
    
    VIDEO_ID_PATTERN = re.compile(r'https://kick.com/video/([a-zA-Z0-9]{8}\-[a-zA-Z0-9]{4}\-[a-zA-Z0-9]{4}\-[a-zA-Z0-9]{4}\-[a-zA-Z0-9]{12})')

    video_id = VIDEO_ID_PATTERN.match(url).group(1)

    video_url = f"{API_URL}{video_id}"

    print(f"Downloading video from {video_url} to {output_path}")

    scraper = cloudscraper.create_scraper()
    res = scraper.get(video_url)

    if res.status_code != 200:
        print("Failed to get video info")
        return False

    video_info = res.json()

    source_url = video_info['source']
    created_at = video_info['livestream']['created_at'].replace(':', '_')
    title = video_info['livestream']['session_title']

    if output_path is None:
        output_path = f"{title} - {created_at}.mp4"

    print(f"Downloading video from {source_url} to {output_path}")
    input("Press Enter to continue...")

    try:
        subprocess.run(["ffmpeg", "-i", source_url, "-vcodec", "copy", "-acodec", "copy", output_path])

    except Exception as e:
        print(f"Failed to download video: {e}")
        return False
    
    return True