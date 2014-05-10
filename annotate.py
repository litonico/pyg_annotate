import re
from ast import literal_eval


def annotate(lang, source):
    """
    Source including annotation hooks in comments

    ......# @0

    and annotations with the corresponding key

    @0{
    content: "This is my annotation",
    range: "3-5", (range, from char to char)
    options: (a dict of Bootstrap popover options)
    }

    Returns the source (with annotations and hooks stripped)
    and a dict of annotations (dicts) mapping ids to line
    nums, char ranges, and popover options.
    """

    annotations = {}
    hook_pattern = re.compile(r'@[0-9]+')
    anno_pattern = re.compile(r'^@[0-9]+\w*\{')
    
    source = source.split("\n")  # Can now iterate over lines of source

    for lineno, line in enumerate(source):
        if anno_pattern.match(line):
            anno_block_start = lineno
            break  # we're at the end of the code; the annotations begin

        comment_start = line.find(comment_chars[lang])

        anno_id = re.match(line[comment_start:],)[1:]

        # strip the '@', convert to int
        try:
            anno_id = int(anno_id)
        except ValueError:
            print("Annotation ID was not a number!")
            raise

        anno_ids += anno_id

    anno_block = source[anno_block_start:].join("\n")  # does this work?
    source = source[:anno_block_start]

    while anno_block is not "":  # TODO: this should REALLY be done recursively
        block_id = int(anno_block[anno_block.find("{"):])
        if block_id not in anno_ids:
            raise LookupError(
                "Annotation {0} has no corresponding hook!"
                .format(block_id))

        for index, char in enumerate(anno_block[1:]):  # chomp the '@'
            curlybrace_count = 1
            if curlybrace_count == 0:  # we've found the end of the annotation
                block_end = index
                break  # out of the for loop
            if char == '{':
                curlybrace_count += 1
            elif char == '}':
                curlybrace_count -= 1
        else:  # if the loop ends without breaking
            if curlybrace_count > 0:
                raise SyntaxError("Unbalaced curly braces in annotation")

        try:  # to add the current block to the list of annotations
            annotations[block_id] = \
                literal_eval(anno_block[len(str(block_id)):block_end])
        except ValueError:
            print("Annotation is not a valid Python dict, or contains \
                    a malformed string")
            raise

        anno_block = anno_block[block_end:]

    return annotations

comment_chars = {
    # Scripting
    'ruby': '#',
    'python': '#',
    'shell': '#',
    'make': '#',

    # Lisps
    'lisp': ';',
    'scheme': ';',
    'racket': ';',

    # C-style (comment blocks not yet supported)
    'c': r'//',
    'c++': r'//',
    'java': r'//',


    # Other
    'html': '<!--'

}
