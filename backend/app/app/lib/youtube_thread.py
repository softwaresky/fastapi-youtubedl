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


class YdlLogger(object):

    def __init__(self):
        self.msg = {}

    def debug(self, msg):
        self.msg["debug"] = msg

    def warning(self, msg):
        self.msg["warning"] = msg

    def error(self, msg):
        self.msg["error"] = msg


class ThreadYoutubeDl(threading.Thread):

    def __init__(self, db: Session = None, ydl_object: models.YdlItem = None):
        threading.Thread.__init__(self)
        self.ydl_object = ydl_object
        self.db = db
        self.url = ydl_object.url
        self.logger = YdlLogger()
        self.dict_data = {}

        self.ydl_opts = {
            'logger': self.logger,
            'progress_hooks': [self.ydl_item_hook],
        }
        self.ydl_opts.update(ydl_object.ydl_opts)
        self.is_finished = False
        self.is_error = False

    def ydl_item_hook(self, d):

        self.dict_data.update(d)

        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    def get_data(self):
        return self.dict_data

    def run(self):

        self.is_finished = False
        self.is_error = False
        # self.dict_data["msg"] = self.logger.msg
        self.dict_data.update(self.logger.msg)

        # crud.ydl_item.update(db=self.db, db_obj=self.ydl_object, obj_in={"status": 2})
        # try:
        #     self.download_urls(url=self.url)
        # except Exception as err:
        #     crud.ydl_item.update(db=self.db, db_obj=self.ydl_object, obj_in={"status": 3})
        # crud.ydl_item.update(db=self.db, db_obj=self.ydl_object, obj_in={"status": 4})

        try:
            self.download_urls(url=self.url)
            self.is_finished = True
        except Exception as err:
            self.dict_data["err"] = f"{err}"
            self.is_error = True

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

                ydl.params["outtmpl"] = os.path.join(settings.YOUTUBE_DL_DST, pattern)

            ydl.download([url])

class ThreadManager(threading.Thread):

    def __init__(self, db: Session = None):
        threading.Thread.__init__(self)
        self.db = db
        self.dict_manager = {}

    def __del__(self):

        if self.dict_manager:
            for id_, obj_ in self.dict_manager.items():
                obj_.join()

            del self.dict_manager

    def get_object_data(self, id=0):
        if id in self.dict_manager:
            return self.dict_manager[id].get_data()
        return {}

    def get_all_objects(self):
        return [self.get_object_data(id=id_) for id_ in self.dict_manager]

    def run(self) -> None:

        while True:

            for ydl_item_ in crud.ydl_item.get_multi_by_status(db=self.db):
                if ydl_item_.status == 1:
                    if len(self.dict_manager) < settings.MAXIMUM_QUEUE:
                        if ydl_item_.id not in self.dict_manager:
                            self.dict_manager[ydl_item_.id] = ThreadYoutubeDl(ydl_object=ydl_item_)
                        if not self.dict_manager[ydl_item_.id].is_alive():
                            self.dict_manager[ydl_item_.id].start()
                            crud.ydl_item.update(db=self.db, db_obj=ydl_item_, obj_in={"status": 2})

                else:
                    if ydl_item_.id in self.dict_manager:
                        if self.dict_manager[ydl_item_.id].is_error:
                            crud.ydl_item.update(db=self.db, db_obj=ydl_item_, obj_in={"status": 3})
                        if self.dict_manager[ydl_item_.id].is_finished:
                            ydl_item_ = crud.ydl_item.update(db=self.db, db_obj=ydl_item_, obj_in={"status": 4})
                        if ydl_item_.status == 4:
                            self.dict_manager.pop(ydl_item_.id)

