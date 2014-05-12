import re
import json


def annotate(source, lang):
    """
    lang:
        Name of the source language.
    source:
        Souce code, including annotation hooks in comments

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
        'clojure': ';',

        # Functional
        'haskell': '--',

        # C-style (comment blocks not yet supported)
        'c': r'//',
        'c++': r'//',
        'java': r'//',

        # Other
        'html': '<!--',
        'assembly': ';'
    }

    annotations = {}
    anno_ids = []
    hook_pattern = re.compile(r'(@[0-9]+)')
    anno_pattern = re.compile(r'(^@[0-9]+\w*\{)')

    source = source.split("\n")  # Can now iterate over lines of source

    for lineno, line in enumerate(source):
        if re.search(anno_pattern, line):
            anno_block_start = lineno
            break  # we're at the end of the code; the annotations begin.

        # Obviously, this bit only works for inline comments.
        # No idea how I should support block comments (the line refs issue)
        comment_start = line.find(comment_chars[lang.lower()])

        if comment_start > -1:  # Line has a comment
            anno_match = re.search(hook_pattern, line[comment_start:])

            if anno_match:  # there's at least* one annotation hook

                # Get a list of hooks, strip the '@' from each
                line_anno_ids = list(
                        map(lambda x: x[1:], list(anno_match.groups()))
                        )
                print(line_anno_ids)

                for anno_id in line_anno_ids:
                    try:
                        anno_id = int(anno_id)  # TODO: mutable check?
                        print(anno_id)
                    except ValueError:
                        print("Annotation ID was not a number!")
                        raise

                    annotations[anno_id] = {"line": lineno}

                print(line_anno_ids)

                # Delete the hook from the line
                source[lineno] = "".join(re.split(hook_pattern, line))

                anno_ids += (line_anno_ids)
                print(anno_ids)

    # The annotation content has been found; we want to iterate over its
    # chars, not its lines, so we'll join it back together
    # TODO: does this work?
    anno_block = "".join(source[anno_block_start:]).strip()

    # And cut out the annotation content from the source
    source = source[:anno_block_start]

    # Whitespace match?
    while anno_block is not "":  # TODO: this should REALLY be done recursively
        block_id = int(anno_block[1:anno_block.find("{")])
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

        try:  # to add the current block to the dict of annotations
            annotations.update({  # update() will match id numbers
                block_id: json.decode(anno_block[len(str(block_id)):block_end])
                })

        except ValueError:
            print("Annotation is not a valid dict, or contains \
                    a malformed string")
            raise

        anno_block = anno_block[block_end:].strip()

    return source.join("\n"), annotations

# overlapping annos on a single line?
