from pubtools import text2web as t2w
from pubtools.prince import pdf_from_data as prince
from string import Template

METADATA = {}

OUTPUT_FILE = "dissertation.pdf"

def make_template_dict(filenames):
    for filename in filenames:
        with open(filename) as f:
            text = f.read()
        
        yield filename, t2w.prepare_html(text)

def prep_webpage():
    metadata = METADATA.copy() #no side effects, i guess
    metadata.update(make_template_dict(filenames))
    
    metadata["css"] = Template(css).safe_substitute(metadata)
    
    r = Template(template_text).safe_substitute(metadata)
    
    return r.encode("UTF-8")

def make_pdf():
    html = prep_webpage()
    pdf  = prince(html)
    
    with open(OUTPUT_FILE, "wb") as f:
        f.write(pdf)