import urllib2
from TorCtl import TorCtl
import BeautifulSoup
import urlparse
from time import sleep

proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
opener = urllib2.build_opener(proxy_support) 

inputUrl = "http://empresasdobrasil.com/empresas/belo-horizonte-mg/"
resultUrl = {inputUrl:False}

def processOneUrl(url):
    """fetch URL content and update resultUrl."""
    print "Processing... ",url
    error = True
    tentativa = 1
    while (error):
       try:
            print "Tentativa ",tentativa
            newId()
            proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
            urllib2.install_opener(opener)
            html_page = urllib2.urlopen(url)
            error = False 
       except urllib2.HTTPError:
            error = True
            tentativa = tentativa + 1
            

    current_urls = []

    soup = BeautifulSoup.BeautifulSoup(html_page)
    for link in soup.findAll('a'):
       #print link
       fullurl = urlparse.urljoin(url, link.get('href'))
       if fullurl.startswith(inputUrl):
           if (fullurl not in resultUrl):
    	        resultUrl[fullurl] = False
                current_urls.append(fullurl)
    resultUrl[url] = True       # set as crawled
    return current_urls

def get_html(url):
    try:
        newId()
        proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
        urllib2.install_opener(opener)
        return urllib2.urlopen(url).read()
    except:
        return ""

def newId():
    conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051)
    conn.send_signal("NEWNYM")

if __name__ == "__main__":
    current_urls = processOneUrl(inputUrl)
    companies_urls = []

    for url in current_urls:
        companies_urls += processOneUrl(url)
        #sleep(2)

    dir_data = "empresasbrasil/"
    i = 1
    fd_urls = open("urls_main.txt","w")
    for url in companies_urls:

        fd_urls.write("%s\n" % url)

        html_page = get_html(url)
        fd = open("%d.html" % i,"w")
        fd.write(html_page)
        fd.close()
        i = i+1
        #sleep(2)
    fd_urls.close()

