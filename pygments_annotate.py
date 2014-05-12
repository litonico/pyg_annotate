class AnnotationFilter(Filter):
    """
    `options` : A list of dicts, with the follwing properties:
    {
    `range`: a string "3-12" or "full_line"

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

    anno_open = "OPEN!"  # for testing
    anno_close = "CLOSE!"
    # popover_options = get_popover_options('magic!')

    # # Popover-annotation handling
    # anno_open, anno_close = '', ''
    # if index > anno_start:  # we've passed the start
    #     anno_open = "<span {opt}>".format(opt=popover_options)
    # if index > anno_end:  # we've passed the end
    #     anno_close = "<\span>"Filter):

    def filter(self, lexer, stream):
        chars_on_line = 0

        for ttype, value in stream:
            value = value.translate(self.escape_html)
            # if:

            #     current_anno += 1
            #     next_anno += 1

            chars_on_line += len(value)

            if value == "\n":
                chars_on_line = 0

