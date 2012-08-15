from . import txt2web
from . import prince

def main(text):
    html = txt2web.make_webpage(text)
    pdf  = prince.pdf_from_data(html)
    return pdf

if __name__ == "__main__":
    import fileinput, sys
    text = ''.join(fileinput.input())
    sys.stdout.buffer.write(main(text))