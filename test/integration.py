def integration_test():
    r"""
    Importing?
    >>> import pyg_annotate

    Pygments as usual?
    >>> import pygments
    >>> from pygments.lexers import get_lexer_by_name
    >>> from pygments.formatters import HtmlFormatter
    >>> pygments.highlight("lambda x: x*2", get_lexer_by_name("python"), HtmlFormatter())
    '<div class="highlight"><pre><span class="k">lambda</span> <span class="n">x</span><span class="p">:</span> <span class="n">x</span><span class="o">*</span><span class="mi">2</span>\n</pre></div>\n'

    pyg_annotate without annotations? Should be the same.
    >>> pyg_annotate.highlight("lambda x: x*2", "python")
    '<div class="highlight"><pre><span class="k">lambda</span> <span class="n">x</span><span class="p">:</span> <span class="n">x</span><span class="o">*</span><span class="mi">2</span>\n</pre></div>\n'

    Complete functionality?
    >>> from pyg_annotate.test import testcase
    >>> pyg_annotate.highlight
    """

if __name__ == "__main__":
    import pyg_annotate
    pyg_annotate.highlight("lambda x: x*2", "python")

    import doctest
    doctest.testmod()
