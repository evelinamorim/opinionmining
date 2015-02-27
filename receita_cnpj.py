from BeautifulSoup import BeautifulSoup as bs
import requests
import Image, urllib2
from StringIO import StringIO

# curl 'http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/captcha/gerarCaptcha.asp' -H 'Host: www.receita.fazenda.gov.br' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:35.0) Gecko/20100101 Firefox/35.0' -H 'Accept: image/png,image/*;q=0.8,*/*;q=0.5' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'DNT: 1' -H 'Referer: http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjreva_solicitacao2.asp' -H 'Cookie: ASPSESSIONIDQQBCSBAA=GHGKLNKDMMCBNHDFECDPFKCN' -H 'Connection: keep-alive'

# url da consulta cnpj na receita federal
url_consulta = "http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjreva_solicitacao.asp"

# criando a sessao para pegar resposta do servidor
sessao = requests.Session()
resposta = sessao.get(url_consulta)

print resposta,sessao.cookies

cookie = resposta.request._cookies
# resposta  do servidor para fazer a busca usando as tags
elementosResposta = bs(resposta.content)

#identificacao da imagem do captcha que esta no site
idImagem = ''

#procurando a imagem por todas as tages que tem id imgcaptcha
for i in elementosResposta.findAll(id='imgcaptcha'):
    indiceInicio = str(i).rfind('guid=')
    indiceTermino =str(i).rfind('/>')
    idImagem = str(i) 
    idImagem = idImagem[indiceInicio:indiceTermino].replace('guid=','').replace('"','')

#pegando a criptografia da imagem para utilizar no metodo post
viewState = ''
for i in elementosResposta.findAll(id='viewstate'):
    indiceInicio = str(i).rfind('value=')
    indiceTermino = str(i).rfind('>')
    viewState = str(i)
    viewState = viewState[indiceInicio:indiceTermino].replace('value=','').replace('"','').replace('/','')

#atribuindo o valor do criptografia a uma variavel global
view = viewState.strip()

print ">>>",idImagem

#url para fazer o dowload da imagem que esta no servidor
#image_url = 'http://www.receita.fazenda.gov.br/scripts/captcha/Telerik.Web.UI.WebResource.axd?type=rca&guid='+idImagem

#pegando a imagem propriamente dita
#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(resposta.request._cookies))
#urllib2.install_opener(opener)

#a imagem no buffer
#url_imagem = urllib2.urlopen(image_url)

#salvando a imagem
#i = Image.open(StringIO(url_imagem.read()))
#i.save('teste.jpg','JPG')
