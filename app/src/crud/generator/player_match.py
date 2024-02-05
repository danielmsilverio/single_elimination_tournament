class PlayerMath:
    """
    Auxiliary Class to generate Match, contains name and match_id

    :params name: int|None default None
    :params match_id: int|None default None
    """

    def __init__(self, name: str | None = None, match_id: int | None = None):
        self.name: str | None = name
        self.match_id: int | None = match_id

    def skippable_player(self) -> bool:
        """
        Validates whether he is an ignorant player,
        that is, just a dummy for assistance
        """
        return self.name is None and self.match_id is None

    def __repr__(self) -> str:
        return f"PlayrMath(name={self.name}, match_id={self.match_id}, skippable_player={self.skippable_player()}"
