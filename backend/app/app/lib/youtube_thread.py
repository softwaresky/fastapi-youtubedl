import os
import threading
import youtube_dl
import pprint
import json
import time
from app.core.config import settings
from app import models, crud, schemas
import logging
import datetime

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

    def __init__(self, ydl_object: models.YdlItem = None):
        threading.Thread.__init__(self)

        self.ydl_object = ydl_object
        self.logger = YdlLogger()
        self.dict_data = {}
        self.extra_info = {}
        self.prepare_filename = ""
        self.dt_hook_last_call = datetime.datetime.now()

        self.ydl_opts = {
            'logger': self.logger,
            'progress_hooks': [self.ydl_item_hook],
        }
        self.ydl_opts.update(ydl_object.ydl_opts)
        self.is_running = False
        self.status = 1

    # def __del__(self):
    #     logger.info(f"{self.name}: __del__ => {self.is_alive()}")
    #     self.join()

    def ydl_item_hook(self, d):

        self.dict_data.update(d)
        self.dt_hook_last_call = datetime.datetime.now()


        # if d['status'] == 'finished':
            # print('Done downloading, now converting ...')
            # logger.info('Done downloading, now converting ...')

    def can_remove(self):
        return datetime.datetime.now() > self.dt_hook_last_call + datetime.timedelta(seconds=3)

    def get_data(self):
        return self.dict_data

    def run(self):

        self.is_running = True
        self.status = 2

        self.dict_data.update(self.logger.msg)

        try:
            self.download_urls(url=self.ydl_object.url, do_calculate_pattern=self.ydl_object.do_calculate_pattern)
            self.is_running = False
            self.status = 4

        except Exception as err:
            self.dict_data["err"] = f"{err}"
            self.is_running = False
            self.status = 3

        if self.dict_data.get("error"):
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

            self.extra_info = ydl.extract_info(url, download=False)
            self.prepare_filename = ydl.prepare_filename(self.extra_info)

            ydl.download([url])


class ThreadManager(threading.Thread):

    def __init__(self, db_conn = None):
        threading.Thread.__init__(self)

        self.daemon = True
        self.dict_manager = {}
        self.db_conn = db_conn


    def __del__(self):

        if self.dict_manager:
            for id_, obj_ in self.dict_manager.items():
                obj_.join()

            del self.dict_manager

        self.join()

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
            logger.info(f"remove_object => [{self.dict_manager[object_id]}] {self.dict_manager[object_id].is_alive()}")

            self.dict_manager[object_id].join()
            del self.dict_manager[object_id]
            logger.info(f"Removed: [{object_id}]")

    def run(self) -> None:

        while True:

            if not self.db_conn:
                continue

            with self.db_conn() as db:
                for ydl_item_ in crud.ydl_item.get_multi_by_status(db=db):
                    dict_update = {}

                    if ydl_item_.status == 1:
                        if len(self.dict_manager) <= settings.MAXIMUM_QUEUE:
                            if ydl_item_.id not in self.dict_manager:
                                self.dict_manager[ydl_item_.id] = ThreadYoutubeDl(ydl_object=ydl_item_)
                                self.dict_manager[ydl_item_.id].deamon = True
                                self.dict_manager[ydl_item_.id].start()
                                logger.info(f"Created: [{ydl_item_.id}] {self.dict_manager[ydl_item_.id]} -> is_alive: {self.dict_manager[ydl_item_.id].is_alive()}")
                                dict_update["status"] = 2
                                dict_update["output_log"] = self.get_object_data(id=ydl_item_.id)
                        else:
                            logger.info(f"Queue is full. {len(self.dict_manager)} / {settings.MAXIMUM_QUEUE}")

                    thread_obj_ = self.dict_manager.get(ydl_item_.id)
                    if thread_obj_ and not thread_obj_.is_running:
                        dict_update["status"] = thread_obj_.status
                        dict_update["output_log"] = thread_obj_.get_data()
                        # logger.info(f"prepare_filename: {thread_obj_.prepare_filename}")
                        # logger.info(f"ext: {thread_obj_.extra_info.get('ext')}")

                    if dict_update:
                        ydl_item_ = crud.ydl_item.update(db=db, db_obj=ydl_item_, obj_in=dict_update)
                        logger.info(f"Updated: [{ydl_item_.id}] => {dict_update}")

                    if thread_obj_ and ydl_item_.status == 4:
                        if thread_obj_.can_remove():
                            self.remove_object(ydl_item_.id)

            time.sleep(0.5)

def get_url_info(url="", ydl_opts={}):

    if url:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                dict_info = ydl.extract_info(url, download=False)

                lst_format_sorted = sorted(dict_info.get("formats", []), key=lambda item: (item["height"] if item.get("height") else 0,
                                                                                           item["quality"] if item.get("quality") else 0,
                                                                                           item["fps"] if item.get("fps")else 0,
                                                                                           item["vbr"] if item.get("vbr") else 0,
                                                                                           item["tbr"] if item.get("tbr") else 0))


                lst_audio_formats = [format_ for format_ in lst_format_sorted if format_.get('vcodec') == 'none']
                lst_video_formats = [format_ for format_ in lst_format_sorted if format_.get('vcodec') != 'none']
                dict_info["formats"] = lst_format_sorted
                dict_info["best_audio_format"] = lst_audio_formats[-1] if lst_audio_formats else {}
                dict_info["best_video_format"] = lst_video_formats[-1] if lst_video_formats else {}
                dict_info["prepare_filename"] = os.path.join(settings.YOUTUBE_DL_DST, ydl.prepare_filename(dict_info))
                return dict_info
            except Exception as err:
                logger.error(f"{err}")

    return {}