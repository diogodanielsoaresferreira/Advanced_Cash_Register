#!/usr/bin/python
# coding= utf-8

# Diogo Daniel Soares Ferreira
# Escuteiros - Praia da Barra, 2015
# Aplicação para gestão de produtos das sardinhadas
	
# Aplicação principal
# Programa desenhado para Python 2.x

import sqlite3
import os, os.path
import cherrypy
import sys
import json
from datetime import datetime

#cria as tabelas da base de dados, senão existirem
#criação da conexão ao ficheiro da base de dados e construção do objecto de pesquisa
con = sqlite3.connect('sardinhadadb.db')
cur = con.cursor()
reload(sys)
sys.setdefaultencoding('utf8')

#cria tabela com informação de produtos (se não existir)
cur.execute('''CREATE TABLE IF NOT EXISTS products (prod_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, pric REAL)''')

#cria tabela com informação de registos de venda
cur.execute('''CREATE TABLE IF NOT EXISTS sell (id INTEGER PRIMARY KEY AUTOINCREMENT, day TEXT, prod_name Text, quant INTEGER, pric Real)''')

#cria tabela com registos de pessoas por dia
cur.execute('''CREATE TABLE IF NOT EXISTS person (id INTEGER PRIMARY KEY AUTOINCREMENT, day TEXT)''')


class Root(object):

	@cherrypy.expose
	#devolve a página incial
	def index(self):
		
		cherrypy.response.headers['Content-Type'] = 'text/html'
		return open('interface/index.html','r').read()

	@cherrypy.expose
	#apresenta o nome dos produtos existentes e o seu preço
	def listProd(self):

		con = sqlite3.connect('sardinhadadb.db')
		cur = con.cursor()

		cur.execute('''SELECT name, pric, prod_id FROM products ORDER BY name''')
		prodlist = cur.fetchall()

		#criação de uma string com sintaxe que permite a codificação em JSON
		returnjson =  '['
		for x in prodlist:
			returnjson+= '{"name":"'+str(x[0])+'",'+'"pric":'+str(x[1])+','+'"id":'+str(x[2])+'},'
		if len(returnjson)>1:
			returnjson=returnjson[:-1]
		returnjson+=']'

		#codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		#definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"
		#return simplejson.dumps(returnarray)
		#devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	# adiciona um novo produto à base de dados
	def newProd(self, name, price):

		name = name.decode('utf-8')
		price = float(price.decode('utf-8'))

		con = sqlite3.connect('sardinhadadb.db')
		cur = con.cursor()

		cur.execute('''INSERT INTO products (name, pric) VALUES (?,?)''',(name, price,))
		con.commit()

		#criação de uma string com sintaxe que permite a codificação em JSON
		returnjson =  '{"message": "O produto '+ name +' foi adicionado com sucesso."}'

		#codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		#definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		#devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	# apaga um produto da base de dados
	def delprod(self, id):
		id = id.decode('utf-8')

		con = sqlite3.connect('sardinhadadb.db')
		cur = con.cursor()

		print id
		# Eliminação de produto da base de dados
		cur.execute('''DELETE FROM products WHERE prod_id=?''',(id,))
		con.commit()

		# criação de uma string com sintaxe que permite a codificação em JSON
		returnjson =  '{"message": "O produto foi eliminado com sucesso."}'

		# codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		# definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		# devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	# Altera o preço de um produto
	def changePrice(self, id, price):
		id = id.decode('utf-8')
		pice = price.decode('utf-8')

		con = sqlite3.connect('sardinhadadb.db')
		cur = con.cursor()

		# Alteração do preço de produto da base de dados
		cur.execute('''UPDATE products SET pric=? WHERE prod_id=?''',(price,id,))
		con.commit()

		# criação de uma string com sintaxe que permite a codificação em JSON
		returnjson =  '{"message": "O preço do produto foi alterado com sucesso."}'

		# codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		# definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		# devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	# Adiciona uma venda à base de dados
	def sellProd(self, prod, quan, price):
		prod = prod.decode('utf-8')
		quan = quan.decode('utf-8')
		price = price.decode('utf-8')

		con = sqlite3.connect('sardinhadadb.db')
		cur = con.cursor()

		currentHour = datetime.now().hour
		currentDay = datetime.now().day
		currentMonth = datetime.now().month
		currentYear = datetime.now().year

		if currentHour>=0 and currentHour<6:
			if currentDay==1:
				if currentMonth==1:
					currentYear -= 1
					currentMonth = 12
					currentDay = 31
				else:
					currentMonth -= 1
					if currentMonth == 2:
						currentDay = 28
					elif currentMonth == 1 or currentMonth == 3 or currentMonth == 5 or currentMonth == 7 or currentMonth == 8 or currentMonth == 10 or currentMonth == 12:
						currentDay = 31
					else:
						currentDay = 30
			else:
				currentDay -=1

		currentDay = str(currentDay)
		if len(currentDay)==1:
			currentDay = '0'+str(currentDay)

		currentMonth = str(currentMonth)
		if len(currentMonth)==1:
			currentMonth = '0'+str(currentMonth)

		currentYear = str(currentYear)

		day = currentDay + "-" + currentMonth + "-" + currentYear

		cur.execute('''INSERT INTO sell (day, prod_name, quant, pric) VALUES (?,?,?,?)''',(day,prod, quan,price))
		con.commit()

		# criação de uma string com sintaxe que permite a codificação em JSON
		returnjson =  '{"message": "O produto vendido com sucesso."}'

		# codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		# definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		# devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	# Adiciona um cliente
	def addClient(self):

		con = sqlite3.connect('sardinhadadb.db')
		cur = con.cursor()

		currentHour = datetime.now().hour
		currentDay = datetime.now().day
		currentMonth = datetime.now().month
		currentYear = datetime.now().year

		if currentHour>=0 and currentHour<6:
			if currentDay==1:
				if currentMonth==1:
					currentYear -= 1
					currentMonth = 12
					currentDay = 31
				else:
					currentMonth -= 1
					if currentMonth == 2:
						currentDay = 28
					elif currentMonth == 1 or currentMonth == 3 or currentMonth == 5 or currentMonth == 7 or currentMonth == 8 or currentMonth == 10 or currentMonth == 12:
						currentDay = 31
					else:
						currentDay = 30
			else:
				currentDay -=1

		currentDay = str(currentDay)
		if len(currentDay)==1:
			currentDay = '0'+str(currentDay)

		currentMonth = str(currentMonth)
		if len(currentMonth)==1:
			currentMonth = '0'+str(currentMonth)

		currentYear = str(currentYear)

		day = currentDay + "-" + currentMonth + "-" + currentYear

		# Alteração do preço de produto da base de dados
		cur.execute('''INSERT INTO person (day) VALUES (?)''',(day,))
		con.commit()

		# criação de uma string com sintaxe que permite a codificação em JSON
		returnjson =  '{"message": "O cliente foi adicionado com sucesso."}'

		# codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		# definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		# devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	# Devolve dias existentes na base de dados
	def getDays(self):

		con = sqlite3.connect('sardinhadadb.db')
		cur = con.cursor()

		cur.execute('''SELECT day FROM person''')
		days = cur.fetchall()

		divdays = []

		for x in days:
			if not(x in divdays):
				divdays.append(x)

		#criação de uma string com sintaxe que permite a codificação em JSON
		returnjson =  '['
		for x in divdays:
			returnjson+= '{"day":"'+str(x[0])+'"},'
		if len(returnjson)>1:
			returnjson=returnjson[:-1]
		returnjson+=']'

		# codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		# definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		# devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	# Recebe um dia e devolve o produto com o seu lucro e a quantidade vendida nesse dia
	def getLucDay(self, day):
		day = day.decode('utf-8')

		con = sqlite3.connect('sardinhadadb.db')
		cur = con.cursor()

		if not(day=="Todos os dias"):
			cur.execute('''SELECT prod_name, quant, pric FROM sell WHERE day=(?)''',(day,))
		else:
			cur.execute('''SELECT prod_name, quant, pric FROM sell''')
		sell = cur.fetchall()

		prod = []
		quant = {}
		prec = {}
		for x in sell:
			if not(x[0] in prod):
				prod.append(x[0])

		for x in prod:
			quant[x] = 0
			prec[x] = 0

		for x in sell:
			quant[x[0]] += x[1]
			prec[x[0]] += x[2]

		#criação de uma string com sintaxe que permite a codificação em JSON
		returnjson =  '['
		for x in prod:
			returnjson+= '{"prod":"'+str(x)+'","quant":"'+str(quant[x])+'","price":"'+str(prec[x])+'"},'
		if len(returnjson)>1:
			returnjson=returnjson[:-1]
		returnjson+=']'

		# codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		# definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		# devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	# Recebe um dia e devolve o número de clientes nesse dia
	def getC(self, day):
		day = day.decode('utf-8')

		con = sqlite3.connect('sardinhadadb.db')
		cur = con.cursor()

		if not(day=="Todos os dias"):
			cur.execute('''SELECT id FROM person WHERE day=(?)''',(day,))
		else:
			cur.execute('''SELECT id FROM person''')
		sell = cur.fetchall()

		i=0
		for x in sell:
			i+=1

		#criação de uma string com sintaxe que permite a codificação em JSON
		returnjson =  '[{"Pessoas":"'+str(i)+'"}]'

		# codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		# definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		# devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)

	@cherrypy.expose
	# apagar vendas
	def delProd(self):

		con = sqlite3.connect('sardinhadadb.db')
		cur = con.cursor()

		# Eliminação das tabelas da base de dados
		cur.execute('''DELETE FROM sell''')
		con.commit()

		cur.execute('''DELETE FROM person''')
		con.commit()

		# criação de uma string com sintaxe que permite a codificação em JSON
		returnjson =  '{"message": "As vendas foram eliminadas com sucesso."}'

		# codificação da variavel no formato JSON
		returnmessage = json.loads(returnjson)

		# definição do tipo de cabeçalho para a comunicaçao HTTP
		cherrypy.response.headers["Content-Type"] = "application/json"

		# devolução no formato JSON para comunicação com o Javascript
		return json.dumps(returnmessage)


if __name__ == '__main__':
	print "Pode aceder à interface Web através do endereço localhost:8080"

	cherrypy.server.socket_port = 8080
	cherrypy.server.socket_host = "0.0.0.0"

	current_dir = os.path.dirname(os.path.abspath(__file__))
	conf = {'/': {'tools.staticdir.root': current_dir},
					'/css': {	'tools.staticdir.on': True,
								'tools.staticdir.dir': 'interface/css'},
					'/js': {	'tools.staticdir.on': True,
								'tools.staticdir.dir': 'interface/js'},
					'/font-awesome': {	'tools.staticdir.on': True,
								'tools.staticdir.dir': 'interface/font-awesome'},
					'/images': {'tools.staticdir.on': True,
								'tools.staticdir.dir': 'interface/images'},
					'/add.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/interface/add.html'},
					'/dev.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/interface/dev.html'},
					'/index.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/interface/index.html'},
					'/graph.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/interface/graph.html'},
					'/sell.html':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/interface/sell.html'},
					'/favicon.ico':{'tools.staticfile.on': True,
								'tools.staticfile.filename': current_dir+'/interface/images/favicon.ico'}
			}
	cherrypy.tree.mount(Root(),"/",conf)
	cherrypy.engine.start()
	cherrypy.engine.block()
