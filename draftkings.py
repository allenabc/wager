from main import access_pickle


def get_soup(fn):
    soup_obj = access_pickle(fn)
    return soup_obj


def convert_soup_to_lists(pickle_file, sport):
    soup = access_pickle(pickle_file)
    team_names = soup.find_all("span", class_="teamName")
    pass


