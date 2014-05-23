sourcestr = """class Soldier(object):

    def __init__(self, name):  # @0
        self.name = name
        self.dead = False

    def die_in_battle(self): # @1
        while not self.dead:
            attack()

@0{'range': (5, 29), 
'content': '__init__ gets parameters when a class is initialized. For example, 
this class will be called as first_soldier = Soldier("Li Si"), where "Li Si" 
will now be the name of that Soldier.'}

@1{'range': 'full_line',
   'content': 'This whole line is highlighted'}
"""
