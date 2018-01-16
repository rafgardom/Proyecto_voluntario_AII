# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2, re
import requests
from models import Equipo, Deporte, Noticia
from datetime import datetime
import unicodedata

def populate_equipos_futbol():
    futbol = Deporte.objects.filter(name = "Futbol")
    if not futbol:
        futbol = Deporte.objects.create(name="Futbol")
    else:
        futbol = Deporte.objects.get(name = "Futbol")

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
            notices_urls = None
            name = team.find('span', attrs={'class': 'escudo'}).get_text().strip()
            if name == "Deportivo":
                name = u"Deportivo Coruña"
            image = "http:" + team.find('img').get("src")
            country = team.find('span', attrs={'class': 'pais'}).get_text().strip()
            as_url = team.find('a', attrs={'class': "col-md-6 col-sm-6 col-xs-6 content-info-escudo"}).get("href")
            complete_as_url = "https://resultados.as.com/" + as_url

            useful_name = name.lower()
            if len(useful_name.split(" ")) > 1:
                marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.split(" ")[0].strip() + "+" \
                                + useful_name.split(" ")[1].strip() + "+futbol&b_avanzada="
            else:
                marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.strip() + "+futbol&b_avanzada="

            notices_urls = complete_as_url + "|" + marca_url

            if name == "Betis":
                notices_urls += "|" + "http://www.estadiodeportivo.com/betis/"

            elif name =="Sevilla":
                notices_urls += "|" + "http://www.estadiodeportivo.com/sevilla/"

            loaded_team = Equipo.objects.filter(name = name)
            if loaded_team:
                loaded_team.update(name = name, image = image, country = country, sport = futbol, url = notices_urls)
            else:
                Equipo.objects.create(name=name, image = image, country = country, sport=futbol, url = notices_urls)
            #print name, image, country


def populate_equipos_f1():
    f1 = Deporte.objects.filter(name="Formula 1")
    if not f1:
        f1 = Deporte.objects.create(name="Formula 1")
    else:
        f1 = Deporte.objects.get(name="Formula 1")

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
            marca_url = rider.find('a').get("href")
            raw_images = rider.find_all("img")
            image = raw_images[0].get("src")
            country = raw_images[1].get("alt")
            #print name, image, country

            complete_url = marca_url

            loaded_team = Equipo.objects.filter(name=name)
            if loaded_team:
                loaded_team.update(name = name, image = image, country = country, sport = f1, url = complete_url)
            else:
                Equipo.objects.create(name=name, image=image, country=country, sport=f1, url = complete_url)



def populate_equipos_motogp():
    moto_gp = Deporte.objects.filter(name="Moto GP")
    if not moto_gp:
        moto_gp = Deporte.objects.create(name="Moto GP")
    else:
        moto_gp = Deporte.objects.get(name="Moto GP")

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
                as_url = "http:" + name.get("href")
                page2 = urllib2.urlopen(request2).read()
                soup2 = BeautifulSoup(page2, 'html.parser')
                image = "http:" + soup2.find('img', attrs={'class': 'img-max-size'}).get("src")
                name = name.get_text()
                country = rider.find('img', attrs={'class': 'pais'}).get("alt")
                #print name, country, image

                useful_name = name.lower()

                if len(useful_name.split(" ")) > 1:
                    marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.split(" ")[
                        0].strip() + "+" \
                                + useful_name.split(" ")[1].strip() + "&b_avanzada="
                else:
                    marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.strip() + "&b_avanzada="

                complete_url = as_url.strip() + "|" + marca_url.strip()
                loaded_team = Equipo.objects.filter(name=name)
                if loaded_team:
                    loaded_team.update(name=name, image=image, country=country, sport=moto_gp, url=complete_url)
                else:
                    Equipo.objects.create(name=name, image=image, country=country, sport=moto_gp, url=complete_url)


def populate_equipos_baloncesto():
    baloncesto = Deporte.objects.filter(name="Baloncesto")
    if not baloncesto:
        baloncesto = Deporte.objects.create(name="Baloncesto")
    else:
        baloncesto = Deporte.objects.get(name="Baloncesto")

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
                useful_name = name.lower()

                if "Madrid" in name:
                    name = "Real Madrid Baloncesto"


                if len(useful_name.split(" ")) > 1:
                    marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.split(" ")[
                        0].strip() + "+" \
                                + useful_name.split(" ")[1].strip() + "+baloncesto&b_avanzada="
                else:
                    marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.strip() + "+baloncesto&b_avanzada="

            else:
                country = "EE.UU."
                name = team.find('h2').find("a").get_text()
                useful_name = name.lower()
                if len(useful_name.split(" ")) > 1:
                    marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.split(" ")[
                        0].strip() + "+" \
                                + useful_name.split(" ")[1].strip() + "&b_avanzada="
                else:
                    marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.strip() + "&b_avanzada="

            complete_url = marca_url

            loaded_team = Equipo.objects.filter(name=name)
            if loaded_team:
                loaded_team.update(name=name, image=image, country=country, sport=baloncesto, url=complete_url)
            else:
                Equipo.objects.create(name=name, image=image, country=country, sport=baloncesto, url=complete_url)

        cont += 1

def populate_tenis():
    tenis = Deporte.objects.filter(name="Tenis")
    if not tenis:
        tenis = Deporte.objects.create(name="Tenis")
    else:
        tenis = Deporte.objects.get(name="Tenis")

    urls = ["https://resultados.as.com/resultados/tenis/ranking_atp/2015/clasificacion/"]

    for url in urls:
        request = urllib2.Request(url)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
        page = urllib2.urlopen(request).read()
        soup = BeautifulSoup(page, 'html.parser')
        tennis_players = soup.find_all('tr', attrs={'class': 'row-table-datos'})

        for tp in tennis_players:
            complete_url = ""
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
                    if data.find('div', attrs={'class': 'itm-body s-left'}):
                        as_url = "http:" + data.find('div', attrs={'class': 'itm-body s-left'}).find("a").get("href")
                    else:
                        as_url =""

                    useful_name = name.lower()
                    if len(useful_name.split(" ")) > 1:
                        marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.split(" ")[
                            0].strip() + "+" \
                                    + useful_name.split(" ")[1].strip() + "&b_avanzada="
                    else:
                        marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.strip() + "&b_avanzada="

                    if as_url =="":
                        complete_url += marca_url
                    else:
                        complete_url += as_url + "|" + marca_url

                else:
                    country = tp.find('span', attrs={'class': 'pais'}).get_text()
                    image = "http:" + tp.find('img', attrs={'class': 'ico-bandera'}).get("src")

                    useful_name = name.lower()
                    if len(useful_name.split(" ")) > 1:
                        marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.split(" ")[
                            0].strip() + "+" \
                                    + useful_name.split(" ")[1].strip() + "&b_avanzada="
                    else:
                        marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.strip() + "&b_avanzada="

                    complete_url += marca_url

                #print name, country, image
                loaded_team = Equipo.objects.filter(name=name)
                if loaded_team:
                    loaded_team.update(name=name, image=image, country=country, sport=tenis, url=complete_url)
                else:
                    Equipo.objects.create(name=name, image=image, country=country, sport=tenis, url=complete_url)

                
def noticias_futbol_marca():
    futbol = Deporte.objects.get(name="Futbol")
    equipos = Equipo.objects.filter(sport=futbol)
    is_new = True

    for equipo in equipos:
        url_futbol = equipo.url
        url = remove_accents(url_futbol.split("|")[1])
        if requests.get(url).status_code == 404:
            continue
        request2 = urllib2.Request(url)
        request2.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
        page2 = urllib2.urlopen(request2).read()
        soup2 = BeautifulSoup(page2, 'html.parser')
        i = 0
        moment = None
        body = None
        if soup2.find('div',attrs={'class':'nav_paginacion'}):
            while i<3:
                #print i
                equiponame = equipo.name
                if " " in equiponame:
                    equiponame = equiponame.replace(" ","+")
                urls3 = "http://cgi.marca.com/buscador/archivo_marca.html?q="+remove_accents(equiponame)+"&t=1&i="+str(i)+"1&n=10&fd=0&td=0&w=65&s=1"
                #print urls3
                i += 1
                if requests.get(urls3).status_code == 404:
                    continue
                request3 = urllib2.Request(urls3)
                request3.add_header('User-Agent',
                               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
                page3 = urllib2.urlopen(request3).read()
                soup3 = BeautifulSoup(page3, 'html.parser')
                for noticias in soup3.find_all('div',attrs={'class':'texto-foto'}):
                    #print noticias
                    title = noticias.find('h4')
                    #print title.get_text()
                    if title != None:
                        url3 = title.find('a').get('href')
                        if not "http" in url3:
                            continue
                        try:
                            page4 = urllib2.urlopen(url3).read()
                            soup4 = BeautifulSoup(page4, 'html.parser')
                            stripdate = soup4.find('time', attrs={'itemprop': 'dateModified'})
                            if stripdate != None:
                                moment = try_parsing_date(stripdate.get_text().replace('CET', '').strip())
                                print moment
                                if moment == None:
                                    moment = try_parsing_date(stripdate.get_text().replace('CST', '').strip())
                                    print moment
                            else:
                                moment = None
                            body=[]
                            for row in soup4.find_all('div',attrs={'itemprop':'articleBody'}):
                                for cuerpo in row.find_all('p'):
                                    body.append(cuerpo.get_text())
                        except:
                            continue
                        
                    searched_team = Equipo.objects.get(name=equipo.name)
                    loaded_noticia = Noticia.objects.filter(url=url3, team=searched_team)
        
                    if not loaded_noticia:
                        Noticia.objects.create(title=title.get_text(), body=body, moment=moment, url=url3, team=equipo)
        
                    else:
                        is_new = False
                        break
                if is_new == False: #Esto se deberia quitar la primera vez que se ejecuta
                    break           #o entra aqui y se va saltando urls de una rara forma
                
def noticias_futbol_as():
    futbol = Deporte.objects.get(name="Futbol")
    equipos = Equipo.objects.filter(sport=futbol)
    is_new = True
    for equipo in equipos:
        url_futbol = equipo.url
        url = remove_accents(url_futbol.split("|")[0])
        if requests.get(url).status_code == 404:
            continue
        request2 = urllib2.Request(url)
        request2.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
        page2 = urllib2.urlopen(request2).read()
        soup2 = BeautifulSoup(page2, 'html.parser')
        url_noticias = soup2.find('div',attrs={'class':'s-tright'})
        try:
            url2 = "http:"+url_noticias.find('a').get('href')
            request3 = urllib2.Request(url2)
            request2.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
            page3 = urllib2.urlopen(request3).read()
            soup3 = BeautifulSoup(page3, 'html.parser')
            for noticias in soup3.find_all('div', attrs={"class":"pntc-content"}):
                title = noticias.find('h2')
                url3 = noticias.find('a').get('href')
                stripdate = noticias.find('span',attrs={'class':'fecha'})
                if stripdate != None:
                    moment = try_parsing_date(stripdate.get_text())
                if not "http" in url3:
                    continue
                try:
                    page4 = urllib2.urlopen(url3).read()
                    soup4 = BeautifulSoup(page4, 'html.parser')
                    body=[]
                    row = soup4.find('div',attrs={'itemprop':'articleBody'})
                    if row != None:
                        for cuerpo in row.find_all('p'):
                            body.append(cuerpo.get_text())
                except:
                    continue

                searched_team = Equipo.objects.get(name=equipo.name)
                loaded_noticia = Noticia.objects.filter(url=url3, team=searched_team)

                if not loaded_noticia:
                    Noticia.objects.create(title=title.get_text(), body=body, moment=moment, url=url3, team=equipo)

                else:
                    is_new = False
                    break
            if is_new == False:
                break
        except:
            continue

def noticias_ED():
    futbol = Deporte.objects.get(name="Futbol")
    equipos = Equipo.objects.filter(sport=futbol)
    is_new= True
    for equipo in equipos:
        if (equipo.name == "Sevilla" or equipo.name == "Betis"):
            url_futbol = equipo.url
            url = remove_accents(url_futbol.split("|")[2])
            if requests.get(url).status_code == 404:
                continue
            request2 = urllib2.Request(url)
            request2.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
            page2 = urllib2.urlopen(request2).read()
            soup2 = BeautifulSoup(page2, 'html.parser')
            for noticias in soup2.find_all(attrs={'itemprop':'headline'}):
                title = noticias.find('a').get_text()
                urlnoticia = "http://estadiodeportivo.com"+noticias.find('a').get('href')
                request3 = urllib2.Request(urlnoticia)
                request3.add_header('User-Agent',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
                page3 = urllib2.urlopen(request3).read()
                soup3 = BeautifulSoup(page3, 'html.parser')
                stripdate = soup3.find('span',attrs={'class':'fecha_hora'})
                stripdate =  stripdate.get_text().replace('|','').replace(' ','').replace('.','/')
                d = stripdate[:10]+ ' ' + stripdate[10:]
                moment = try_parsing_date(d)
                body=[]
                row = soup3.find('span',attrs={'itemprop':'articleBody'})
                if row != None:
                    for cuerpo in row.find_all('p'):
                        body.append(cuerpo.get_text())

                searched_team = Equipo.objects.get(name=equipo.name)
                loaded_noticia = Noticia.objects.filter(url=urlnoticia, team=searched_team)

                if not loaded_noticia:
                    Noticia.objects.create(title=title, body=body, moment=moment, url=urlnoticia, team=equipo)

                else:
                    is_new = False
                    break
            if is_new == False:
                break

def noticias_tenis_marca():
    tenis = Deporte.objects.get(name="Tenis")
    equipos = Equipo.objects.filter(sport=tenis)
    is_new = True
    for equipo in equipos:
        url = remove_accents(equipo.url)
        if "|" in url:
            url = url.split("|")[1]
        if requests.get(url).status_code == 404:
            continue
        request2 = urllib2.Request(url)
        request2.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
        page2 = urllib2.urlopen(request2).read()
        soup2 = BeautifulSoup(page2, 'html.parser')
        i = 0
        if soup2.find('div',attrs={'class':'nav_paginacion'}):
            while i<3:
                equiponame = equipo.name
                if " " in equiponame:
                    equiponame = equiponame.replace(" ","+")
                    
                urls3 = "http://cgi.marca.com/buscador/archivo_marca.html?q="+remove_accents(equiponame)+"&t=1&i="+str(i)+"1&n=10&fd=0&td=0&w=65&s=1"
                #print urls3
                i += 1
                #print urls3
                if requests.get(urls3).status_code == 404:
                    continue
                request3 = urllib2.Request(urls3)
                request3.add_header('User-Agent',
                               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
                page3 = urllib2.urlopen(request3).read()
                soup3 = BeautifulSoup(page3, 'html.parser')
                moment = None
                body = None
                for noticias in soup3.find_all('div',attrs={'class':'texto-foto'}):
                    #print noticias
                    title = noticias.find('h4')
                    #print title.get_text()
                    if title != None:
                        url3 = title.find('a').get('href')
                        if not "http" in url3:
                            continue
                        try:
                            page4 = urllib2.urlopen(url3).read()
                            soup4 = BeautifulSoup(page4, 'html.parser')
                            stripdate = soup4.find('time',attrs={'itemprop':'dateModified'})
                            print stripdate.get_text()
                            if stripdate != None:
                                moment = try_parsing_date(stripdate.get_text().replace('CET', '').strip())
                                if moment == None:
                                    moment = try_parsing_date(stripdate.get_text().replace('CST', '').strip())
                            else:
                                moment = None
                            body=[]
                            for row in soup4.find_all('div',attrs={'itemprop':'articleBody'}):
                                for cuerpo in row.find_all('p'):
                                    body.append(cuerpo.get_text())
                            #print body
                        except:
                            continue
                        
                    searched_team = Equipo.objects.get(name=equipo.name)
                    loaded_noticia = Noticia.objects.filter(url=url3, team=searched_team)
                    if not loaded_noticia:
                        Noticia.objects.create(title=title.get_text(), body=body, moment=moment, url=url3, team=equipo)
        
                    else:
                        is_new = False
                        break
                if is_new == False:
                    break


def noticias_tenis_as():
    tenis = Deporte.objects.get(name="Tenis")
    equipos = Equipo.objects.filter(sport=tenis)
    is_new = True
    for equipo in equipos:
        if "|" in equipo.url:
            url = remove_accents(equipo.url)
            url = url.split("|")[0]
            try:
                if requests.get(url).status_code == 404:
                    continue
                request2 = urllib2.Request(url)
                request2.add_header('User-Agent',
                               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
                page2 = urllib2.urlopen(request2).read()
                soup2 = BeautifulSoup(page2, 'html.parser')
                for noticias in soup2.find_all('div', attrs={"class":"pntc-content"}):
                    title = noticias.find('h2')
                    url3 = noticias.find('a').get('href')
                    stripdate = noticias.find('span',attrs={'class':'fecha'})
                    if stripdate != None:
                        moment = try_parsing_date(stripdate.get_text())
                    if not "http" in url3:
                        continue
                    try:
                        page3 = urllib2.urlopen(url3).read()
                        soup3 = BeautifulSoup(page3, 'html.parser')
                        body=[]
                        row = soup3.find('div',attrs={'itemprop':'articleBody'})
                        if row != None:
                            for cuerpo in row.find_all('p'):
                                body.append(cuerpo.get_text())
                    except:
                        continue

                    searched_team = Equipo.objects.get(name=equipo.name)
                    loaded_noticia = Noticia.objects.filter(url=url3, team=searched_team)

                    if not loaded_noticia:
                        Noticia.objects.create(title=title.get_text(), body=body, moment=moment, url=url3, team=equipo)

                    else:
                        is_new = False
                        break
                if is_new == False:
                    break
            except:
                continue
                
def noticias_baloncesto():
    baloncesto = Deporte.objects.get(name="Baloncesto")
    equipos = Equipo.objects.filter(sport=baloncesto)
    is_new = True
    for equipo in equipos:

        url = remove_accents(equipo.url)
        if requests.get(url).status_code == 404:
            continue
        request2 = urllib2.Request(url)
        request2.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
        page2 = urllib2.urlopen(request2).read()
        soup2 = BeautifulSoup(page2, 'html.parser')
        i = 0
        if soup2.find('div',attrs={'class':'nav_paginacion'}):
            while i<3:
                equiponame = equipo.name
                if " " in equiponame:
                    equiponame = equiponame.replace(" ","+")
                    
                urls3 = "http://cgi.marca.com/buscador/archivo_marca.html?q="+remove_accents(equiponame)+"&t=1&i="+str(i)+"1&n=10&fd=0&td=0&w=65&s=1"
                #print urls3
                i += 1
                #print urls3
                if requests.get(urls3).status_code == 404:
                    continue
                request3 = urllib2.Request(urls3)
                request3.add_header('User-Agent',
                               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
                page3 = urllib2.urlopen(request3).read()
                soup3 = BeautifulSoup(page3, 'html.parser')
                for noticias in soup3.find_all('div',attrs={'class':'texto-foto'}):
                    #print noticias
                    title = noticias.find('h4')
                    #print title.get_text()
                    if title != None:
                        url3 = title.find('a').get('href')
                        if not "http" in url3:
                            continue
                        try:
                            page4 = urllib2.urlopen(url3).read()
                            soup4 = BeautifulSoup(page4, 'html.parser')
                            stripdate = soup4.find('time', attrs={'itemprop': 'dateModified'})
                            if stripdate != None:
                                moment = try_parsing_date(stripdate.get_text().replace('CET', '').strip())
                                if moment == None:
                                    moment = try_parsing_date(stripdate.get_text().replace('CST', '').strip())
                            else:
                                moment = None
                            body=[]
                            for row in soup4.find_all('div',attrs={'itemprop':'articleBody'}):
                                for cuerpo in row.find_all('p'):
                                    body.append(cuerpo.get_text())
                            #print body
                        except:
                            continue
                        
                    searched_team = Equipo.objects.get(name=equipo.name)
                    loaded_noticia = Noticia.objects.filter(url=url3, team=searched_team)
        
                    if not loaded_noticia:
                        Noticia.objects.create(title=title.get_text(), body=body, moment=moment, url=url3, team=equipo)
        
                    else:
                        is_new = False
                        break
                if is_new == False:
                    break

def noticias_f1():
    f1 = Deporte.objects.get(name="Formula 1")
    f1_equipos = Equipo.objects.filter(sport=f1)
    is_new = True
    for equipo in f1_equipos:
        url = remove_accents(equipo.url)
        try:
            if requests.get(url).status_code == 404:
                continue
            page = urllib2.urlopen(url).read()
            soup = BeautifulSoup(page, 'html.parser')
            for noticias in soup.find_all('li',attrs={'class':['content-item','flex__item']}):
                title = noticias.find('h3')
                if title != None:
                    url2 = title.find('a').get('href')
                    if not "http" in url2:
                        continue
                    try:
                        page2 = urllib2.urlopen(url2).read()
                        soup2 = BeautifulSoup(page2, 'html.parser')
                        stripdate = soup2.find('time', attrs={'itemprop': 'dateModified'})
                        if stripdate != None:
                            moment = try_parsing_date(stripdate.get_text().replace('CET', '').strip())
                            if moment == None:
                                moment = try_parsing_date(stripdate.get_text().replace('CST', '').strip())
                        else:
                            moment = None
                        for row in soup2.find_all('div',attrs={'class':'row'}):
                            body = []
                            for cuerpo in row.find_all('p'):
                                body.append(cuerpo.get_text())
                    except:
                        continue
                            #print body
                searched_team = Equipo.objects.get(name=equipo.name)
                loaded_noticia = Noticia.objects.filter(url=url2, team=searched_team)

                if not loaded_noticia:
                    Noticia.objects.create(title=title.get_text(), body=body, moment=moment, url=url2, team=equipo)

                else:
                    is_new = False
                    break
            if is_new == False:
                break
        except:
            continue

def noticias_moto():
    mgp = Deporte.objects.get(name="Moto GP")
    equipos = Equipo.objects.filter(sport=mgp)
    is_new=True
    for equipo in equipos:
        url_mgp = equipo.url
        if "|" in url_mgp:
            url = url_mgp.split("|")[1]
        url = remove_accents(url_mgp.split("|")[1])
        if requests.get(url).status_code == 404:
            continue
        request2 = urllib2.Request(url)
        request2.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
        page2 = urllib2.urlopen(request2).read()
        soup2 = BeautifulSoup(page2, 'html.parser')
        i = 0
        if soup2.find('div',attrs={'class':'nav_paginacion'}):
            while i<3:
                equiponame = equipo.name
                if " " in equiponame:
                    equiponame = equiponame.replace(" ","+")
                    
                urls3 = "http://cgi.marca.com/buscador/archivo_marca.html?q="+remove_accents(equiponame)+"&t=1&i="+str(i)+"1&n=10&fd=0&td=0&w=65&s=1"
                #print urls3
                i += 1
                #print urls3
                if requests.get(urls3).status_code == 404:
                    continue
                request3 = urllib2.Request(urls3)
                request3.add_header('User-Agent',
                               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
                page3 = urllib2.urlopen(request3).read()
                soup3 = BeautifulSoup(page3, 'html.parser')
                for noticias in soup3.find_all('div',attrs={'class':'texto-foto'}):
                    #print noticias
                    title = noticias.find('h4')
                    #print title.get_text()
                    if title != None:
                        url3 = title.find('a').get('href')
                        if not "http" in url3:
                            continue
                        try:
                            page4 = urllib2.urlopen(url3).read()
                            soup4 = BeautifulSoup(page4, 'html.parser')
                            stripdate = soup4.find('time', attrs={'itemprop': 'dateModified'})
                            if stripdate != None:
                                moment = try_parsing_date(stripdate.get_text().replace('CET', '').strip())
                                if moment == None:
                                    moment = try_parsing_date(stripdate.get_text().replace('CST', '').strip())
                            else:
                                moment = None
                            body=[]
                            for row in soup4.find_all('div',attrs={'itemprop':'articleBody'}):
                                for cuerpo in row.find_all('p'):
                                    body.append(cuerpo.get_text())
                            #print body
                        except:
                            continue
                        
                    searched_team = Equipo.objects.get(name=equipo.name)
                    loaded_noticia = Noticia.objects.filter(url=url3, team=searched_team)
        
                    if not loaded_noticia:
                        Noticia.objects.create(title=title.get_text(), body=body, moment=moment, url=url3, team=equipo)
        
                    else:
                        is_new = False
                        break
                if is_new == False:
                    break

def noticias_mgp_as():
    mgp = Deporte.objects.get(name="Moto GP")
    equipos = Equipo.objects.filter(sport=mgp)
    is_new = True
    for equipo in equipos:
        if "|" in equipo.url:
            url = equipo.url.split("|")[0]
            if requests.get(url).status_code == 404:
                continue
            request2 = urllib2.Request(url)
            request2.add_header('User-Agent',
                           'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13')
            page2 = urllib2.urlopen(request2).read()
            soup2 = BeautifulSoup(page2, 'html.parser')
            for noticias in soup2.find_all('div', attrs={"class":"pntc-content"}):
                title = noticias.find('h2')
                url3 = noticias.find('a').get('href')
                stripdate = noticias.find('span',attrs={'class':'fecha'})
                if stripdate != None:
                    moment = try_parsing_date(stripdate.get_text())
                if not "http" in url3:
                    continue
                try:
                    page3 = urllib2.urlopen(url3).read()
                    soup3 = BeautifulSoup(page3, 'html.parser')
                    body=[]
                    row = soup3.find('div',attrs={'itemprop':'articleBody'})
                    if row != None:
                        for cuerpo in row.find_all('p'):
                            body.append(cuerpo.get_text())
                except:
                    continue
    
                searched_team = Equipo.objects.get(name=equipo.name)
                loaded_noticia = Noticia.objects.filter(url=url3, team=searched_team)
    
                if not loaded_noticia:
                    Noticia.objects.create(title=title.get_text(), body=body, moment=moment, url=url3, team=equipo)
    
                else:
                    is_new = False
                    break
            if is_new == False:
                break

def try_parsing_date(text):
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y','%d-%m-%Y','%d/%m/%Y %H:%M','%d-%m-%Y %H:%M'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
        
def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])