'''
import yt_dlp
import os
from pathlib import Path

path = Path('I:\\Movies')

def download_youtube_videos(url, output_path=path):

#	if os.path.exists(path) and os.path.isdir(path):
#		print("folder exist")
#	else:
#		print("folder not found")

	
	try:
		if not os.path.exists(output_path):
			os.makedirs(output_path)

		ydl_opts = {
			'format': 'best',
			'outtmpl': f'{output_path}/%(title)s.%(ext)s',
			'noplaylist': True,
		}

		print(f'Attending to Download: {url}')
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])
		print(f'Download Completed! video saved to {output_path}')

	except yt_dlp.utils.DownloadError as de:
		print(f'Download error: {str(de)}')
		print('\nListing available formats...')

		try:
			with yt_dlp.YoutubeDL({'listformats': True}) as ydl:
				ydl.download([url])
		except Exception as e:
			print(f'failed to list formats: {str(e)}')

	except Exception as e:
		print(f'An error occured: {str(e)}')
		


if __name__ == "__main__":
	video_url = input("Enter the URL: ")
	download_youtube_videos(video_url)
'''

import yt_dlp
import os
from pathlib import Path

# Change download path to local laptop folder
LOCAL_DOWNLOAD_PATH = Path.home() / "Videos" / "Downloaded"
ARCHIVE_FILE = LOCAL_DOWNLOAD_PATH / "downloaded.txt"

CHANNELS = [
    "https://www.youtube.com/@BeastBoyShub/videos",
    "https://www.youtube.com/@BeastBoyShub/videos",
    "https://www.youtube.com/@visa2explore/videos"
]

def download_from_channels():
    LOCAL_DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'format': 'best',
        'outtmpl': str(LOCAL_DOWNLOAD_PATH / '%(uploader)s/%(title)s.%(ext)s'),
        'download_archive': str(ARCHIVE_FILE),
        'ignoreerrors': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(CHANNELS)

if __name__ == "__main__":
    download_from_channels()