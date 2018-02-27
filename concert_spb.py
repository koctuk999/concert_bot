import bs4
import requests
import pickle
class Artist(object):
    def __init__(self,name,date,time,price,club):
        self.name=name
        self.date=date
        self.time=time
        self.price=price
        self.club=club
    def __str__(self):
        rep="\n\t\t{0}:\nДата:{1}\nВремя:{2}\nЦена:{3}".format(
            self.name,self.date,self.time,self.price)
        return rep


def afisha_aurora():
    req = requests.get("http://aurora-hall.ru/")
    b = bs4.BeautifulSoup(req.text, "html.parser")
    L = b.find_all(class_="item")
    afisha = []
    for i in L:
        name = i.find_all(class_="name-group")[0].get_text()
        date = i.find_all(class_="date")[0].get_text().strip()
        time = i.find_all(class_="time")[0].get_text().strip().strip('АКЦИЯ:').strip()
        artist =Artist(name,date,time,None,'Aurora')
        afisha.append(artist)
    return afisha


def afisha_kosmonavt():
    req = requests.get("http://www.cosmonavt.su/?content=billboard")
    b = bs4.BeautifulSoup(req.text, "html.parser")
    L = b.find_all(class_="add_item concert")
    afisha = []
    for i in L:
        name = i.select('.nostyle')[0].get_text()
        date = ' '.join((i.select('.add_date')[0].get_text(), i.select('.add_month')[0].get_text(),
                         i.select('.add_day')[0].get_text()))
        time = i.select('.add_time')[0].get_text()
        artist = Artist(name, date, time, None, 'Космонавт')
        afisha.append(artist)
    return afisha


def write_in_file(name_file, afisha):
    f = open(name_file, 'wb')
    billboard=afisha
    pickle.dump(billboard,f)
    f.close()

def read_of_file(name_file):
    f=open(name_file,'rb')
    return pickle.load(f)



if __name__ == '__main__':
    afisha=read_of_file('aurora.txt')
    for artist in afisha:
        print(artist)