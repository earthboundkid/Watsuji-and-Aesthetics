import re

#Finds all headings.
_RE_HEADINGS = re.compile(r'<h(\d)( class=(.*?))*?>(.*?)</h(\d)>')
#(r'<h(\d)>(.*?)</h(\d)>')

#Templating strings.
_make_header    = "{} id='header{}'{}".format
_tab = "\t{}".format
_link_no_class = "\t<a href='#header{}'>{}</a>".format
_link_w_class = "\t<a href='#header{}' class={}>{}</a>".format

class Matchhandler:
    def __init__(self):
        self.matches = []
        self.count   = 0
    
    def __call__(self, matchobj):
        
        self.count += 1
        
        heading_full  = matchobj.group(0)
        heading_depth = int(matchobj.group(1))
        heading_class = matchobj.group(3)
        heading_text  = matchobj.group(4)
        
        if heading_class is None:
            link_text = _link_no_class(self.count, heading_text)
        else:
            link_text = _link_w_class(self.count, heading_class, heading_text)
        
        
        self.matches.append( (heading_depth, link_text) )
        
        #Shove an ID into the header.
        return _make_header(heading_full[:3], self.count, heading_full[3:])
    
    def create_toc(self):
        matches = self.matches[::-1]
        return '\n'.join(_node(matches, 2))


def _node(matches, node_depth):
    yield "<ol>"
    while True:
        if not matches: break
        depth, text = matches.pop()
        
        if depth < node_depth:
            matches.append( (depth, text) )
            break
        
        elif depth > node_depth:
            yield "\t<li>"
            matches.append( (depth, text) )
            for output in _node(matches, depth):
                yield _tab(output)
            yield "\t</li>"
        
        else: #equal depth
            yield "\t<li>"
            yield text
            
            #We need to look ahead before closing the list item
            
            if matches:
                depth, text = matches.pop()
                matches.append( (depth, text) )
                if depth > node_depth:
                    for output in _node(matches, depth):
                        yield _tab(output)
            
            yield "\t</li>"
    
    yield "</ol>"

def add_toc(text, replacestring="<toc />"):
    m = Matchhandler()
    text = _RE_HEADINGS.sub(m, text)
    toc = m.create_toc()
    
    return text.replace(replacestring, toc, 1)

