
def read_text(str):
    """
    Reads a text file and returns its content as a string.
    
    :param str: Path to the text file.
    :return: Content of the text file as a string.
    """
    with open(str, 'r') as file:
        return file.read()