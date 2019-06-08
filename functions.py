from count import mergeSort

# returns number of inversions
def do_count_invert(sorted_shows):
    rate_list = []
    for i in sorted_shows:
        rate_list.append(i.user_rate)
    return mergeSort(rate_list, len(rate_list))

# fix pode ser otimizado para retornar valores já calculados
def get_max_inverts(lengh):
    max_inverts = 0
    for i in range(lengh):
        max_inverts += i
    return max_inverts

def get_geometry(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    return "{}x{}+{}+{}".format(
        width, height, int((screen_width-width)/2), int((screen_height-height)/2)
    )

def get_show_by_id(show_id, shows):
    return shows[show_id]