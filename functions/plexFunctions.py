import httpx

class PlexFunctions():
    def __init__(self, plex_token: str, plex_url: str, plex_user: str):
        self.plex_token = plex_token
        self.plex_url = plex_url
        self.plex_user = plex_user

    def getPlayingMedia(self, sessions: dict) -> dict:
        playing_media = {}
        media_container = sessions.get('MediaContainer', {})
        num_items = media_container.get('size', 0)
        if num_items == 0:
            return playing_media
        
        metadata = media_container.get('Metadata', [])
        for item in metadata:
            user = item.get("User", {}).get("title", "Unknown User")
            if user.lower() != self.plex_user.lower():
                continue
            
            if item.get("type") != "track": # only handle music tracks, can be expanded later
                continue

            title = item.get("title")
            artist = item.get("originalTitle") or item.get("grandparentTitle")
            album = item.get("parentTitle")
            album_year = item.get("parentYear", "")
            thumbnail = item.get("thumb") or item.get("grandparentThumb")
            duration = item.get("duration")  # duration in milliseconds
            duration_offset = item.get("viewOffset")  # current position in milliseconds

            player = item.get("Player", {})
            player_state = player.get("state", "playing") # paused, playing

            if player_state != "playing":
                continue

            playing_media = {
                "user": user,
                "plex_url": self.plex_url,
                "plex_token": self.plex_token,
                "title": title,
                "artist": artist,
                "album": album,
                "album_year": album_year,
                "thumbnail": thumbnail,
                "duration": duration,
                "duration_offset": duration_offset,
            }
            break # assuming only one media item per user

        return playing_media
        

    def getSessions(self) -> dict:
        headers = {
            "X-Plex-Token": self.plex_token,
            "Accept": "application/json"
        }
        url = f"{self.plex_url}/status/sessions"
        response = httpx.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            playing_media = self.getPlayingMedia(data)
            if playing_media:
                return playing_media
        return {}