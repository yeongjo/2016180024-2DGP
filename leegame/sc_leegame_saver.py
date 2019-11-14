from krita import (krita, InfoObject)
import time

myTime = time.strftime('%y%m%d_%H%M%S', time.localtime(time.time()))

imagePath = str("G:/Projects/Python/2dgp/leegame/전기이태륜/"+myTime+".png")
doc = Krita.instance().activeDocument()
doc.exportImage(imagePath, InfoObject())
