DEFAULT_SPLITTER = "\n\n"


def normalize_splitter(splitter_str: str) -> str:
    """
    Normalizes the splitter string by replacing escaped newline characters with actual newline characters.
    :param splitter_str:
    :return:
    """
    if not splitter_str:
        raise ValueError("Empty splitter string")
    return splitter_str.replace('\\n', '\n')
