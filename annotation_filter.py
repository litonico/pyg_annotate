from pygments.filter import Filter
from pygments.util import get_list_opt
import annotate


def run_annotate(source_in):
    annotations, source = annotate(source_in)

    options = {"annotations": annotations}
    filter = AnnotationFilter(options)
    print(filter)


class AnnotationFilter(Filter):
    """
    `options` : A list of dicts, with the follwing properties:
    {
    `range`: a string (e.g. "3-12") or "full_line"

    }
    """

    def __init__(self, **options):
        Filter.__init__(self, **options)

        self.escape_html = {
            ord('&'): u'&amp;',
            ord('<'): u'&lt;',
            ord('>'): u'&gt;',
            ord('"'): u'&quot;',
            ord("'"): u'&#39;',
        }

        self.annotations = get_list_opt(options, "annotations")

        # Make sure the annotations are sorted by line, then char- we then only
        # Need to check the first annotation, not all of them.
        self.annotations.sort(
            key=lambda anno: (anno["line"], anno["range"][0])
            )

    # # Popover-annotation handling
    # anno_open, anno_close = '', ''
    # if index > anno_start:  # we've passed the start
    # if index > anno_end:  # we've passed the end
    #    Filter):

    # value = value.translate(self.escape_html)

    def filter(self, lexer, stream):
        anno_open = "OPEN!"  # for testing
        anno_close = "CLOSE!"

        chars_on_line = 0
        linenum = 0
        opened = False
        annotation = self.annotations.pop(0)

        for ttype, value in stream:
            chars_on_line += len(value)

            if self.annotations:
                # popover_options = annotation["options"]
                # popover_data = ''
                # for option_name, option in popover_options:
                #     popover_data += 'data-{name}="{opt}" '.format(
                #         name=option_name, opt=option
                #         )
                # anno_open = "<span {data}>".format(data=popover_data)
                # anno_close = "<\span>"

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
                    linenum += 1
                    yield ttype, value

                    # Full-line annotation handling: close the annotation
                    if anno_end is None:
                        yield anno_close, Token.Annotation

                else:  # Not a newline
                    if not opened:
                        if chars_on_line > anno_start:
                            opened = True
                            yield anno_open, Token.Annotation
                            yield ttype, value
                        else:
                            yield ttype, value

                    else:  # Close the <span> tag
                        if anno_end is not None and chars_on_line > anno_end:
                            yield ttype, value
                            yield anno_close, Token.Annotation
                            # Move to the next annotation
                            annotation = self.annotations.pop(0)
                            opened = False
                        else:
                            yield ttype, value

            else:
                yield ttype, value
