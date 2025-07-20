import re
from typing import List

def split_text(text: str, max_length: int = 4000) -> List[str]:
    """Разбивает текст на части, не разрывая markdown"""
    parts = []
    while text:
        if len(text) <= max_length:
            parts.append(text)
            break
        
        # Ищем место для разрыва
        split_index = max_length
        for delimiter in ['\n\n', '.\n', '! ', '? ', '.\n', '\n', '. ', ' ']:
            index = text.rfind(delimiter, 0, max_length)
            if index != -1:
                split_index = index + len(delimiter)
                break
        
        parts.append(text[:split_index].strip())
        text = text[split_index:]
    
    return parts