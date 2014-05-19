from pyg_annotate.lib.annotation_filter import AnnotationFilter
from pyg_annotate.lib.annotation_formatter import AnnotationHtmlFormatter
from pygments.util import StringIO, BytesIO
from pygments import lexers


def lex(code, lexer):
    """
    Lex ``code`` with ``lexer`` and return an iterable of tokens.
    """
    try:
        return lexer.get_tokens(code)
    except TypeError as err:
        if isinstance(err.args[0], str) and \
           'unbound method get_tokens' in err.args[0]:
            raise TypeError('lex() argument must be a lexer instance, '
                            'not a class')
        raise


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
    Ignore the formatter passed; just use the annotation Html formatter.
    """

    if isinstance(lexer, str):  # in case a string is passed
        lexer = lexers.get_lexer_by_name(lexer)

    lexer = lexer.add_filter(AnnotationFilter)
    return format(lex(code, lexer), AnnotationHtmlFormatter, outfile)
