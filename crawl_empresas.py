import urllib2
from TorCtl import TorCtl
import BeautifulSoup
import urlparse
import time
import random

proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
opener = urllib2.build_opener(proxy_support) 

inputUrl = "http://empresasdobrasil.com/empresas/belo-horizonte-mg/"
modelUrl = "http://empresasdobrasil.com/empresa"
resultUrl = {inputUrl:False}
headers={'User-Agent':'Googlebot'}

sleep_time = 300

def eligible_url(url):
    """
    For second crawler phase, test whether the url is eligible 
    for crawling
    """
    if (url!=inputUrl):
       pass
    else:
       return False

def processOneUrl(url):
    """fetch URL content and update resultUrl."""
    print "Processing... ",url
    error = True
    tentativa = 1
    sleep_local_time = 600
    while (error):
       try:
            print "Tentativa ",tentativa
            #newId()
            #proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
            #urllib2.install_opener(opener)
            request=urllib2.Request(url, None, headers)
            html_page = urllib2.urlopen(request)
            html_page_read = html_page.read()
            error = False 
            if ("Acesso - bloqueado" in  html_page_read):
                time.sleep(sleep_local_time)
                sleep_local_time += sleep_time
                error = True
       except urllib2.HTTPError:
            error = True
            tentativa = tentativa + 1
            
    print "Total time: ",sleep_local_time
    current_urls = []
    soup = BeautifulSoup.BeautifulSoup(html_page_read)
    list_links = soup.findAll('a')

    if (len(list_links)==0):
      print "Warning: No links detected!"
    else:
      pass
      #print list_links

    for link in list_links:
       #print link
       fullurl = urlparse.urljoin(url, link.get('href'))
       if fullurl.startswith(modelUrl):
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

def read_categories():
    file_c = "categorias_sep.txt"
    fd_c = open(file_c,"r")
    return map(lambda x: x.replace('\n','').replace('\'',''),fd_c.readlines())

if __name__ == "__main__":
    #current_urls = processOneUrl(inputUrl)
    current_urls = read_categories()
    #print current_urls
    companies_urls = []

    dir_data = "empresasbrasil/"
    i = 1
    
    for url in current_urls:
        companies_urls = processOneUrl(url)
        time.sleep(600 + random.randint(0,300))
        #print companies_urls
        #sleep(2)
        fd_urls = open("urls_main1.txt","a")

        for url in companies_urls:

            fd_urls.write("%s\n" % url)

            #html_page = get_html(url)
            #fd = open("%d.html" % i,"w")
            #fd.write(html_page)
            #fd.close()
            i = i+1
        fd_urls.close()

