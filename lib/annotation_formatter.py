import os
from pygments.formatters.html import HtmlFormatter, _escape_html_table
from pygments.token import Token


# if ttype is Token.Annotation:
# yield 0, value


class AnnotationHtmlFormatter(HtmlFormatter):

    def __init__(self, **options):
        HtmlFormatter.__init__(self, **options)

    def _format_lines(self, tokensource):
        """
        Just format the tokens, without any wrapping tags.
        Yield individual lines.
        """
        nocls = self.noclasses
        lsep = self.lineseparator
        # for <span style=""> lookup only
        getcls = self.ttype2class.get
        c2s = self.class2style
        escape_table = _escape_html_table
        tagsfile = self.tagsfile

        lspan = ''
        line = ''

        for ttype, value in tokensource:
            if value == "\n":  # DEBUG
                print("NL")
            else:
                print(value)

            if ttype is Token.Annotation:
                cspan = ''
                lspan = ''

            else:
                if nocls:
                    cclass = getcls(ttype)
                    while cclass is None:
                        ttype = ttype.parent
                        cclass = getcls(ttype)
                    cspan = cclass \
                        and '<span style="%s">' % c2s[cclass][0] \
                        or ''
                else:
                    cls = self._get_css_class(ttype)
                    cspan = cls and '<span class="%s">' % cls or ''

            if ttype is Token.Annotation:
                parts = value.split('\n')  # We need those angle brackets!
            else:
                parts = value.translate(escape_table).split('\n')

            if tagsfile and ttype in Token.Name:
                filename, linenumber = self._lookup_ctag(value)
                if linenumber:
                    base, filename = os.path.split(filename)
                    if base:
                        base += '/'
                    filename, extension = os.path.splitext(filename)
                    url = self.tagurlformat % \
                        {'path': base, 'fname': filename, 'fext': extension}
                    parts[0] = "<a href=\"%s#%s-%d\">%s" % \
                        (url, self.lineanchors, linenumber, parts[0])
                    parts[-1] = parts[-1] + "</a>"

            # for all but the last line
            for part in parts[:-1]:
                if line:
                    if lspan != cspan:
                        line += (lspan and '</span>') + cspan + part + \
                                (cspan and '</span>') + lsep
                    else:  # both are the same
                        line += part + (lspan and '</span>') + lsep
                    yield 1, line
                    line = ''

                elif part:
                    yield 1, cspan + part + (cspan and '</span>') + lsep
                else:
                    yield 1, lsep
            # for the last line
            if line and parts[-1]:
                if lspan != cspan:
                    line += (lspan and '</span>') + cspan + parts[-1]
                    lspan = cspan
                else:
                    line += parts[-1]
            elif parts[-1]:
                line = cspan + parts[-1]
                lspan = cspan
            # else we neither have to open a new span nor set lspan

        if line:
            yield 1, line + (lspan and '</span>') + lsep
