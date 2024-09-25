import music_tag
from io import BytesIO

f = music_tag.load_file("/home/doug/Music/Intan Kadewie/Ayun - Ayun Gobyog/Intan Kadewie_Ayun - Ayun Gobyog_01_Ayun - Ayun Gobyog (feat. Anisa Salma).mp3")

art = f['artwork']

print(art.first.mime)  # -> 'image/jpeg'
print(art.first.width) # -> 1280
print(art.first.height)  # -> 1280
print(art.first.depth)  # -> 24
print(type(art.first.data))  # -> b'... raw image data ...'

buf = BytesIO(art.first.data)

print(type(buf))

