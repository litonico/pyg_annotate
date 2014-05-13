from generate_annotations import annotate
from testcase import sourcestr

# print(annotate(sourcestr, "Python"))
source, anno = annotate(sourcestr, "Python")

print(source)
print(anno)
