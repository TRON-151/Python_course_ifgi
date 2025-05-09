# imports
from qgis.PyQt.QtCore import QUrl # type: ignore
from qgis.PyQt.QtWebKitWidgets import QWebView # type: ignore

# request District names
district = '[% "Name" %]'

# create URL
url = f"https://de.wikipedia.org/wiki/{district}"

# display
view = QWebView()
view.load(QUrl(url))
view.show()