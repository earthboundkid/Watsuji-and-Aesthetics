#!/usr/local/bin/python3

START_LINE = r'^\[\^(.*?)\]\:(.*?)$'
INNER = r'\[\^(.*?)\]'

FOOTNOTE_OVERWRITE_WARNING = "{WARNING FOOTNOTE OVERWRITING!}"
UNKNOWN_FOOTNOTE_WARNING = "{WARNING FOOTNOTE UNKNOWN!}"
CITATION_TEXT = "<aside id='footnote-%(id)s'>%(note)s</aside>"


class Footnote(object):
    def __init__(self, 
                 overwrite=FOOTNOTE_OVERWRITE_WARNING, 
                 unknown=UNKNOWN_FOOTNOTE_WARNING,
                 cite=CITATION_TEXT):
        self.overwrite_message = overwrite
        self.unknown_message = unknown
        self.citation_text = cite
        if hasattr(cite, "__call__"):
            self.citer = cite
        else:
            self.citer = None
        self.footnotes = {"ibid": "_Ibid_."}
        self.warnings = None
        self.ibidno = 0
        
        import re
        self.start_line = re.compile(START_LINE)
        self.inner = re.compile(INNER)
    
    def _dictmaker(self, match):
        key = match.group(1)
        value = match.group(2)
        if not key:
            key = self._count
            self._count += 1
        if not key in self.footnotes or key == "ibid":
            self.footnotes[key] = value
        else:
            self.warnings = True
            self.footnotes[key] += self.overwrite_message + value 
        return ''
    
    def citewrap(self, key):
        if key in self.footnotes:
            footnote = self.footnotes[key].strip()
        else:
            self.warnings = True
            footnote = self.unknown_message
        #Special case #ibid
        if key == "ibid":
            key += str(self.ibidno)
            self.ibidno += 1
        
        if self.citer is None:
            return self.citation_text % { "id": key, "note": footnote }
        else:
            return self.citer(key, footnote)
    
    def _cut_out_notes(self, match):
        key = match.group(1)
        if not key:
            key = self._count
            self._count += 1
        return self.citewrap(key)
    
    def footnote_inserter(self, lines):
        #use a list here, so we catch all the footnotes before processing
        self._count = 0
        lines = [self.start_line.sub(self._dictmaker, line) for line in lines]
        #put footnotes where the markers are.
        self._count = 0
        for line in lines:
            yield self.inner.sub(self._cut_out_notes, line)
    
    def __call__(self, text):
        if "[^" not in text: return text #Bail fast.
        
        text = '\n'.join(self.footnote_inserter(text.splitlines()))
        if self.warnings:
            text = ("Keywords: Bad footnotes\n"
                    "#Warning! Footnoting error(s) found!\n" + text)
        return text


def insert_footnotes(text, overwrite=FOOTNOTE_OVERWRITE_WARNING, 
    unknown=UNKNOWN_FOOTNOTE_WARNING, cite=CITATION_TEXT):
    footnote = Footnote(overwrite, unknown, cite)
    return footnote(text)


if __name__ == "__main__":
    import fileinput
    print(insert_footnotes(fileinput.input()))
