from core.kapp import Kapp
from core.httpResponse import HTTPResponse
import json

class NextPage(kcommand):
	nextPageHash = str(uuid.uuid4())
    
    def __init__(self):
        super(NextPage, self).__init__(
            "NextPage", self.nextPageHash)

class Dashboard(Kapp):
    name = "Dashboard"

    def iconCallback(self, kcommand):
        return HTTPResponse(content=self.getRes("icon.png"))
		
	def nextPageCallback(self, kcommand):
		#TODO
		
	def homeCallback(self, kcommand):
		# TODO: Replace with configurable HTTP path
        config = json.loads(self.getRes("dashboard.json"))
		
		start = config["start"]
		for p in config["pages"]:
			name = p["name"]
			meta = ""
			if "auto forward" in p:
				delay = 10
				if "delay" in p:
					delay = p["delay"]
				meta = '<meta http-equiv="Refresh" content="' + str(delay) + '; URL=' + NextPage().setParam("page", p["auto forward"]).toURL() + '" />'
			
			content = ""
			if "content" in p:
				for c in p["content"]:
					width = "20px"
					if "width" in c:
						width = c["width"]
					height = "20px"
					if "height" in c:
						height = c["height"]
						
					if c["type"] == "mdi":
						# TODO: load mdi icon properly: '<i class="mdi mdi-account-badge"></i>'
						content = content + '<img src="/res/'+ c["id"] +'.svg"style="position:absolute;width:'+height+';height:'+width+';top:'+ c["top"] +';left:'+c["left"]+';">'
					else if c["type"] == "text":
						content = content + '<p style="position:absolute;width:'+height+';height:'+width+';top:'+ c["top"] +';left:'+c["left"]+';">' + p["text"] +  '</p>'
		
        return HTTPResponse(content=self.getRes("dashboard.html").replace("$TITLE$", name).replace("$META$", meta).replace("$CONTENT$", content))

def register(appID, appPath, ctx):
    print("register " + Dashboard.name)
	app = Dashboard(appID, appPath, ctx)
	app.subscribe(NextPage(), app.nextPageCallback)
    return app
