Pygments Annotator
==================

Allows Pygments-formatted source code to be annotated with Bootstrap popovers.
The goal is simple easy integration with Jekyll and any web service that uses
Pygments.

Annotations are listed at the end of a file, with hooks in the comments of the
lines where they should appear. They can either be full-line, or have a 
character range. For simplicity, the range is rounded to the nearest Pygments 
token– usually around whitespace. 

A Python dict of [Bootstrap popover options](http://getbootstrap.com/javascript/ 
"Bootstrap popover options") can also be included: they'll be used to format
the `<span>` tags around the popover.

Here's how it works! This is an example explaining classes from
[The Codeless Code](http://thecodelesscode.com/ "The Codeless Code")– I've
annotated it to explain some of the Python notation, like `__init__`.

    class Soldier(object):

        def __init__(self, name):  # @0
            self.name = name
            self.dead = False

        def die_for_emperor(self): # @1
            while not self.dead:
                attack()

    @0{'range': (5, 29), 
    'content': '__init__ gets parameters when a class is initialized. For 
    example, this class will be called as first_soldier = Soldier("Li Si"), 
    where "Li Si" will now be the name of that Soldier.'}

    @1{"range": "full_line",
    "content": "This method doesn't really exist; it's just an example",
    "options": {data-container="body" data-trigger="hover" 
    data-placement="right"}}

+ Annotations are placed in inline comments, using the @ symbol and a unique
ID. They're cross-referenced with a block of annotations at the bottom of the
source.

+ Comments that are **just** annotations are deleted, but otherwise, they're
preserved.

+ `range` can be either a tuple of character ranges or `'full_line'`. The 
character ranges are rounded to the nearest token for simplicity.

+ A JSON object called `options` can be included: it will be the Popover's 
options. Otherwise, the defaults (`data-container="body"` and 
`data-placement="top"`) are used.

Installation
------------
Download or `git clone` this directory into your Python3 `site_packages`, or
symlink it there. You can then import it into a python project with `import 
pyg_annotate`. It does **not** currently work with the `pygmentize` script, 
because it contains a bunch of different compenents, not just a formatter.

Dependencies
------------
Python 3 is required; versions below 3 are not supported.

Requires [Pygments](http://pygments.org/) (`pip3 install pygments`)

Currently [Bootstrap](http://getbootstrap.com/) is also required, though adding
support for other annotation-styles is possible.

Extending Language Support
--------------------------
Just edit `lib/language_data.py` to include the name of a Pygments lexer you'd
like to support and the single-line comment charcter of that language. Then, 
fire off a pull request so we all can use you extention!
