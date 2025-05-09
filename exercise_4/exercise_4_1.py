# imports
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

# request District names
district = '[% "Name" %]'

# create URL
url = f"https://de.wikipedia.org/wiki/{district}"

# display
view = QWebView()
view.load(QUrl(url))
view.show()