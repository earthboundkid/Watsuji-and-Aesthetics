import re

#Finds all headings.
_RE_HEADINGS = re.compile(r'<h(\d)>(.*?)</h(\d)>')
_HEADER_T    = "{} id='header{}'{}"
_OL_START    = "<ol>\n"
_OL_STOP     = "</ol>\n"
_LINK_T      = "<a href='#header{}'>{}</a>\n"
_LI_T        = "<li><a href='#header{}'>{}</a></li>\n"

class Matchhandler:
    def __init__(self):
        self.matches = []
        self.count   = 0
    
    def __call__(self, matchobj):
        self.count += 1
        
        heading_full  = matchobj.group(0)
        heading_depth = matchobj.group(1)
        heading_text  = matchobj.group(2)
        
        self.matches.append( (int(heading_depth), heading_text, self.count) )
        
        #Shove an ID into the header.
        return _HEADER_T.format(heading_full[:3], self.count, heading_full[3:])
    
    def create_toc(self):
        return '\n'.join(_toc_helper(self.matches))



def _toc_helper(matches):
    
    old_depth = min_depth = 2
    
    for depth, text, id in matches:
        if depth > old_depth and depth > min_depth:
            yield _OL_START * (depth - max(old_depth, min_depth) )
            old_depth = depth
        elif depth < old_depth:
            yield _OL_STOP * (old_depth - max(depth, min_depth))
            old_depth = depth
        
        if depth > min_depth:
            yield _LI_T.format(id, text)
        else:
            yield _LINK_T.format(id, text)
    
    #Clean up remaining OLs
    yield _OL_STOP * max(old_depth - min_depth, 0)

def add_toc(text, replacestring="<toc />"):
    m = Matchhandler()
    text = _RE_HEADINGS.sub(m, text)
    toc = m.create_toc()
    
    return text.replace(replacestring, toc, 1)

