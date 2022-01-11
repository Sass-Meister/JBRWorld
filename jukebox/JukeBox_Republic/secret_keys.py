# These are Peter's keys, they go unused because I can't edit his settings to use the redirect_uri I please
#client_id = 'ca45aea8a19447c3844ccb67e93e21b4'
#client_secret = 'e0201d80fa524b3d944ee45582949922'
#scope = 'playlist-modify-private playlist-modify-public playlist-read-collaborative playlist-read-private ugc-image-upload user-follow-modify user-follow-read user-library-modify user-library-read user-modify-playback-state user-read-currently-playing user-read-email user-read-playback-position user-read-playback-state user-read-private user-read-recently-played user-top-read'


# These are Max's keys and work with the redirect uri that is used when run on a server
client_id = '2bbbe9ccb58544678963e26d40ac3422'
client_secret = 'a95370f1c49b4ebc94251cd33da3e2e7'
scope = 'user-modify-playback-state user-read-currently-playing user-read-playback-position user-read-playback-state user-read-private user-read-recently-played user-top-read'

# Uncomment the one for the correct situation
redirect_uri = 'http://jbr.world/callback' # Used for www
#redirect_uri = 'http://127.0.0.1:8000/callback' # used for localhost

