import youtube_dl
import os
import pprint

url = "https://www.youtube.com/watch?v=bZ_BoOlAXyk&list=RDbZ_BoOlAXyk&start_radio=1"

class YdlLogger(object):

    def __init__(self):
        self.msg = {}

    def debug(self, msg):
        self.msg["debug"] = msg

    def warning(self, msg):
        self.msg["warning"] = msg

    def error(self, msg):
        self.msg["error"] = msg

ydl_logger = YdlLogger()

def ydl_item_hook(d):
    # pprint.pprint(d)
    # print (d.get("status"))
    if d:
        _percent_str = d.get("_percent_str")
        status = d.get("status")
        print (f"[{_percent_str}] {status}")

ydl_opts = {
    # "format": "bestaudio/best",
    # "postprocessors": [{
    #       'key': 'FFmpegExtractAudio',
    #       'preferredcodec': 'mp3',
    #       'preferredquality': '192',
    #     }],
    'logger': ydl_logger,
    'progress_hooks': [ydl_item_hook],
    "noplaylist": True
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    pattern = "%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"
    ydl.params["outtmpl"] = os.path.abspath(os.path.join(r"E:\docker_volume\youtube-dl", pattern))
    ydl.download([url])