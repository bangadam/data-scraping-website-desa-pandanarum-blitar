from typing import Optional
import bs4
from Constant.constants import Constants
import requests
from pprint import pprint
from fastapi import FastAPI

app = FastAPI()
request_session = requests.Session()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/artikel")
def all():
    url = Constants.API_HOST + '/index.php/first/index'
    res = request_session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    items = res.findAll('li', class_='artikel')
    data = []
    for item in items:
        title = item.find('h3').text
        dateTime = item.find('div', class_='kecil').text.replace('Administrator', '')
        img = item.find('img')['src'].replace('\t', '')
        link = item.find('h3').find('a')['href'].replace('\t', '')
        id = link.split("/artikel/")[1]
        data.append({
            'id': id,
            'title': title,
            'dateTime': dateTime,
            'img': str(img),
            'link': link
        })

    return {
        "status": 200,
        "data": data
   }

@app.get('/artikel/{id}')
def show(id: int):
    url = Constants.API_HOST + "/index.php/first/artikel/{}".format(id)
    pprint(url)
    res = request_session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    res = res.find('div', class_="artikel")
    title = res.find('h2').text.replace('\t', '')
    dateTime = res.find('h3').text.replace('Administrator', '')
    img = res.find('img')['src'].replace('\t', '')
    description = res.find('p').text
    data = {
        "title": title,
        "dateTime": dateTime,
        "img": img,
        "description": description
    }
    return {
        "status": 200,
        "data": data
    }

@app.get('/gallery')
def all():
    url = Constants.API_HOST + '/index.php/first/gallery'
    res = request_session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    items = res.find('ul', class_="thumbnail").findAll('li')
    data = []
    for item in items:
        thumbnail = item.find('img')['src'].replace('\t', '')
        albumTitle = item.find('div', class_="title").text
        id = item.find('div', class_="title").find('a')['href'].split('sub_gallery/')[1]
        data.append({
            "id": id,
            "thumbnail": thumbnail,
            "albumTitle": albumTitle
        })
    return {
        "status": 200,
        "data": data
    }

@app.get('/sub-gallery/{galleryId}')
def sub_gallery(galleryId: int):
    url = Constants.API_HOST + "/index.php/first/sub_gallery/{}".format(galleryId)
    res = request_session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    items = res.find('div', id="contentcolumn").find('ul', class_="thumbnail").findAll('li')
    data = []
    for item in items:
        img = item.find('img')['src'].replace('\t', '')
        title = item.find('div', class_="title").text
        data.append({
            "title": title,
            "img": img
        })

    return {
        "status": 200,
        "data": data
    }

@app.get('/layanan-desa')
def all():
    url = Constants.API_HOST + '/index.php/first/kategori/8'
    res = request_session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    items = res.findAll('li', class_='artikel')
    data = []
    for item in items:
        title = item.find('h3').text
        dateTime = item.find('div', class_='kecil').text.replace('Administrator', '')
        img = item.find('img')['src'].replace('\t', '')
        link = item.find('h3').find('a')['href'].replace('\t', '')
        id = link.split("/artikel/")[1]
        data.append({
            'id': id,
            'title': title,
            'dateTime': dateTime,
            'img': str(img),
            'link': link
        })

    return {
        "status": 200,
        "data": data
   }

@app.get('/layanan-desa/{id}')
def show(id: int):
    url = Constants.API_HOST + "/index.php/first/artikel/{}".format(id)
    res = request_session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    res = res.find('div', class_="artikel")
    title = res.find('h2').text.replace('\t', '')
    dateTime = res.find('h3').text.replace('Administrator', '')
    img = res.find('img')['src'].replace('\t', '')
    description = res.find('div', class_="teks").text
    data = {
        "title": title,
        "dateTime": dateTime,
        "img": img,
        "description": description
    }
    return {
        "status": 200,
        "data": data
    }

@app.get('/profile-desa')
def show():
    url = Constants.API_HOST + "/index.php/first/artikel/32"
    res = request_session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    item = res.find('div', class_="teks").text.replace('\n', '')
    return {
        "status": 200,
        "data": item
    }


def organisasiData(organisasi: str):
    result = 0;
    ## Struktur Organisasi
    if(organisasi == "strukturOrganisasi"):
        result = 151
    ## Struktur Kartar
    elif(organisasi == "kartar"):
        result = 152
    ## Struktur Badan Permusyawaratan
    elif (organisasi == "badanPermusyawaratan"):
        result = 153
    ## Struktur BUMIDESA
    elif (organisasi == "bumiDesa"):
        result = 155
    ## Visi Misi
    elif (organisasi == "visiMisi"):
        result = 8

    return result

@app.get('/organisasi/{organisasi}')
def show(organisasi: str):
    organisasiId = organisasiData(organisasi)
    url = Constants.API_HOST + "/index.php/first/artikel/{}".format(organisasiId)
    res = request_session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')

    if (organisasiId == 8):
        item = res.find('div', class_="teks").text
    else:
        item = res.find('div', id="contentcolumn").find('img')['src'].replace('\t', '')

    return {
        "status": 200,
        "data": item
    }


def getDataStatistikType(type):
    result = None;
    ## Data Pekerjaan
    if(type == "pekerjaan"):
        result = 1
    ## Data Pendidikan
    elif(type == "pendidikan"):
        result = 0
    ## Data Agama
    elif (type == "agama"):
        result = 3

    return result


@app.get('/data-statistik/{type}')
def all(type: str):
    typeId = getDataStatistikType(type)
    url = Constants.API_HOST + "/index.php/first/statistik/{}".format(typeId)
    res = request_session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    items = res.select('.box-danger+ .box-danger .box-body')[0].findAll('tr')
    data = []
    for item in items:
        col = item.findAll('td')
        if len(col) != 0:
            no = col[0].getText()
            kelompok = col[1].getText()
            nJumlah = col[2].getText()
            percentJumlah = col[3].getText()
            nMale = col[4].getText()
            percentMale = col[5].getText()
            nFemale = col[6].getText()
            percentFemale = col[7].getText()
            data.append({
                "no": no,
                "kelompok": kelompok,
                "nJumlah": nJumlah,
                "percentJumlah": percentJumlah,
                "nMale": nMale,
                "percentMale": percentMale,
                "nFemale": nFemale,
                "percentFemale": percentFemale
            })

    return {
        "status": 200,
        "data": data
    }

@app.get('/data-administrasi')
def all():
    url = Constants.API_HOST + "/index.php/first/statistik/{}".format(15)
    res = request_session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    items = res.select('#contentcolumn .box-danger .box-body')[0].findAll("tr")

    data = []
    for item in items:
        col = item.findAll('td')
        if len(col) != 0:
            no = col[0].getText()
            namaDusun = col[1].getText()
            kepalaDusun = col[2].getText()
            jumlahRT = col[3].getText()
            jumlahKK = col[4].getText()
            jiwa = col[5].getText()
            jumlahLaki = col[6].getText()
            jumlahPerempuan = col[7].getText()
            data.append({
                "no": no,
                "namaDusun": namaDusun,
                "kepalaDusun": kepalaDusun,
                "jumlahRT": jumlahRT,
                "jumlahKK": jumlahKK,
                "jiwa": jiwa,
                "jumlahLaki": jumlahLaki,
                "jumlahPerempuan": jumlahPerempuan
            })

    return {
        "status": 200,
        "data": data
    }

@app.get('/kontak')
def show():
    url = Constants.API_HOST + "/index.php/first/artikel/36"
    res = request_session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    item = res.find('div', class_="teks").text
    return {
        "status": 200,
        "data": item
    }


def getFormId(type):
    result = 0;
    if (type == "keberatan"):
        result = 139
    elif (type == "pemberitahuan-tertulis"):
        result = 140
    elif (type == "penolakan-informasi"):
        result = 142

    return result


@app.get('/form/{type}')
def show(type: str):
    typeId = getFormId(type)
    url = Constants.API_HOST + "/index.php/first/artikel/{}".format(typeId)
    res = request_session.get(url)
    res = bs4.BeautifulSoup(res.content, 'html.parser')
    item = res.find('div', class_="teks").text
    link = res.select('p a')[0]['href']
    pprint(link)
    return {
        "status": 200,
        "data": {
            "description": item,
            "link": link.replace('\t', '')
        }
    }