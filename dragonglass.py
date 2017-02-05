from bottle import *
import hashlib
import time
import sqlite3

db = {'test':'pass', 'anothertest': 'passaswell'}
current_milli_time = lambda: int(round(time.time() * 1000))


@get('/')
def index():
	return template("index", title = "dragonglass")


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='/home/zython/dragonglass/static/')

@get('/id/<id>')
def getFromID(id):
	return template("id", filltext=retrieveText(id), ID=id, title="Your dragonglass from: TODO")


@post('/')
def submit():
	postdata = request.body.read()
	textbody = request.forms.get("textbody")
	print postdata
	if len(textbody) == 0:
		redirect("/")
	else:
		redirectvalue = storeText(textbody)
		redirect("/id/"+redirectvalue)

def retrieveText(id):
	value = db.get(id)
	return value


#Hashes the Passed String with a current timestamp in miliseconds
def stringToHash(string):
	timestamp = current_milli_time()
	hashvalue = hashlib.sha1(string+str(timestamp)).hexdigest()
	return hashvalue




#TODO avoid collision
#https://www.tutorialspoint.com/sqlite/sqlite_python.htm
def storeText(string):
	hashstring = stringToHash(string)
	db[hashstring] = string
	print hashstring
	print string
	return hashstring

def main():
	conn = sqlite3.connect('dragondata.db')
	print conn
	run(host='localhost', port=8080,debug="true")


if __name__ == '__main__':
	main()

