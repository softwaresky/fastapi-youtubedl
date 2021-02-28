import os
import threading
import youtube_dl
import pprint
import json
import time
from app.core.config import settings
from app import models, crud, schemas
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("youtube_thread")


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
        self.logger = YdlLogger()
        self.dict_data = {}

        self.ydl_opts = {
            'logger': self.logger,
            'progress_hooks': [self.ydl_item_hook],
        }
        self.ydl_opts.update(ydl_object.ydl_opts)
        # self.is_finished = False
        # self.is_error = False

        self.is_running = False
        self.status = 1

    def ydl_item_hook(self, d):

        self.dict_data.update(d)

        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    def get_data(self):
        return self.dict_data

    def run(self):

        self.is_running = True
        self.status = 2

        # self.is_finished = False
        # self.is_error = False
        # self.dict_data["msg"] = self.logger.msg
        self.dict_data.update(self.logger.msg)

        try:
            self.download_urls(url=self.ydl_object.url, do_calculate_pattern=self.ydl_object.do_calculate_pattern)
            # self.is_finished = True

            self.is_running = False
            self.status = 4

        except Exception as err:
            self.dict_data["err"] = f"{err}"
            # self.is_error = True

            self.is_running = False
            self.status = 3

    def download_urls(self, url: str = "", do_calculate_pattern: bool = False):

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            if "outtmpl" not in self.ydl_opts:
                pattern = "%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"

                if do_calculate_pattern:
                    info = ydl.extract_info(url, download=False)
                    if info.get("_type") == "playlist":
                        pattern = "%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"

                        for dict_entry_ in info.get("entries", []):

                            if [dict_entry_.get(key_) for key_ in ["series", "season_number", "episode_number"] if dict_entry_.get(key_)]:
                                pattern = "%(series)s/%(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s"
                                break

                            if [dict_entry_.get(key_) for key_ in ["chapters"] if dict_entry_.get(key_)]:
                                pattern = "%(playlist)s/%(chapter_number)s - %(chapter)s/%(title)s.%(ext)s"
                                break

                ydl.params["outtmpl"] = os.path.abspath(os.path.join(settings.YOUTUBE_DL_DST, pattern))

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

    def stop_thread_by_id(self, item_id=0):

        thread_item = self.dict_manager.get(item_id)
        if thread_item:

            if thread_item.is_alive():
                thread_item.join()

            logger.info(f"Stop: [{item_id}] {thread_item} -> {thread_item.is_alive()}")
            return thread_item.is_alive()

    def get_all_thread_info(self):

        dict_result = {}

        for id_, thread_ in self.dict_manager.items():
            dict_result[id_] = {"thread": f"{thread_}", "is_alive": thread_.is_alive()}

        return dict_result

    def remove_object(self, object_id=0):
        if object_id in self.dict_manager:
            self.dict_manager.pop(object_id)

    def run(self) -> None:

        while True:

            for ydl_item_ in crud.ydl_item.get_multi_by_status(db=self.db):
                dict_update = {}

                if ydl_item_.status == 1:
                    if len(self.dict_manager) < settings.MAXIMUM_QUEUE:
                        if ydl_item_.id not in self.dict_manager:
                            self.dict_manager[ydl_item_.id] = ThreadYoutubeDl(ydl_object=ydl_item_)
                            logger.info(f"Created: [{ydl_item_.id}] {self.dict_manager[ydl_item_.id]}")
                        if not self.dict_manager[ydl_item_.id].is_alive():
                            self.dict_manager[ydl_item_.id].start()
                            logger.info(f"Start: [{ydl_item_.id}] {self.dict_manager[ydl_item_.id]} -> {self.dict_manager[ydl_item_.id].is_alive()}")
                            dict_update["status"] = 2
                            dict_update["output_log"] = self.get_object_data(id=ydl_item_.id)
                            # crud.ydl_item.update(db=self.db, db_obj=ydl_item_, obj_in={"status": 2, "output_log": self.get_object_data(id=ydl_item_.id)})
                    else:
                        logger.info(f"Queue is full. {len(self.dict_manager)}")
                # else:
                thread_obj_ = self.dict_manager.get(ydl_item_.id)
                if thread_obj_ and not thread_obj_.is_running:
                    dict_update["status"] = thread_obj_.status
                    dict_update["output_log"] = thread_obj_.get_data()

                    if thread_obj_.status == 4:
                        removed_thread = self.dict_manager.pop(ydl_item_.id)
                        logger.info(f"Removed: [{ydl_item_.id}] {removed_thread}")

                # if ydl_item_.id in self.dict_manager:
                #     if not self.dict_manager[ydl_item_.id].is_running or ydl_item_.status != self.dict_manager[ydl_item_.id].status:
                #         dict_update["status"] = self.dict_manager[ydl_item_.id].status
                #         dict_update["output_log"] = self.dict_manager[ydl_item_.id].get_data()
                #
                #         # if self.dict_manager[ydl_item_.id].is_error:
                #         #     dict_update["status"] = 3
                #         #     dict_update["output_log"] = self.get_object_data(id=ydl_item_.id)
                #         #     # crud.ydl_item.update(db=self.db, db_obj=ydl_item_, obj_in={"status": 3})
                #         # if self.dict_manager[ydl_item_.id].is_finished:
                #         #     dict_update["status"] = 4
                #         #     dict_update["output_log"] = self.get_object_data(id=ydl_item_.id)
                #         #     # ydl_item_ = crud.ydl_item.update(db=self.db, db_obj=ydl_item_, obj_in={"status": 4})
                #         # # if ydl_item_.status == 4:
                #         # #     self.dict_manager.pop(ydl_item_.id)

                if dict_update:
                    crud.ydl_item.update(db=self.db, db_obj=ydl_item_, obj_in=dict_update)

def get_url_info(url="", ydl_opts={}):

    if url:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                dict_info = ydl.extract_info(url, download=False)
                lst_audio_formats = [format_ for format_ in dict_info.get("formats", []) if format_.get('vcodec') == 'none']
                lst_video_formats = [format_ for format_ in dict_info.get("formats", []) if format_.get('vcodec') != 'none']
                dict_info["best_audio_format"] = lst_audio_formats[-1] if lst_audio_formats else {}
                dict_info["best_video_format"] = lst_video_formats[-1] if lst_video_formats else {}
                dict_info["prepare_filename"] = os.path.join(settings.YOUTUBE_DL_DST, ydl.prepare_filename(dict_info))
                return dict_info
            except:
                pass

    return {}