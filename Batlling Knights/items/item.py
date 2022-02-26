class Item:
    def __init__(self, start_position)->None:
        self.position = start_position
        self.equipped = False
        
    @property
    def position(self)->tuple:
        return self._position

    @position.setter
    def position(self, new_position:tuple)->None:
        self._position = new_position
        
    @property
    def equipped(self)->bool:
        return self._equipped

    @equipped.setter
    def equipped(self, updated_quipped_bool:bool)->None:
        self._equipped = updated_quipped_bool

    
    def __str__(self)->str:
        return 'Item'