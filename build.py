#!/Library/Frameworks/Python.framework/Versions/3.2/bin/python3

import os
import pubtools.txt2web as t2w
from pubtools.prince import pdf_from_file as prince
from pubtools.toc_hard import add_toc
import string

DEFAULT_PATH = os.path.dirname(os.path.abspath(__file__))

def make_filepath(filename, path=DEFAULT_PATH):
    return os.path.join(path, filename)


METADATA =  {
    "lineheight": "2",
    "title": "Dissertation: Watsuji Tetsurō and the Subject of Aesthetics",
    "subject": "",
    "keywords": "",
    "author": "Carl M. Johnson",
    "templatefile": make_filepath("pubtools/template.html"),
    "cssfile": make_filepath("pubtools/style.css"),
    "bodyclass": "prince",
    "lang": "en",
    }

HTML_FILENAME = "output/dissertation.html"
PDF_FILENAME = "output/dissertation.pdf"

#Make a translation dictionary to kill puncts and convert spaces
#For use in make_identifier
_TRANS = {ord(char): None for char in string.punctuation}
_TRANS[ord(" ")] = "_"


def make_identifier(filename):
    "string.Template won't accept $values with spaces and whatnot."
    
    #Chop off .md extension
    name = filename[:-3]
    
    #Get rid of punctuation and spaces
    name = name.translate(_TRANS)
    
    #Prepend an underbar
    return "_" + name 

def prepare_template_dict(filenames):
    for filename in filenames:
        with open(filename, encoding="UTF-8") as f:
            text = f.read()
        
        yield make_identifier(filename), t2w.prepare_html(text)

def create_template_dict(filenames):
    metadata = METADATA.copy() #no side effects, i guess
    metadata.update(prepare_template_dict(filenames))
    return metadata


def prep_webpage(template_dict):
    print("Reading in CSS file.")
    with open(template_dict["cssfile"], encoding="UTF-8") as f:
        css = f.read()
    
    print("Reading in template file.")
    with open(template_dict["templatefile"], encoding="UTF-8") as f:
        template_text = f.read()
    
    #Inlining CSS
    template_dict["css"] = string.Template(css).substitute(template_dict)
    
    t = string.Template(template_text)
    html = t.substitute(template_dict)
    
    #Add table of contents
    html = add_toc(html)
    
    return html

def get_filenames():
    return [fn for fn in os.listdir(DEFAULT_PATH) if fn.endswith(".md")]

def main():
    print("Processing files.")
    filenames = get_filenames()
    template_dict = create_template_dict(filenames)
    html = prep_webpage(template_dict)
    
    #Make filepaths from filenames
    html_filepath = make_filepath(HTML_FILENAME)
    pdf_filepath  = make_filepath(PDF_FILENAME)
    
    #Write out HTML
    print("Writing HTML.")
    with open(html_filepath, "w", encoding="UTF-8") as f:
        f.write(html)
    
    
    #Make PDF
    print("Writing PDF.")
    prince(html_filepath, pdf_filepath)
    
    #Done
    print("Done.")
    

if __name__ == "__main__":
    main()