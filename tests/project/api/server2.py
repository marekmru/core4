from core4.api.v1.application import CoreApiContainer
from core4.api.v1.request.standard.static import CoreStaticFileHandler
import project.api.server1

class ProjectServer2(CoreApiContainer):
    root = "/another"
    rules = [
        (r"/req1", project.api.request.TestHandler1),
        (r"/stat2/(.*)", CoreStaticFileHandler, {
            "path": "./html",
            "inject": {
                "testvar": "variable hello from ProjectServer2",
                "timer": "bla",
            },
            "default_filename": "default.html",
            "protected": True
        })
    ]


