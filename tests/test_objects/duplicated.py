"""Definition of the classes used for duplicates verification."""


class Duplicated:
    """This class will have own schema..."""
    name: str


class DuplicateUser:
    """... but this class will reference Duplicated and also will have own schema."""
    name: str
    duplicate: Duplicated
