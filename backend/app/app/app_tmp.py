from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Any, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.requests import  Request
from fastapi.responses import StreamingResponse, HTMLResponse
import pprint
import time
import json
from lib.youtube_thread import ThreadManager

youtube_manager_main = ThreadManager()
time.sleep(1)
youtube_manager_main.start()

app = FastAPI()

class YoutubeDL(BaseModel):
    url: str
    ydl_opts: Optional[dict] = None


class YoutubeDLIn(BaseModel):
    id: int
    url: str
    ydl_opts: Optional[dict] = None


def auto_fill():
    youtube_manager_main.add_object(id=1, url="https://www.youtube.com/playlist?list=PLTcx_OTDaQdUZq-hYF8qhEN8rNwOTZw__")

html = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <script src="https://code.jquery.com/jquery-3.0.0.js"></script>
        <title>My Project</title>
    </head>
    <body>
        <h1>WebSocket Stream</h1>
        <div id="div_stream" >
        
        </div>
        <ul id='messages'>
        </ul>
        <script>
            const source = new EventSource("/stream/1");
            source.onmessage = function (event) {
                const data = JSON.parse(event.data);
            
                // var messages = document.getElementById('messages')
                // var message = document.createElement('li')
                // var content = document.createTextNode(JSON.stringify(data))
                // message.appendChild(content)
                // messages.appendChild(message)
        
                $("#div_stream").html(JSON.stringify(data));
            };
            
        </script>
    </body>
</html>
"""

@app.get("/")
async def index():
    auto_fill()
    return HTMLResponse(html)

@app.get("/{id}")
def read_youtube_dl(
        id: int,
) -> Any:
    dict_data = youtube_manager_main.get_object_data(id=id)

    return dict_data

@app.get("/stream/{id}")
def stream_youtube_dl(
        id: int,
) -> Any:

    def _generate_data():
        while True:
            dict_data = youtube_manager_main.get_object_data(id=id)
            yield f"data: {json.dumps(dict_data)}\n\n"
            time.sleep(1)

    return StreamingResponse(_generate_data(), media_type='text/event-stream')

@app.post("/")
def create_youtube_dl(youtube_dl_in: YoutubeDLIn) -> Any:
    youtube_manager_main.add_object(id=youtube_dl_in.id, url=youtube_dl_in.url)
    return youtube_dl_in.dict()



# def main():
#     import uvicorn
#     uvicorn.run(app, port=5678)
#     pass
#
#
# if __name__ == '__main__':
#     main()
