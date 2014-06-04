import re
from ast import literal_eval
from pyg_annotate.lib.language_data import comment_chars


def annotate(source, lexer_name):
    """
    lexer_name:
        Name of the source language.
    source:
        Souce code, including annotation hooks in comments

    ......# @0

    and annotations with the corresponding key

    @0{
        content: "This is my annotation",
        range: (3, 5),  # a tuple
        options: {}     # a dict of Bootstrap popover options
    }

    Returns the source (with annotations and hooks stripped)

    and a list of annotations (dicts) which have line
    nums, char ranges, and a dict of popover options.
    """

    annotations = {}
    anno_ids = []
    hook_pattern = re.compile(r'(@[0-9]+)')
    anno_pattern = re.compile(r'(^@[0-9]+\w*\{)')

    source = source.split("\n")  # Can now iterate over lines of source

    while source[0].isspace():  # Blank lines at the beginning?
        source = source[1:]

    for lineno, line in enumerate(source):
        if re.search(anno_pattern, line):
            anno_block_start = lineno
            break  # we're at the end of the code; the annotations begin.

        # Obviously, this bit only works for inline comments.
        # No idea how I should support block comments (the line refs issue)
        try:
            comment_start = line.find(comment_chars[lexer_name])
        except LookupError:
            print("Lexer's comment character not found– please modify "
                  "language_data.py")
            raise

        if comment_start > -1:  # Line has a comment
            anno_match = re.search(hook_pattern, line[comment_start:])

            if anno_match:  # there's at least one annotation hook

                # Get a list of hooks, strip the '@' from each
                line_anno_ids = list(
                    map(lambda x: int(x[1:]), list(anno_match.groups()))
                )

                for anno_id in line_anno_ids:
                    # Humans start line indices at 1
                    annotations[anno_id] = {"line": lineno+1}

                # Delete the hook from the line
                source[lineno] = re.sub(hook_pattern, "", line)

                # Check if the comment is empty; if it is, delete it.
                if not source[lineno][comment_start+1:].strip():
                    source[lineno] = source[lineno][:comment_start].rstrip()

                anno_ids += (line_anno_ids)

    # The annotation content has been found; we want to iterate over its
    # chars, not its lines, so we'll join it back together
    try:
        # If this fails, we know the annotation block doesn't exist
        anno_block = "".join(source[anno_block_start:]).strip()
    except:
        return '\n'.join(source), []

    # And cut out the annotation content from the source
    source = source[:anno_block_start]

    while anno_block is not "":  # This should REALLY be done recursively

        block_id = int(anno_block[1:anno_block.find("{")])
        if block_id not in anno_ids:
            raise LookupError(
                "Annotation {0} has no corresponding hook!"
                .format(block_id))

        curlybrace_count = 1

        # Used in list slices to chomp the '@' and the block_id (an int)
        start_offset = 1 + len(str(block_id))

        for index, char in enumerate(anno_block[start_offset+1:]):
            if curlybrace_count == 0:  # We've found the end of the annotation
                block_end = index + start_offset + 1  # to include the '}'
                break  # out of the for loop

            if char == '{':
                curlybrace_count += 1
            elif char == '}':
                curlybrace_count -= 1
        else:  # if the loop ends without breaking
            if curlybrace_count > 0:
                raise SyntaxError("Unbalaced curly braces in annotation")

        try:
            block_end
        except NameError:
            print("Annotation isn't formatted correctly! Make sure there's "
                  "a newline before your annotaton block.")
            raise

        try:  # to add the current block to the dict of annotations
            annotations[block_id].update(
                # append the anno data to the line number data
                literal_eval(anno_block[start_offset:block_end])
            )
        except ValueError:
            print("Annotation is not a valid dict, "
                  "or contains a malformed string")
            raise

        anno_block = anno_block[block_end:].strip()

    return '\n'.join(source), list(annotations.values())
