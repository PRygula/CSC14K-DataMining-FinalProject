import polyglot
from polyglot.text import Text

blob = "we will meet at eight on Thursday morning"

text = Text(blob)
print text.pos_tags
print "-" * 30
print text.words[0].pos_tag
if text.words[0].pos_tag == "PRON":
	print "yayyyyyyy"
print "-" * 30
print text
