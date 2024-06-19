class APIObject:
    def __init__(self):
        """
        Initializes the APIObject with an empty params dictionary.
        """
        self.params = {}

    def create_params(self):
        """
        Creates a dictionary of parameters where the values are not None.

        Returns:
            dict: A dictionary with keys and values from self.params where the values are not None.
        """
        return {key: value for key, value in self.params.items() if value is not None}