from . import run

MARKDOWN_PATH = ["/usr/local/bin/markdown"]

def txt2html(text):
    r = run.run(MARKDOWN_PATH, text)
    r = r.replace("&mdash;", "&#8202;&mdash;&#8202;") #Yay for hairspaces!
    return r

if __name__ == "__main__":
    import fileinput
    input = ''.join(fileinput.input())
    print(txt2html(input))