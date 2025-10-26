# Kirinify
A comfy, autumn themed music player ~~which stores songs locally AND on the server it's hosted on, therefore it works offline. Furthermore you can modify the metadata of the music files (such as genre,artist,album name, release date, etc...).~~ Also you can add tags to group them, ~~and modularly create playlists~~ for example you might have a tag for My Little Pony music and another tag for fast-paced songs then you can on the spot create a song ~~queue~~ list comprised only of MLP songs that are also fast-paced (or a specific genre, mood, etc tags are fully customisable).
No queue is not a bug it's a feature actually, it's MINDFUL COMPUTING you have to pick each song to listen to one at a time and will be present while listening to them. 

## Features
- Forget NodeJS, this project uses No JS  
- Comfy Autumn theme  
- Save music files to server if they don't already exist  
- List all music files  
- Actually play music files  
- Save song details to DB  
- Save added tags to DB  
- Delete songs  
- Display and delete all tags  
- Filter songs by tags using an OR mode or ALL mode in which it must have either any of the tags or all of the tags 
- .zip file download of all files  
- Download individual songs   

### Planned Features
- Visible name different from file name  
- Rename songs  
- Pagination or Infinite Scroll  
- Search for songs by name  
- Filter songs by name AND tags  
- Store upload date, file size, and duration  
- Sort/Filter by upload date, file size, and duration  
- Delete all songs with a certain tag  
- Frontend.  
- Make tags not be case sensitive

- Built in archive button to "delete" songs you don't like anymore (can be undone).  
- Modify metadata of those files (to change genre and other song details)  
- Be able to compress songs to lower quality versions  
- Built in A B testing to see if you can actually tell the difference between compressed and non compressed versions  
- Support streaming from cloud services and other websites (for example: youtube, onedrive, dropbox etc...)

<!--
Require JS, implement as Userscript in Violentmonkey?
- Create a music queue and allow you to select multiple songs and add to the queue  
- Add all songs with a certain tag to queue (aka create playlists)  
- Add all songs with multiple tags to queue (songs with tag1 AND tag2 only)  
-->

# Set up instructions
```sh
git clone https://github.com/shania-codes/kirinify  
cd kirinify  
python3 -m venv venv  
source venv/bin/activate  
pip install flask  
flask run  
```
