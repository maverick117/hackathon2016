#!/usr/bin/python2
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import json
import time

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"
                elif self.path == "/rec":
                    f = open(curdir + sep + 'data.json')
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()

                    return
		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

        def do_POST(self):
                if self.path!="/send":
			self.send_response(403)
			return
        	print "in post method"
        	self.data_string = self.rfile.read(int(self.headers['Content-Length']))
                #print self.data_string

        	self.send_response(200)
                
        	data = json.loads(self.data_string)
                data['Client_IP'] = self.client_address
                #data['time_of_post'] = time.time()

                #print data
        	#with open("post.json", "w") as outfile:
            	#	json.dump(data, outfile)
        	#print "{}".format(data)

                # TODO: Put POST data in database
                try:                
                    with open('data.json') as data_file:
                        database = json.load(data_file)
                except:
                    database = {}
                database[data["id"]] = data
                with open('data.json',mode='w') as data_file:
                    json.dump(database,data_file)

                self.analyze(database)
        	return

        def analyze(self,database):
            for d in database:
                pass 
			
			
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port' , PORT_NUMBER
	
	#Wait forever for incoming http requests
	server.serve_forever()

except KeyboardInterrupt:
	print '\nSIGINT received, shutting down the web server'
	server.socket.close()
	

