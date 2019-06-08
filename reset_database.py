import random
from consts import *
from readers import read_shows

fusers = open("users.txt","r")

fusers_data = open("users_data.txt","w")
#i = random.choice(lista)

users = {}
shows = read_shows() # return dictionary with id to the name of the show

#tshows = {}   this is for debug


# read users from file
for u in fusers:
    temp = u.split('|')
    userid = int(temp[USER_ID])
    username = temp[USER_NAME][:-1]
    fusers_data.write("{}|{}|".format(userid, username))
    # user -> user id, user name and list of tuples of show_id and rate
    users[userid] = (userid, username, [])
    number_of_rated_shows = random.randint(MIN_SHOWS,MAX_SHOWS+1)
    # choose the shows and give the rate
    rateline = ''
    for i in range(number_of_rated_shows):

        usershowid = random.choice(list(shows))
        usershowrate = random.randint(1,5)
        rateline += "{}-{},".format(usershowid, usershowrate)
        # putting into a users library for debug
        # users[userid][USER_SHOWS].append( 
        #     ( usershowid, usershowrate )
        # )
    fusers_data.write(rateline[:-1]) # :-1 removes the ',' of the end
    fusers_data.write('\n')
    

# for debug
# user = random.choice(users)
# #print(user)
# print("nome",user[USER_NAME])
# print("filmes e *'s")
# for i in user[USER_SHOWS]:
#     print("{}*: {}".format(i[1],tshows[i[0]]))



fusers_data.close()
fusers.close()
