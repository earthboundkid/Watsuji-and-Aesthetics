HEADING_CHAR = "#"
TOC_MARKER = "<toc />"
SPAN = "%s<span id='hn_%s'>\N{ZERO WIDTH SPACE}</span>%s"
TOC_HEADER = ""

def make_toc(text,
            toc_marker=TOC_MARKER, 
            toc_header=TOC_HEADER, 
            heading_char=HEADING_CHAR, 
            span=SPAN):
    toc = TableOfContents(toc_marker, toc_header, heading_char, span)
    return toc(text)

class TableOfContents(object):
    def __init__(self, 
                toc_marker=TOC_MARKER, 
                toc_header=TOC_HEADER, 
                heading_char=HEADING_CHAR, 
                span=SPAN):
        self.toc_marker = toc_marker
        self.toc_header = toc_header
        self.heading_char = heading_char
        self.span = span
    
    def heading_catcher(self, line):
        for char in line:
            if char == self.heading_char:
                yield char
            else:
                return
    
    def heading_level(self, line):
        return sum(1 for char in self.heading_catcher(line))
    
    def heading_mapper(self, lines):
        for line in lines:
            if line.startswith(self.heading_char):
                yield line
    
    def toc_maker(self, keyed_headings):
        yield self.toc_header
        #In case someone requests a TOC, but there are no headings.
        if not keyed_headings:
            return
        base = keyed_headings[0][1]
        for key, depth, heading in keyed_headings:
            if depth == 1:
                s = "* &nbsp;\n%s* [%s](#hn_%s)"
            else:
                s = "%s1. [%s](#hn_%s)"
            yield s % ("\t" * (depth - base), 
                       heading.strip(self.heading_char), key)
    
    def get_keyed_headings(self, text):
        lines = text.splitlines()
        headings = list(self.heading_mapper(lines))
        depths = [self.heading_level(heading) for heading in headings]
        return list(zip(range(len(headings)), depths, headings))
    
    def __call__(self, text):
        if self.toc_marker in text: #Bail fast.
            beginning, _, text = text.partition(self.toc_marker)
            keyed_headings = self.get_keyed_headings(text)
            toc = '\n'.join(self.toc_maker(keyed_headings))
            for key, depth, heading in keyed_headings:
                marked = self.span % (heading[:depth], 
                    key, heading[depth:])
                text = text.replace(heading, marked, 1)
            text = "".join([beginning, self.toc_header, toc, text])
        return text

if __name__ == "__main__":
    import fileinput
    toc = TableOfContents()
    text = ''.join(fileinput.input())
    print(toc(text))