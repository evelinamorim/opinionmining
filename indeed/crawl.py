import urllib
import urllib2

url = 'http://www.indeed.com.br/cmp'

empresa=MRS
values = {'q':empresa}
data = urllib.urlencode(values)

full_url = url + '?' + data
#req = urllib2.Request(url)
print full_url
response = urllib2.urlopen(full_url)

html = response.read()

print html
