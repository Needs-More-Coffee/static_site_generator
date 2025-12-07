from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    for i in range(1, 7):
        if block.startswith("#" * i + " "):
            return BlockType.HEADING
        
    if all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    
    lines = block.split("\n")
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            break
    else:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH