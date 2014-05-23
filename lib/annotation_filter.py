from pygments.filter import Filter
from pygments.token import Token
# from pyg_annotate.lib.generate_annotations import annotate


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

    def filter(self, lexer, stream):
        anno_open = "<span>OPEN!</span>"  # for testing
        anno_close = "<span>CLOSE!</span>"

        chars_on_line = 0
        lineno = 0
        opened = False
        annotation = self.annotations.pop(0)

        for ttype, value in stream:
            chars_on_line += len(value)

            if self.annotations:
                # popover_options = annotation["options"]
                # # The stuff required for a popover
                # popover_data = 'data-toggle="popover" '
                # for option_name, option in popover_options:
                #     popover_data += 'data-{name}="{opt}" '.format(
                #         name=option_name, opt=option
                #         )
                # anno_open = "<span {data}>".format(data=popover_data)
                # anno_close = "<\span>"

                anno_line = annotation["line"]

                try:
                    anno_start, anno_end = annotation["range"]
                except ValueError:
                    if annotation["range"] == "full_line":
                        anno_start = 0

                    else:
                        print("Annotation range is not valid- "
                              "should be a 2-tuple or 'full_line'")
                        raise

                if value == "\n":
                    chars_on_line = 0
                    lineno += 1
                    yield ttype, value

                    # Close annotations that are still open
                    if opened:
                        yield anno_close, Token.Annotation
                        opened = False

                else:  # Not a newline
                    if not opened:
                        if anno_line == lineno and chars_on_line > anno_start:
                            opened = True
                            yield Token.Annotation, anno_open
                            yield ttype, value
                        else:
                            yield ttype, value

                    else:  # Close the <span> tag
                        if anno_end is not None and chars_on_line > anno_end:
                            yield ttype, value
                            yield Token.Annotation, anno_close
                            # Move to the next annotation
                            annotation = self.annotations.pop(0)
                            opened = False
                        else:
                            yield ttype, value

            else:
                yield ttype, value
