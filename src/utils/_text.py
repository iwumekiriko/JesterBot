import re


def prepare_block_text(text: str) -> str:
    if text.find('`') != -1:
        return "```" + text.replace('`', '\'') + "```"
    
    return f"```{text}```"