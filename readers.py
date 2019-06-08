from consts import *
from classes import *

# read shows from file
def read_shows():
    """
    'shows' is a dictionary of 'Show' objects, the key is 'show_id'
    shows[show_id] = Show(id, name)
    """
    fshows = open("shows.txt","r")
    shows = {}

    for s in fshows:
        temp = s.split('|')
        show_id = int(temp[SHOW_ID])
        shows[show_id] = Show(show_id, temp[SHOW_NAME][:-1])
        #shows.append((int(temp[SHOW_ID]), temp[SHOW_NAME][:-1])) # read as a tuple
    
    fshows.close()
    return shows

# read users from file
def read_users_data():
    """
    'users' is a dictionary of 'User' objects, the key is the user id
    users[user_id] = User(user_id, user_name, user_rated_shows)
    """
    #debug_name = 'Charde'
    fusers_data = open("users_data.txt","r")
    users = {}

    for u in fusers_data:
        # read the user informations
        user_shows_str = []
        temp = u.split('|')
        user_id = int(temp[USER_ID])
        #temp_user = User(user_id, temp[USER_NAME])

        # list like this => ['4-5', '5-3', '6-21']
        user_shows_str = temp[USER_SHOWS][:-1].split(',')
        new_rated_shows = []

        # if(temp[USER_NAME] == debug_name):
        #     print("temp user shows")
        #     print(temp[USER_SHOWS])
        #     print("user shows str:")
        #     print(user_shows_str)

        # read shows rated by the user
        # it's kept as a list of tuples => (show_id, show_rate)
        for show in user_shows_str:
            showid, showrate = show.split('-')
            
            new_rated_shows.append( 
                ( int(showid), int(showrate) )
            )
        
        users[user_id] = User(user_id, temp[USER_NAME], new_rated_shows)
        
        # debug
        # if(users[user_id].name == debug_name):
        #     print("rated user shows")
        #     print(sorted(users[user_id].rated_shows, key=lambda x : x[SHOW_ID]))
        #     pause = input("")

    
    fusers_data.close()
    return users