from contracts import contract, new_contract

class Width:
    '''
>>> width = Width(name='Wide', short_name='EE')
>>> width
Wide
>>> width.short_name
'EE'
    '''

    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name

    def get_name(self):
        return self._name

    @contract(name=str)
    def set_name(self, name):
        self._name = name

    name = property(get_name, set_name)

    def get_short_name(self):
        return self._short_name

    @contract(short_name=str)
    def set_short_name(self, short_name):
        self._short_name = short_name

    short_name = property(get_short_name, set_short_name)

    def __repr__(self) -> str:
        return self.name


