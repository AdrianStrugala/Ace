import webbrowser

googleUrl = "http://google.com/?#q="

def Execute(phrase_to_search):
    webbrowser.get('windows-default').open(googleUrl + phrase_to_search, new=0)