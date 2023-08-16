class Stickers:
    """
    Class that contains all the stickers that the user can use
    """
    def __init__(self, stickers=None):
        """
        Stickers constructor
        :param stickers: List of stickers to add to the stickers list
        """
        if stickers is None:
            self.stickers_list = []
        else:
            self.stickers_list = stickers
        self.selected_sticker = None

    def get_stickers_values(self):
        """
        Get all the stickers names
        :return: A list of all the stickers names
        """
        return [str(sticker.name) for sticker in self.stickers_list]

    def add_sticker(self, sticker):
        """
        Add a sticker to the stickers list
        :param sticker: Sticker to add
        :return: None
        """
        self.stickers_list.append(sticker)

    def remove_sticker(self, sticker):
        """
        Remove a sticker from the stickers list
        :param sticker: Sticker to remove
        :return: None
        """
        self.stickers_list.remove(sticker)
