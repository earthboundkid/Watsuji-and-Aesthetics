import re

#Finds all headings.
_RE_HEADINGS = re.compile(r'<h(\d)>(.*?)</h(\d)>')
_HEADER_T    = "{} id='header{}'{}"
_OL_START    = "<ol>\n"
_OL_STOP     = "</ol>\n"
_OLI_START   = "<li><ol>\n"
_OLI_STOP    = "</ol></li>\n"
_LINK_T      = "<a href='#header{}'>{}</a>\n"
_LI_T        = "<li><a href='#header{}'>{}</a></li>\n"

class Matchhandler:
    def __init__(self):
        self.matches = []
        self.count   = 0
    
    def __call__(self, matchobj):
        
        
        heading_full  = matchobj.group(0)
        heading_depth = int(matchobj.group(1))
        heading_text  = matchobj.group(2)
        
        #Special case the title page.
        if heading_depth == 1:
            return heading_full
        
        self.count += 1
        
        self.matches.append( (heading_depth, heading_text, self.count) )
        
        #Shove an ID into the header.
        return _HEADER_T.format(heading_full[:3], self.count, heading_full[3:])
    
    def create_toc(self):
        return '\n'.join(_toc_helper(self.matches))



def _toc_helper(matches):
    yield _OL_START
    old_depth = min_depth = 2
    
    for depth, text, id in matches:
        if depth > old_depth and depth > min_depth:
            yield _OLI_START * (depth - max(old_depth, min_depth) )
            old_depth = depth
        elif depth < old_depth:
            yield _OLI_STOP * (old_depth - max(depth, min_depth))
            old_depth = depth
        
        yield _LI_T.format(id, text)
    
    #Clean up remaining OLs
    yield _OL_STOP * max(old_depth - min_depth, 0)
    
    yield _OL_STOP

def add_toc(text, replacestring="<toc />"):
    m = Matchhandler()
    text = _RE_HEADINGS.sub(m, text)
    toc = m.create_toc()
    
    return text.replace(replacestring, toc, 1)

