from pygments.filter import Filter
from pygments.token import Token


class AnnotationFilter(Filter):
    """
    `annotations` : A list of dicts, with the follwing properties:
    {
    'range': a tuple of the character range (5, 12) or "full_line"
    'content': the annotation's message
    'options': a dict of Bootstrap popover options

    }
    """

    def __init__(self, **options):
        Filter.__init__(self, **options)
        self.annotations = options["annotations"]

        # Make sure the annotations are sorted by line, then char- we then only
        # Need to check the first annotation, not all of them.
        self.annotations.sort(
            key=lambda anno: (anno["line"], anno["range"][0])
            )

        self.escape_html = {
            ord('&'): '&amp;',
            ord('<'): '&lt;',
            ord('>'): '&gt;',
            ord('"'): '&quot;',
            ord("'"): '&#39;',
        }

    def filter(self, lexer, stream):

        chars_on_line = 0
        lineno = 1  # lines, as we talk about them, are 1-indexed
        opened = False
        if self.annotations:
            annotation = self.annotations.pop(0)
        else:
            annotation = None

        for ttype, value in stream:

            if annotation:

                # The stuff required for a popover
                popover_data = \
                    'class="anno_popover" data-content="{0}" '\
                    .format(annotation['content'].translate(self.escape_html))

                # Options handling, if they exist
                try:
                    popover_options = annotation["options"]
                except:  # No options, use defaults
                    popover_data += \
                        'data-container="body" data-placement="top"'
                else:
                    for option_name, option in popover_options:
                        popover_data += 'data-{name}="{opt}" '.format(
                            name=option_name, opt=option
                            )

                anno_open = "<span {data}>".format(data=popover_data)

                # TODO: unsure of the cause of this, but the span before
                # The end of an annotation is supressed in the formatter.
                anno_close = "</span></span>"

                anno_line = annotation["line"]

                try:
                    anno_start, anno_end = annotation["range"]
                except ValueError:
                    if annotation["range"] == "full_line":
                        anno_start = 0
                        anno_end = None

                    else:
                        print("Annotation range is not valid- "
                              "should be a 2-tuple or 'full_line'")
                        raise

                if value == '\n':
                    chars_on_line = 1  # Compensates for Pygments
                    lineno += 1

                    # Close any annotations that are still open
                    if opened:
                        yield Token.Annotation, anno_close
                        chars_on_line += len(value)

                        if self.annotations:
                            annotation = self.annotations.pop(0)
                        opened = False

                    yield ttype, value  # Newline AFTER the closing annotation

                else:  # Not a newline
                    if not opened:
                        if anno_line == lineno and chars_on_line >= anno_start:
                            yield Token.Annotation, anno_open

                            yield ttype, value
                            chars_on_line += len(value)

                            opened = True
                        else:
                            yield ttype, value
                            chars_on_line += len(value)

                    else:  # Close the <span> tag
                        if anno_end is not None and chars_on_line > anno_end:
                            yield Token.Annotation, anno_close
                            # Move to the next annotation
                            if self.annotations:
                                annotation = self.annotations.pop(0)
                            opened = False

                            yield ttype, value
                            chars_on_line += len(value)
                        else:
                            yield ttype, value
                            chars_on_line += len(value)

            else:
                yield ttype, value
                chars_on_line += len(value)
