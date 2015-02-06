import urllib
import urllib2
from lxml import etree

#url = 'http://www.indeed.com.br/cmp'

def get_xml():
    url = 'http://api.indeed.com/ads/apisearch'

    #empresa='MRS'
    cidade ='belo horizonte,mg'
    pais = 'br'
    values = {'l':cidade,'publisher':4636456854731054,'v':2,'co':pais}
    data = urllib.urlencode(values)

    full_url = url + '?' + data
    #req = urllib2.Request(url)
    #print full_url
    response = urllib2.urlopen(full_url)

    html = response.read()
    
    print html

def process_xml(xml_file):
    tree = etree.parse(xml_file)
    q = [tree.getroot()]
    while (q!=[]):
        n = q.pop()
        q  = q + n.getchildren()
        if (n.tag == 'company'):
          print ">>",n.text


if __name__ == '__main__':
    #process_xml('vagasbelohorizonte.xml')
