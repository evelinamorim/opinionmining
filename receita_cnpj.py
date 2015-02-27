from BeautifulSoup import BeautifulSoup
import requests
import Image, urllib2
from StringIO import StringIO
import scrapy
import os

# curl 'http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/captcha/gerarCaptcha.asp' -H 'Host: www.receita.fazenda.gov.br' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:35.0) Gecko/20100101 Firefox/35.0' -H 'Accept: image/png,image/*;q=0.8,*/*;q=0.5' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'DNT: 1' -H 'Referer: http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjreva_solicitacao2.asp' -H 'Cookie: ASPSESSIONIDQQBCSBAA=GHGKLNKDMMCBNHDFECDPFKCN' -H 'Connection: keep-alive'
#ASPSESSIONIDCQTDRBBB

captcha_req_link = 'http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/captcha/gerarCaptcha.asp'
host =  'www.receita.fazenda.gov.br'
accept = 'image/png,image/*;q=0.8,*/*;q=0.5'
accept_language = 'en-US,en;q=0.5'
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
referer = 'http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjreva_solicitacao2.asp'

headers={'User-Agent':user_agent,'Host':host,'Accept':accept,'Accept-Language':accept_language,\
         'Referer':referer,'Connection':'keep-alive','Accept-Encoding':'gzip,deflate'}

# url da consulta cnpj na receita federal
url_consulta = "http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjreva_solicitacao2.asp"

# criando a sessao para pegar resposta do servidor
sessao = requests.Session()
resposta = sessao.get(url_consulta)

cookie_header =  sessao.cookies.get_dict()
cookie_name = cookie_header.keys()[0]
cookie_key = cookie_header.values()[0]

cookie = resposta.request._cookies

command = "curl \'%s\' -H \'Host:%s\' -H \'User-Agent:%s\' -H \'Accept:%s\' -H \'Accept-Language:%s\'\
           --compressed -H \'DNT:1\' -H \'Referer:%s\' -H \'Cookie: %s=%s\' -H \'Connection: keep-alive\' > captcha.png" % \
          (captcha_req_link,host,user_agent,accept,accept_language,referer,str(cookie_name),str(cookie_key))

os.system(command)
#req = scrapy.http.Request(captcha_req_link,headers=headers,cookies=cookie_header)
#print req.body
#print dir(sessao.cookies)
import sys
sys.exit()
# resposta  do servidor para fazer a busca usando as tags
elementosResposta = BeautifulSoup(resposta.content)


#identificacao da imagem do captcha que esta no site
idImagem = ''

#procurando a imagem por todas as tages que tem id imgcaptcha
for i in elementosResposta.findAll(id='imgCaptcha'):
    #indiceInicio = str(i).rfind('guid=')
    indiceInicio = str(i).rfind('id=')
    indiceTermino =str(i).rfind('/>')
    idImagem = str(i) 
    #idImagem = idImagem[indiceInicio:indiceTermino].replace('guid=','').replace('"','')
    idImagem = idImagem[indiceInicio:indiceTermino].replace('id=','').replace('"','')

#print idImagem
#import sys
#sys.exit()
#pegando a criptografia da imagem para utilizar no metodo post
#viewState = ''
#for i in elementosResposta.findAll(id='viewstate'):
#    indiceInicio = str(i).rfind('value=')
#    indiceTermino = str(i).rfind('>')
#    viewState = str(i)
#    viewState = viewState[indiceInicio:indiceTermino].replace('value=','').replace('"','').replace('/','')

#atribuindo o valor do criptografia a uma variavel global
#view = viewState.strip()

print ">>>",idImagem,resposta.request._cookies

#url para fazer o dowload da imagem que esta no servidor
#image_url = 'http://www.receita.fazenda.gov.br/scripts/captcha/Telerik.Web.UI.WebResource.axd?type=rca&guid='+idImagem

#pegando a imagem propriamente dita
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(resposta.request._cookies))
urllib2.install_opener(opener)

#a imagem no buffer
#url_imagem = urllib2.urlopen(image_url)

#salvando a imagem
#i = Image.open(StringIO(url_imagem.read()))
#i.save('teste.jpg','JPG')
