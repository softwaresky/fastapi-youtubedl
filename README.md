# fastapi-youtubedl

Web application for downloading video/audio from [YouTube](https://youtube.com)

## Quick Guide
![quick-guide](./imgs/all-in-one.gif)

## Instruction
### Docker
For build and run this application please following this commands

1. Building image: ```docker build -t fastapi-youtubedl-vue .```
2. Run container: ```docker run -d --name fastapi-youtubedl-vue --env-file .env -e MAX_WORKERS=2 -e PORT=6696 -p 6696:6696 -v C:/youtube-dl:/youtube-dl  fastapi-youtubedl-vue```
3. Go to [http://localhost:6696](http://localhost:6696) 
or look at the address to your **fastapi-youtubedl-vue** container

This is default arguments, you can change these docker arguments.