from bs4 import BeautifulSoup
import urllib2, re
from models import Equipo, Deporte, Noticia
from datetime import datetime

def populate_equipos_futbol():
    futbol = Deporte.objects.filter(name = "Futbol")
    futbol_url = "https://as.com/futbol/" + "|" + "http://www.marca.com/futbol.html?intcmp=MENUPROD&s_kw=futbol" + "|" + \
                 "http://www.estadiodeportivo.com/noticias-futbol/"
    if not futbol:
        futbol = Deporte.objects.create(name="Futbol", url = futbol_url)
    else:
        futbol = Deporte.objects.get(name = "Futbol", url = futbol_url)

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
            #print team.prettify()
            name = team.find('span', attrs={'class': 'escudo'}).get_text().strip()
            image = "http:" + team.find('img').get("src")
            country = team.find('span', attrs={'class': 'pais'}).get_text().strip()
            as_url = team.find('a', attrs={'class': "col-md-6 col-sm-6 col-xs-6 content-info-escudo"}).get("href")
            complete_as_url = "https://resultados.as.com/" + as_url

            useful_name = name.lower()

            if len(useful_name.split(" ")) > 1:
                marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.split(" ")[0].strip() + "+" \
                                + useful_name.split(" ")[1].strip() + "&b_avanzada="
            else:
                marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.strip() + "&b_avanzada="

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
    f1_url = "https://as.com/motor/formula_1.html?omnil=src-sab|http://www.marca.com/motor/formula1.html?intcmp=MENUPROD&s_kw=formula-1" \
             "|http://www.estadiodeportivo.com/motor/automovilismo/"
    f1 = Deporte.objects.filter(name="Formula 1")
    if not f1:
        f1 = Deporte.objects.create(name="Formula 1", url=f1_url)
    else:
        f1 = Deporte.objects.get(name="Formula 1", url=f1_url)

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
    url_moto = "https://as.com/tag/moto_gp/a/?omnil=src-sab|http://www.marca.com/motor/motogp.html?intcmp=MENUPROD&s_kw=moto-gp|" \
               "http://www.estadiodeportivo.com/motor/motociclismo/"
    moto_gp = Deporte.objects.filter(name="Moto GP")
    if not moto_gp:
        moto_gp = Deporte.objects.create(name="Moto GP", url =url_moto)
    else:
        moto_gp = Deporte.objects.get(name="Moto GP", url =url_moto)

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
    url_baloncesto = "https://as.com/baloncesto/|http://www.marca.com/baloncesto.html?intcmp=MENUPROD&s_kw=baloncesto|" \
                     "http://www.estadiodeportivo.com/noticias-baloncesto/"
    baloncesto = Deporte.objects.filter(name="Baloncesto")
    if not baloncesto:
        baloncesto = Deporte.objects.create(name="Baloncesto", url=url_baloncesto)
    else:
        baloncesto = Deporte.objects.get(name="Baloncesto",url=url_baloncesto)

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
                if len(useful_name.split(" ")) > 1:
                    marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.split(" ")[
                        0].strip() + "+" \
                                + useful_name.split(" ")[1].strip() + "&b_avanzada="
                else:
                    marca_url = "http://cgi.marca.com/buscador/archivo_marca.html?q=" + useful_name.strip() + "&b_avanzada="

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
    url_tenis="https://as.com/tenis/|http://www.marca.com/tenis.html?intcmp=MENUPROD&s_kw=tenis|" \
              "http://www.estadiodeportivo.com/noticias-tenis/"
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

                
def noticias_futbol():
    #TODO Coger la url desde la base de datos. En este caso "futbol.url" Una vez cogidas diferenciar cual es del as, de marca y de estadio deportivo
    #TODO Estas noticias unicamente van a servir para mostrarlas en la pantalla de inicio o cuando el usuario es anonimo, por tanto estas noticias
    #TODO no tienen ningun equipo asociado puesto que son "globales"
    #TODO Despues por cada equipo habra que hacer scrapping para almacenar todas las noticias referentes a dichos equipos. De esta forma el usuario
    #TODO podra acceder a sus noticias favoritas sin esperar tiempo de procesado.
    #TODO Para evitar que el poblado de noticias tarde tanto, el primer poblado realizarlo completo pero los demas limitar a que comprueben si hay
    #TODO noticias nuevas solo en la primera pagina. Para poblar la BBDD utilizar la misma forma que se usa en populate_deportes (actualizando la
    #TODO entrada en la base de datos y nunca eliminando y volviendo a crear)

    url= "http://www.marca.com/futbol.html"
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    for noticias in soup.find_all('li',attrs={'class':['content-item','flex__item']}):
        title = noticias.find('h3')
        if title != None:
            url2 = title.find('a').get('href')
            #print url2
            #print title.get_text()
            page2 = urllib2.urlopen(url2).read()
            soup2 = BeautifulSoup(page2, 'html.parser')
            stripdate = soup2.find(attrs={'class':['fecha','date','center col-md-4','panel-heading']}) 
            if stripdate != None:
                moment = try_parsing_date(stripdate.get_text().replace('CET','').strip())
                #print moment
                if moment == None:
                    moment = datetime.now()
            for row in soup2.find_all('div',attrs={'class':'row'}):
                for cuerpo in row.find_all('p'):
                    body = cuerpo.get_text()
                    #print body
                    Noticia.objects.create(title=title.get_text(),body=body, moment=moment, url=url2)
        #link = noticias.find_all('a',title = True)
        #print link

def noticias_tenis():
    url= "http://www.marca.com/tenis.html?intcmp=MENUPROD&s_kw=tenis"
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    for noticias in soup.find_all('li',attrs={'class':['content-item','flex__item']}):
        title = noticias.find('h3')
        if title != None:
            url2 = title.find('a').get('href')
            #print url2
            #print title.get_text()
            page2 = urllib2.urlopen(url2).read()
            soup2 = BeautifulSoup(page2, 'html.parser')
            stripdate = soup2.find(attrs={'class':['fecha','date','center col-md-4','panel-heading']}) 
            if stripdate != None:
                moment = try_parsing_date(stripdate.get_text().replace('CET','').strip())
                #print moment
            for row in soup2.find_all('div',attrs={'class':'row'}):
                for cuerpo in row.find_all('p'):
                    body = cuerpo.get_text()
                    #print body
                    Noticia.objects.create(title=title,body=body, moment=moment, url=url2)

def noticias_baloncesto():
    url= "http://www.marca.com/baloncesto.html?intcmp=MENUPROD&s_kw=baloncesto"
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    for noticias in soup.find_all('li',attrs={'class':['content-item','flex__item']}):
        title = noticias.find('h3')
        if title != None:
            url2 = title.find('a').get('href')
            #print url2
            #print title.get_text()
            page2 = urllib2.urlopen(url2).read()
            soup2 = BeautifulSoup(page2, 'html.parser')
            stripdate = soup2.find(attrs={'class':['fecha','date','center col-md-4','panel-heading']}) 
            if stripdate != None:
                moment = try_parsing_date(stripdate.get_text().replace('CET','').strip())
                #print moment
            for row in soup2.find_all('div',attrs={'class':'row'}):
                for cuerpo in row.find_all('p'):
                    body = cuerpo.get_text()
                    #print body
                    Noticia.objects.create(title=title,body=body, moment=moment, url=url2)

def noticias_f1():
    url= "http://www.marca.com/motor/formula1.html?intcmp=MENUPROD&s_kw=formula-1"
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    for noticias in soup.find_all('li',attrs={'class':['content-item','flex__item']}):
        title = noticias.find('h3')
        if title != None:
            url2 = title.find('a').get('href')
            #print url2
            #print title.get_text()
            page2 = urllib2.urlopen(url2).read()
            soup2 = BeautifulSoup(page2, 'html.parser')
            stripdate = soup2.find(attrs={'class':['fecha','date','center col-md-4','panel-heading']}) 
            if stripdate != None:
                moment = try_parsing_date(stripdate.get_text().replace('CET','').strip())
                #print moment
            for row in soup2.find_all('div',attrs={'class':'row'}):
                for cuerpo in row.find_all('p'):
                    body = cuerpo.get_text()
                    #print body
                    Noticia.objects.create(title=title,body=body, moment=moment, url=url2)

def noticias_moto():
    url= "http://www.marca.com/motor/motogp.html?intcmp=MENUPROD&s_kw=moto-gp"
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    for noticias in soup.find_all('li',attrs={'class':['content-item','flex__item']}):
        title = noticias.find('h3')
        if title != None:
            url2 = title.find('a').get('href')
            #print url2
            #print title.get_text()
            page2 = urllib2.urlopen(url2).read()
            soup2 = BeautifulSoup(page2, 'html.parser')
            stripdate = soup2.find(attrs={'class':['fecha','date','center col-md-4','panel-heading']}) 
            if stripdate != None:
                moment = try_parsing_date(stripdate.get_text().replace('CET','').strip())
                #print moment
            for row in soup2.find_all('div',attrs={'class':'row'}):
                for cuerpo in row.find_all('p'):
                    body = cuerpo.get_text()
                    #print body
                    Noticia.objects.create(title=title,body=body, moment=moment, url=url2)
                    
def try_parsing_date(text):
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y','%d-%m-%Y','%d/%m/%Y %H:%M','%d-%m-%Y %H:%M'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
