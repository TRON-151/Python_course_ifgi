# imports
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

# Namen des Districts abfragen 
district = '[% "Name" %]'

# in die URL einsetzen
url = f"https://de.wikipedia.org/wiki/{district}"

# anyeigen
view = QWebView()
view.load(QUrl(url))
view.show()
