# Kirinify
A comfy, autumn themed music player which stores songs locally AND on the server it's hosted on, therefore it works offline. Furthermore you can modify the metadata of the music files (such as genre,artist,album name, release date, etc...). Also you can add tags to group them and modularly create playlists for example you might have a tag for My Little Pony music and another tag for high BPM songs then you can on the spot create a song queue comprised only of MLP songs that are also high BPM (or a specific genre, mood, etc).

## Features
- Comfy Autumn theme  
- Save music files to server
- List all music files 
- Actually play music files  

### Planned Features
- Modify metadata of those files (to change genre and other song details)  
- Add tags to songs  
- Add all songs with a certain tag to queue (aka create playlists)  
- Add all songs with multiple tags to queue (songs with tag1 AND tag2 only)  
- Create a music queue and allow you to select multiple songs and add to the queue  
- Create a single file archive which you can then download and copy to other places  
- Built in archive button to "delete" songs you don't like anymore (can be undone).  

<!--
- Be able to compress songs to lower quality versions  
- Built in A B testing to see if you can actually tell the difference between compressed and non compressed versions  
- Support streaming from cloud services and other websites (for example: youtube, onedrive, dropbox etc...)
-->


# Set up instructions
Backend: Flask  
Frontend: Jinja2 + HTML + CSS + JS  
<!-- Desktop: PySide6 -->

Set up commands:
```sh
git clone https://github.com/shania-codes/kirinify  
cd kirinify  
python3 -m venv venv  
source venv/bin/activate  
pip install flask  
flask run  
```
