from pyg_annotate.lib import annotation_filter, annotation_formatter
from pygments import lex
from pygments.util import StringIO, BytesIO


def format(tokens, formatter, outfile=None):
    """
    Format a tokenlist ``tokens`` with the formatter ``formatter``.

    If ``outfile`` is given and a valid file object (an object
    with a ``write`` method), the result will be written to it, otherwise
    it is returned as a string.
    """
    try:
        if not outfile:
            # print formatter, 'using', formatter.encoding
            realoutfile = formatter.encoding and BytesIO() or StringIO()
            formatter.format(tokens, realoutfile)
            return realoutfile.getvalue()
        else:
            formatter.format(tokens, outfile)
    except TypeError as err:
        if isinstance(err.args[0], str) and \
           'unbound method format' in err.args[0]:
            raise TypeError('format() argument must be a formatter instance, '
                            'not a class')
        raise


def highlight(code, lexer, formatter=None, outfile=None):
    """
    Lex ``code`` with ``lexer`` and format it with the formatter ``formatter``.

    If ``outfile`` is given and a valid file object (an object
    with a ``write`` method), the result will be written to it, otherwise
    it is returned as a string.
    """
    real_formatter = annotation_formatter
    lexer = lexer.add_filter(annotation_filter)

    return format(lex(code, lexer), real_formatter, outfile)
