# YouTube Music Browser Authentication Setup for piPod

This procedure creates the `browser.json` file used by `ytmusicapi`.

## 1. Get an authenticated YouTube Music request

On the desktop computer:

1. Open Chrome.
2. Go to:
   `https://music.youtube.com`
3. Make sure you are logged into the Google/YouTube account containing the playlists you want piPod to access.
4. Open Developer Tools:
   `Ctrl+Shift+I`
5. Select the **Network** tab.
6. Filter for:
   `browse`
7. Use YouTube Music normally, such as opening **Library**, until a `browse?...` request appears.
8. Right-click that request.
9. Select:
   `Copy → Copy as cURL`

Do not share the copied cURL command. It contains Google session credentials.

## 2. Save the cURL request on the Pi

On the Pi:

```bash
nano ~/.piPod/request.txt
```

Paste the entire copied cURL command.

Save with:

```text
Ctrl+O
Enter
Ctrl+X
```

## 3. Extract the request headers

Run:

```bash
python - <<'PY'
import shlex

request_file = "/home/pi/.piPod/request.txt"
headers_file = "/home/pi/.piPod/headers.txt"

text = open(request_file).read()
args = shlex.split(text)

headers = []
i = 0

while i < len(args):
    arg = args[i]

    if arg in ("-H", "--header") and i + 1 < len(args):
        headers.append(args[i + 1])
        i += 2
        continue

    if arg in ("-b", "--cookie") and i + 1 < len(args):
        headers.append("Cookie: " + args[i + 1])
        i += 2
        continue

    i += 1

with open(headers_file, "w") as f:
    f.write("\n".join(headers))

print("Created:", headers_file)

for header in headers:
    name = header.split(":", 1)[0]
    print(name)
PY
```

The output should include:

```text
Cookie
Authorization
```

among the other headers.

Chrome stores the cookie in the cURL command using `-b`, so simply extracting `-H` entries is not sufficient.

## 4. Create `browser.json`

Activate the piPod virtual environment if necessary, then:

```bash
cd ~/.piPod

python - <<'PY'
from ytmusicapi import setup

headers = open("headers.txt").read()

setup(
    filepath="browser.json",
    headers_raw=headers
)

print("Recreated browser.json")
PY
```

This should create:

```text
/home/pi/.piPod/browser.json
```

## 5. Test the authentication

Run:

```bash
python - <<'PY'
from ytmusicapi import YTMusic

yt = YTMusic("/home/pi/.piPod/browser.json")

playlists = yt.get_library_playlists()

print("Playlist count:", len(playlists))

for playlist in playlists[:10]:
    print(playlist["title"])
PY
```

A successful test should show a non-zero playlist count and playlist names.

## 6. piPod configuration

In:

```text
/home/pi/.piPod/piPod.conf
```

the YouTube Music authentication file should be:

```ini
YouTubeOauthFile = browser.json
```

In:

```text
/home/pi/RaspberryPi-iPod/common/library/youtubedownloader.py
```

authentication should use:

```python
from ytmusicapi import YTMusic
```

and:

```python
def getYouTubeAutorization(self):
    return YTMusic(
        self.config.YouTubeDownloadOauthFileLocation
    )
```

## Important notes

`request.txt`, `headers.txt`, and `browser.json` contain authentication credentials. Do not commit them to Git or share their contents.

Browser authentication may eventually expire. If piPod later stops seeing YouTube Music playlists, repeat this procedure to generate a fresh `browser.json`.

Also make sure the Pi's system clock is correct before using YouTube Music. HTTPS authentication can fail if the Pi has an incorrect date or time.
