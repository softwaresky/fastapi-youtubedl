import os
import threading
import youtube_dl
import pprint
import json
import time
from app.core.config import settings
from app import models, crud, schemas
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

YOUTUBE_DL_DST = settings.YOUTUBE_DL_DST


class MyLogger(object):

    def __init__(self):
        self.msg = ""

    def debug(self, msg):
        self.msg = msg

    def warning(self, msg):
        self.msg = msg

    def error(self, msg):
        self.msg = msg

"""
            # crud.ydl_item.update(db=db, db_obj=item, obj_in=item_in)
            db_obj = crud.ydl_item.get(self.db, id_)
            obj_in = {'status': 4}
            item = crud.ydl_item.update(self.db, db_obj=db_obj, obj_in=obj_in)
            print ("Updated")
            pprint.pprint(jsonable_encoder(item))
"""

class ThreadYoutubeDl(threading.Thread):

    def __init__(self, url="", ydl_opts={}):
        threading.Thread.__init__(self)
        self.url = url
        self.logger = MyLogger()
        self.dict_data = {}
        self.is_finished = False


        self.ydl_opts = {
            'logger': self.logger,
            'progress_hooks': [self.my_hook],
        }
        self.ydl_opts.update(ydl_opts)

    def my_hook(self, d):

        self.dict_data.update(d)

        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    def get_data(self):
        return self.dict_data

    def run(self):

        self.dict_data["msg"] = self.logger.msg
        self.is_finished = False
        self.download_urls(url=self.url)
        self.is_finished = True

    def download_urls(self, url: str = "", do_calculate_pattern: bool = False):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:

            if "outtmpl" not in self.ydl_opts:
                pattern = "%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"

                if do_calculate_pattern:
                    info = ydl.extract_info(url, download=False)
                    if info.get("_type") == "playlist":
                        pattern = "%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"

                        for dict_entry_ in info.get("entries", []):

                            if [dict_entry_.get(key_) for key_ in ["series", "season_number", "episode_number"] if
                                dict_entry_.get(key_)]:
                                pattern = "%(series)s/%(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s"
                                break

                            if [dict_entry_.get(key_) for key_ in ["chapters"] if dict_entry_.get(key_)]:
                                pattern = "%(playlist)s/%(chapter_number)s - %(chapter)s/%(title)s.%(ext)s"
                                break

                ydl.params["outtmpl"] = os.path.join(YOUTUBE_DL_DST, pattern)

            ydl.download([url])

class ThreadManager(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.dict_manager = {}


    def __del__(self):

        if self.dict_manager:
            for id_, obj_ in self.dict_manager.items():
                obj_.join()

            del self.dict_manager

    def add_object(self, id=0, url=""):

        if url and id:
            if id not in self.dict_manager:
                self.dict_manager[id] = ThreadYoutubeDl(url=url)

    def remove_object(self, id=0):
        if id:
            self.dict_manager.pop(id)

    def get_object_data(self, id=0):
        if id in self.dict_manager:
            return self.dict_manager[id].get_data()
        return {}

    def get_all_objects(self):
        return [self.get_object_data(id=id_) for id_ in self.dict_manager]

    def clear_finished(self):


        lst_finished = []
        try:
            lst_finished = [k for k in self.dict_manager if self.dict_manager[k].is_finished]
        except:
            pass
        for id_ in lst_finished:
            popped_id = self.dict_manager.pop(id_)
            print(f"popped_id: {popped_id}")


    def run(self) -> None:

        while True:

            self.clear_finished()
            lst_id = list(self.dict_manager.keys())
            for id_ in lst_id:
                if not self.dict_manager[id_].is_alive():
                    self.dict_manager[id_].start()


# def main():
#     url = 'https://www.youtube.com/playlist?list=PLTcx_OTDaQdUZq-hYF8qhEN8rNwOTZw__'
#
#
#     t_manager = ThreadManager()
#     t_manager.start()
#
#     t_manager.add_object(1, url)
#
# main()
