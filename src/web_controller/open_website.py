import webbrowser

url_beginning = 'www.'

def Execute(url):
    if url[:4] != url_beginning :
        url = url_beginning + url

    webbrowser.get('windows-default').open(url, new=0)