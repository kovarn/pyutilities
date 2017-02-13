from ipywidgets import HTML
import webbrowser


# author: Martin http://stackoverflow.com/a/40878617/7070842
def view(df):
    css = """<style>
    table { border-collapse: collapse; border: 3px solid #eee; }
    table tr th:first-child { background-color: #eeeeee; color: #333; font-weight: bold }
    table thead th { background-color: #eee; color: #000; }
    tr, th, td { border: 1px solid #ccc; border-width: 1px 0 0 1px; border-collapse: collapse;
    padding: 3px; font-family: monospace; font-size: 10px }</style>
    """
    s = '<script type="text/Javascript">'
    s += 'var win = window.open("", "Title", "toolbar=no, location=no, directories=no, status=no, ' \
         'menubar=no, scrollbars=yes, resizable=yes, width=780, height=200, ' \
         'top="+(screen.height-400)+", left="+(screen.width-840));'
    s += 'win.document.body.innerHTML = \''
    # s += df.to_html().replace("\n", '\\') + '\';'
    s += '{css}<div id="df">{df}</div>\';'.format(css=css, df=df.to_html()).replace("\n", '\\')
    s += '</script>'

    return HTML(s)


def view_in_tab(df):
    df.to_html("frame.html")
    url = "http://localhost:8888/files/notebook/frame.html"
    webbrowser.open(url, new=2)


def update_view(df):
    s = '<script type="text/Javascript">'
    s += 'win.document.getElementById("df").innerHTML = \'' + df.to_html().replace("\n", '\\') + '\';'
    s += '</script>'
    return HTML(s)
