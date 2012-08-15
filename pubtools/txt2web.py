#!/usr/local/bin/python3
"""Makes HTML from plain text using Markdown and some custom stuff.
"""

from . import footnoter as f
from . import markdown as m
#from . import toc_maker as t
from os import path

DEFAULT_PATH = path.dirname(path.abspath(__file__))

DEFAULT_METADATA = {
    "lineheight": "2",
    "title": "Untitled",
    "subject": "",
    "keywords": "",
    "author": "Carl M. Johnson",
    "templatefile": path.join(DEFAULT_PATH, "template.html"),
    "cssfile": path.join(DEFAULT_PATH, "style.css"),
    "bodyclass": "prince",
    "lang": "en",
}

def make_webpage(text, return_metadata=False, cite=None):
    #do all the normal stuff
    text, metadata = prepare_html(text, True, cite)
    
    #make it into a full html file
    text = html_template(text, metadata)
    
    return (text, metadata) if return_metadata else text

def prepare_html(text, return_metadata=False, cite=None):
    #HACK so that daggers work as footnote placeholders.
    text = text.replace("\n\N{dagger}", "\n[^]:")
    text = text.replace("\N{dagger}", "[^]")
    
    #make text footnote friendly
    if cite is not None:
        text = f.insert_footnotes(text, cite=cite)
    else:
        text = f.insert_footnotes(text)
    
    #get title and other metadata
    text, metadata = metadata_getter(text)
    
    #Don't do this anymore.
    #insert table of contents
    #text = t.make_toc(text, toc_marker="<toc />", toc_header="")
    
    #markdown text
    text = m.txt2html(text)
    
    return (text, metadata) if return_metadata else text

def metadata_getter(text):
    metadata = DEFAULT_METADATA.copy()
    #Bomb the BOM now!
    if text.startswith("\ufeff"):
        text = text[1:]
    
    lines = text.splitlines()
    n = None
    for n, line in enumerate(lines):
        words  = line.split()
        if not len(words) > 1:
            break
        if not words[0].endswith(":"):
            break
        key, value, value = line.partition(": ")
        key = key.lower().replace("_", "").replace("-", "")
        if not key in metadata:
            break
        metadata[key] = value

    #Empty document?
    if n is None:
        return "", metadata
    
    text = '\n'.join(lines[n:])
    #Add wordcount metadata
    metadata["keywords"] = ",".join(["Word count: %s, Line count: %s" 
        % (len(text.split()), len(list(filter(None, lines))) - n), 
        metadata["keywords"]])
    return text, metadata

def html_template(body, metadata):
    try:
        template_text = open(metadata["templatefile"]).read()
    except IOError:
        error = "<html><body>Template file ('%r') not found.</body></html>"
        return  error % metadata["templatefile"]
    try:
        css = open(metadata["cssfile"]).read()
    except IOError:
        error = "<html><body>CSS file ('%r') not found.</body></html>"
        return  error % metadata["cssfile"]
    
    from string import Template
    metadata = metadata.copy() #no side effects, i guess
    metadata["body"] = body
    metadata["css"] = Template(css).safe_substitute(metadata)
    r = Template(template_text).safe_substitute(metadata)
    return r.encode("UTF-8")

if __name__ == "__main__":
    import sys, fileinput
    text = ''.join(fileinput.input())
    sys.stdout.buffer.write(make_webpage(text))
