from bs4 import BeautifulSoup
import urllib2, re
from models import Equipo, Deporte

def populate_equipos_futbol():
    futbol = Deporte.objects.create(name="Futbol")

    urls = ["https://resultados.as.com/resultados/futbol/primera/equipos/", "https://resultados.as.com/resultados/futbol/segunda/equipos/",
            "https://resultados.as.com/resultados/futbol/inglaterra/equipos/", "https://resultados.as.com/resultados/futbol/italia/equipos/",
            "https://resultados.as.com/resultados/futbol/alemania/2017_2018/equipos", "https://resultados.as.com/resultados/futbol/francia/equipos/"]

    for url in urls:
        request = urllib2.Request(url)
        request.add_header('User-Agent',
                             'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
        page = urllib2.urlopen(request).read()
        soup = BeautifulSoup(page, 'html.parser')

        teams = soup.find_all('li', attrs={'class': 'col-md-3 col-sm-4 col-xs-12 s-tcenter mod-info-equipo'})
        for team in teams:
            #print team.prettify()
            name = team.find('span', attrs={'class': 'escudo'}).get_text()
            image = "http:" + team.find('img').get("src")
            country = team.find('span', attrs={'class': 'pais'}).get_text()

            Equipo.objects.create(name=name, image = image, country = country, sport=futbol)
            #print name, image, country

def populate_equipos_f1():
    f1 = Deporte.objects.create(name="Formula 1")

    urls = ["http://www.marca.com/deporte/motor/formula1/escuderias/?intcmp=MENUMIGA&s_kw=escuderias-y-pilotos"]

    for url in urls:
        request = urllib2.Request(url)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
        page = urllib2.urlopen(request).read()
        soup = BeautifulSoup(page, 'html.parser')
        riders = soup.find_all('li', attrs={'class': 'piloto col-md-6 col-sm-6 col-xs-12'})
        for rider in riders:

            name = rider.find('a').get("title")
            raw_images = rider.find_all("img")
            image = raw_images[0].get("src")
            country = raw_images[1].get("alt")
            #print name, image, country
            Equipo.objects.create(name=name, image=image, country=country, sport=f1)


def populate_equipos_motogp():
    moto_gp = Deporte.objects.create(name="Moto GP")

    urls = ["https://resultados.as.com/resultados/motor/motogp/2017/integrantes/"]

    for url in urls:
        request = urllib2.Request(url)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
        page = urllib2.urlopen(request).read()
        soup = BeautifulSoup(page, 'html.parser')
        riders = soup.find_all('tr', attrs={'class': 'row-table-datos'})
        for rider in riders:
            #print rider.prettify()
            name = rider.find("a")
            if name != None:
                request2 = urllib2.Request("http:" + name.get("href"))
                request2.add_header('User-Agent',
                                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
                page2 = urllib2.urlopen(request2).read()
                soup2 = BeautifulSoup(page2, 'html.parser')
                image = "http:" + soup2.find('img', attrs={'class': 'img-max-size'}).get("src")
                name = name.get_text()
                country = rider.find('img', attrs={'class': 'pais'}).get("alt")
                #print name, country, image
                Equipo.objects.create(name=name, image=image, country=country, sport=moto_gp)

def populate_equipos_baloncesto():
    baloncesto = Deporte.objects.create(name="Baloncesto")

    urls = ["http://www.marca.com/baloncesto/acb/equipos.html?intcmp=MENUMIGA&s_kw=equipos-y-jugadores",
            "http://www.marca.com/baloncesto/nba/equipos.html"]
    cont = 0
    for url in urls:
        request = urllib2.Request(url)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
        page = urllib2.urlopen(request).read()
        soup = BeautifulSoup(page, 'html.parser')
        teams = soup.find_all('li', attrs={'id': 'nombreEquipo'})
        for team in teams:
            image = "http:" + team.find('img', attrs={'class': 'escudo'}).get("src")
            if(cont < 1):
                country = "Spain"
                name = team.find('h2', attrs={'class': 'cintillo'}).get_text()
            else:
                country = "EE.UU."
                name = team.find('h2').find("a").get_text()
            #print name, image, country
            Equipo.objects.create(name=name, image=image, country=country, sport=baloncesto)
        cont += 1

def populate_tenis():
    tenis = Deporte.objects.create(name="Tenis")

    urls = ["https://resultados.as.com/resultados/tenis/ranking_atp/2015/clasificacion/"]

    for url in urls:
        request = urllib2.Request(url)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
        page = urllib2.urlopen(request).read()
        soup = BeautifulSoup(page, 'html.parser')
        tennis_players = soup.find_all('tr', attrs={'class': 'row-table-datos'})
        for tp in tennis_players:

            name = tp.find('span', attrs={'class': 'player-nom'})

            if name != None:
                name = name.get_text()
                url2 = tp.find("a")
                if url2 != None:
                    url2 = "http:" + url2.get("href")
                    request2 = urllib2.Request(url2)
                    request2.add_header('User-Agent',
                                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
                    page2 = urllib2.urlopen(request2).read()
                    soup2 = BeautifulSoup(page2, 'html.parser')
                    data = soup2.find('section', attrs={'class': 'ficha-jug cf'})
                    country = data.find_all("dd")[1].find("strong").get_text()
                    image = "http:" + soup2.find('img', attrs={'class': 's-left ficha-jug-foto'}).get("src")
                else:
                    country = tp.find('span', attrs={'class': 'pais'}).get_text()
                    image = "http:" + tp.find('img', attrs={'class': 'ico-bandera'}).get("src")
                #print name, country, image
                Equipo.objects.create(name=name, image=image, country=country, sport=tenis)

