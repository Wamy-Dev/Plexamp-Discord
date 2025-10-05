from functions.discordFunctions import DiscordRPC
from functions.plexFunctions import PlexFunctions
from functions.configFunctions import loadItem
import time

def main():
    config_file = "config/config.json"
    discord_app_id = loadItem(config_file, "discord_app_id")
    plex_token = loadItem(config_file, "plex_token")
    public_plex_url = loadItem(config_file, "public_plex_url")
    private_plex_url = loadItem(config_file, "private_plex_url")
    plex_user = loadItem(config_file, "plex_user")

    if not all([discord_app_id, plex_token, public_plex_url, private_plex_url, plex_user]):
        print("Missing configuration. Please check config.json.")
        return

    discord_rpc = DiscordRPC(discord_app_id)
    if not discord_rpc.setupConnection():
        return

    plex_functions = PlexFunctions(plex_token, public_plex_url, private_plex_url, plex_user)

    try:
        while True:
            sessions = plex_functions.getSessions()
            if sessions:
                if not discord_rpc.connected:
                    if not discord_rpc.setupConnection():
                        continue
                activity = discord_rpc.formatMusicActivity(sessions)
                if activity:
                    discord_rpc.setActivity(activity)
            else:
                discord_rpc.disconnect()
            time.sleep(10)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        discord_rpc.disconnect()

if __name__ == "__main__":
    main()
