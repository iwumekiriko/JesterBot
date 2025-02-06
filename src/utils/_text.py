def prepare_block_text(text: str) -> str:
    """
    Support func for logger's edited/deleted messages.

    Args:
        text (str): message's text
    
    Returns:
        str: text with replaced symbols
    """

    if text.find('`') != -1:
        return "```" + text.replace('`', '\'') + "```"

    return f"```{text}```"
