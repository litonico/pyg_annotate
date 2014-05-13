Pygments Annotator
==================

Allows Pygments-formatted source code to be annotated with Bootstrap popovers.
The goal is simple easy integration with Jekyll and any web service that uses
Pygments

Annotations are listed at the end of a file, with hooks in the comments of the
lines where they should appear. They can either be full-line, or have a 
character range. For simplicity, the range is rounded to the nearest Pygments 
token– usually around whitespace. 

A Python dict of [Bootstrap popover options](http://getbootstrap.com/javascript/ 
"Bootstrap popover options") can also be included: they'll be used to format
the `<span>` tags around the popover.

Here's how it works!

    class Soldier(object):

        def __init__(self, name):  # @0
            self.name = name
            self.dead = False

        def die_for_emperor(self): # @1
            while not self.dead:
                attack()

    @0{'range': '5-29', 
    'content': '__init__ gets parameters when a class is initialized. For example, 
    this class will be called as first_soldier = Soldier("Li Si"), where "Li Si" will 
    now be the name of that Soldier.'}

    @1{"range": "full_line",
    "content": "This whole line is highlighted",
    "options": {}
