import cherrypy
import os
from pathlib import Path


@cherrypy.expose
class RESTfulServicePOLYCY110(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, userID):
        with open(os.getcwd() + "/inputCommands/Commands-{}.txt".format(userID), "r") as f:
            strLines = f.readlines()
        print("User : " + userID + " is requesting a new command. Giving him :" + strLines[0] + "\n")

        if len(strLines) == 0:
            return "0"

        #Saving the files, skipping the first Line
        with open(os.getcwd() + "/inputCommands/Commands-{}.txt".format(userID), "w") as f:
            cpt = 0
            for line in strLines:
                if cpt == 0:
                    cpt += 1
                    continue
                f.write(line)
                cpt+= 1

        return strLines[0]


    @cherrypy.tools.accept(media='multipart/form-data')
    def POST(self, userID, commandID, time, file):

        size = 0
        Path(os.getcwd() + "/output/{}".format(userID)).mkdir(parents=True, exist_ok=True)
        with open(os.getcwd() + "/output/{}/{}-{}.txt".format(userID, commandID, time), "wb") as f:
            while True:
                data = file.file.read(8192)
                if not data:
                    break
                size += len(data)
                f.write(data)
        return "Thank you!"

    def PUT(self):
        return ""

    def DELETE(self):
        return ""


def main():
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8081,
                            'request.show_tracebacks': False
                            })
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(RESTfulServicePOLYCY110(), '/', conf)


if __name__ == "__main__":
    main()
