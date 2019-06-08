# Matchflix #

import os
import tkinter as tk
from readers import *
from count import *
import signal
from classes import *
from math import ceil
from functions import *

WINDOW_FORMAT = (16, 9)
WINDOW_TIMES_SIZE = 60
width = None
height = None

def validate_login_name(name, users):
    for u in users.values():
        if u.name == name:
            return u
    return None
    # for u in users:
    #     if users[u].name == name:
    #         return User(users[u].id, users[u].name,users[u].rated_shows)
    # return None

# the show is a list of tuple => (show_id, show_rate)
def has_rated_show(id_show, other_shows,debug=False):
    if(debug):
        print("id {}, others {}".format(id_show,other_shows))
    for s in other_shows:
        if(s[SHOW_ID] == id_show):
            return s
    return NOT_FOUND

# returns the intersection of rated shows of two users
def get_intersec(user, other):
    intersecs = []

    for user_show in user.rated_shows:
        #print(user_show)
        user_show_id = user_show[SHOW_ID]
        other_show = has_rated_show(user_show_id, other.rated_shows)
        if (other_show != NOT_FOUND):
            intersecs.append(
                Intersec(user_show_id, user_show[SHOW_RATE], other_show[SHOW_RATE])
            )
    return intersecs

def get_suggestions(user, users_data, shows):
    compared_users = []
    suggestions = [] # will be suggested series with 3 stars or more
    #  it's a list of ids of the shows

    users_data_values = users_data.values()
    for comp in users_data_values:
        # pegar interseção dos shows de user e cada usuario, pelo id
        if(user.id != comp.id):
            intersection = get_intersec(user, comp)
            if(len(intersection) >= MIN_NUMBER_OF_MATCHES):
                newcomp = ComparedUsers(comp, intersection)
                if(newcomp.match_percentage >= ACCEPTED_MATCH_PERCENT):
                    compared_users.append(newcomp)
    # sort by dercreasing show rate (from 5 to 1 stars)
    compared_users = sorted(compared_users, key=lambda x: x.match_percentage,reverse=True)
    # debug
    print("seus shows (id do show, note que você deu):",sorted(user.rated_shows, key=lambda x: x[SHOW_ID]))
    
    # getting list of suggested shows
    for comp in compared_users:
        # debug
        #if(comp.other_user.name == 'Omar2'):
            #print("achei",comp.other_user)
            #print("comp other user",comp.other_user.rated_shows)
        sorted_comp_user_shows = sorted(comp.other_user.rated_shows, key=lambda x: x[SHOW_RATE],reverse=True)
        
        for show in sorted_comp_user_shows:
            # if a good rated show of a matched user isn't rated by the user
            # it will be suggested to the user
            if(show[SHOW_RATE] < MIN_ACCEPTED_RATE):
                continue
            if(has_rated_show(show[SHOW_ID], user.rated_shows)==NOT_FOUND ):
                # if this show wasn't added before then add to suggestions
                if(not(show[SHOW_ID] in suggestions)):
                    suggestions.append( show[SHOW_ID] )
    
    return suggestions, compared_users

class FrameFiller:
    def __init__(self, title, showsFrame,shows_to_place, show_database, isRated=False):
        self.pageFrame = showsFrame
        self.shows_to_place = shows_to_place
        self.show_database = show_database
        self.isRated = isRated

        self.current_page = 0
        self.placed_shows = []
        self.total_of_pages = ceil(len(shows_to_place) / SHOWS_PER_PAGE)
        self.vartxt = tk.StringVar()
        self.label = tk.Label(self.pageFrame, text=title)
        self.page_label = tk.Label(self.pageFrame, textvariable=self.vartxt)
        self.nextBttn = tk.Button( self.pageFrame, text='Próximo', command=lambda:self.next_page() )
        self.prevBttn = tk.Button( self.pageFrame, text='Anterior', command=lambda:self.prev_page() )
        
        self.nextBttn.grid(row=SHOWS_PER_PAGE+2, column=2)
        self.prevBttn.grid(row=SHOWS_PER_PAGE+2, column=0)
        self.page_label.grid(row=SHOWS_PER_PAGE+2, column=1)
        self.label.grid(row=0, column=1)

        self.reset_shows()
    
    def destroy_shows(self):
        for show in self.placed_shows:
            self.placed_shows.remove(show)
            show.destroy()
    
    def reset_shows(self):
        self.destroy_shows()
        
        i = 2 # row to start showing shows
        index = 0
        if(self.isRated):
            stars = ''
            # for i in range(int(show[SHOW_RATE])):
            #     stars += '*'
            #tk.Label(showsFrame, text=show.name+' | estrelas: '+stars).grid(row=i,column=0)
        else:
            #mylist.insert(tk.END, get_show_by_id(show_id, show_database).name) # fix terminar
            #tk.Label(self.pageFrame, text=get_show_by_id(show_id, self.show_database).name).grid(row=i,column=0)#,sticky=tk.W)
            selected_shows = self.shows_to_place[self.current_page*SHOWS_PER_PAGE:self.current_page*SHOWS_PER_PAGE+SHOWS_PER_PAGE]
            self.vartxt.set("Página {}/{}".format(self.current_page+1, self.total_of_pages))
            for s in selected_shows:
                self.placed_shows.append(
                    tk.Button(self.pageFrame, text=get_show_by_id(s, self.show_database).name)
                )
                self.placed_shows[index].grid(row=index+i,column=1)
                index += 1


    def next_page(self):
        if(self.current_page+1 < self.total_of_pages):
            self.current_page += 1
            self.reset_shows()

    def prev_page(self):
        if(self.current_page > 0):
            self.current_page -= 1
            self.reset_shows()
    
    def destroy(self):
        self.destroy_shows()
        self.label.destroy()
        self.nextBttn.destroy()
        #self.prevBttn.destroy() fix


def new_session(name, users_data, show_database, info_txt, oldroot):
    user = validate_login_name(name, users_data)
    if(user != None):

        suggestions, compared_users = get_suggestions(user, users_data, show_database)
        print("total de matches:",len(compared_users))
        print("")
        print("melhor match:",compared_users[0].other_user.name)
        print("")
        print("10 melhores matches dos usuários comparados:")
        print("  nome | porcentagem de match | shows (id do show, note que deu)")
        bests = compared_users[:10]
        for i in bests:
            print("  {} | {}% | shows (id do show, note que deu){}\n".format(
                i.other_user.name, int(i.match_percentage), i.other_user.rated_shows
            ))
        print("====================")
        print("total de sugeridos:",len(suggestions))
        print("20 melhores sugeridos (id's):",suggestions[:20])
        oldroot.destroy()
        
        root = tk.Tk()
        root.title('Matchflix')
        width = WINDOW_FORMAT[0]*WINDOW_TIMES_SIZE
        height = WINDOW_FORMAT[1]*WINDOW_TIMES_SIZE
        
        root.geometry(get_geometry(root, width, height))

        # declaring widgets
        topbarFrame = tk.Frame(root)
        
        showsFrame = tk.Frame(root)
        suggestionFrame = tk.Frame(root)
        ratedFrame = tk.Frame(root)

        matchflix_label = tk.Label(topbarFrame, text='Matchflix', fg='darkred',font=("Helvetica", 30))
        # fix terminar isso, para poder trocar user
        tk.Label(topbarFrame, text='logado como {}'.format(user.name)).grid(row=0, column=1)
        show_frame_title = 'Filmes e Séries'
        sugg_frame_title = 'Sujestões para você'
        rate_frame_title = 'Avaliados por mim'

        open_window = FrameFiller(sugg_frame_title, suggestionFrame,suggestions, show_database)
        # show_label = tk.Label(showsFrame, text=show_f)
        # sugg_label = tk.Label(suggestionFrame, text=)
        # rate_label = tk.Label(ratedFrame, text=)

        listrow = 1
        
        # put wids
        topbarFrame.grid(row=0, column=0)
        #   fix mostrar shows por ordem de relevancia
        #showsFrame.grid(row=listrow, column=0)
        suggestionFrame.grid(row=listrow, column=1)
        #ratedFrame.grid(row=listrow, column=2)

        # show_label.grid(row=0, column=0)
        # sugg_label.grid(row=0, column=0)
        # rate_label.grid(row=0, column=0)

        matchflix_label.grid(row=0, column=0)

        root.mainloop()
    else:
        info_txt.set("Nome '{}' não cadastrado!".format(name))

def run():
    os.system("clear")
    users_data = read_users_data()
    show_database = read_shows()

    # root screen (login screen)
    root = tk.Tk()
    root.title('Entre ou crie uma conta no Matchflix')
    width = 600
    height = 400

    # declaring widgets
    loginFrame = tk.Frame(root)
    # fix terminar parte de cadastro
    registerFrame = tk.Frame(root)
    #   for login
    info_txt = tk.StringVar()
    info = tk.Label(loginFrame, textvariable=info_txt)
    login_txt = tk.Label(loginFrame, text='Nome de login: (escreva um nome que já existe)')
    username = tk.Entry(loginFrame)
    # debug
    # username.delete(0,tk.END)
    # username.insert(0,'Omar')
    # end
    logbutton = tk.Button(loginFrame, text='Entrar',
     command=lambda:new_session(username.get().capitalize(), users_data, show_database, info_txt, root))

    # puttin all widgets
    loginFrame.grid(row=0,column=0)
    registerFrame.grid(row=0,column=1)

    username.grid(row=0, column=1)  
    login_txt.grid(row=0,column=0)
    logbutton.grid(row=1,column=0)
    info.grid(row=1,column=1)
  
    root.geometry(get_geometry(root, width, height))

    root.mainloop()


if(__name__ == '__main__'):
    # for debug
    # root = tk.Tk()
    # new_session('Omar', read_users_data(), read_shows(),
    #   tk.Label(tk.Frame(root), textvariable=tk.StringVar()), root)
    # root.mainloop()
    run()