from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_mode

md_block_type_paragraph = "paragraph"
md_block_type_heading = "heading"
md_block_type_code = "code"
md_block_type_quote = "quote"
md_block_type_unordered_list = "unordered_list"
md_block_type_ordered_list = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    if (
            block.startswith("# ")
            or block.startswith("## ")
            or block.startswith("### ")
            or block.startswith("#### ")
            or block.startswith("##### ")
            or block.startswith("###### ")
    ):
        return md_block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return md_block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return md_block_type_paragraph
        return md_block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return md_block_type_paragraph
        return md_block_type_unordered_list
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return md_block_type_paragraph
        return md_block_type_unordered_list
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return md_block_type_paragraph
            i += 1
        return md_block_type_ordered_list
    return md_block_type_paragraph


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(strip_blocks, filter(filter_empty_blocks, blocks)))
    return blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    block_type = block_to_block_type(block)
    if block_type == md_block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == md_block_type_heading:
        return heading_to_html_node(block)
    if block_type == md_block_type_code:
        return code_to_html_node(block)
    if block_type == md_block_type_ordered_list:
        return olist_to_html_node(block)
    if block_type == md_block_type_unordered_list:
        return ulist_to_html_node(block)
    if block_type == md_block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    block = block.strip("`").strip()
    lines = block.split("\n")
    children = []
    for line in lines:
        textnode = text_to_children(line)
        children.append(ParentNode("code", textnode))
    return ParentNode("pre", children)


def olist_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        line = line[2:].strip()
        textnode = text_to_children(line)
        children.append(ParentNode("li", textnode))
    return ParentNode("ol", children)


def ulist_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        line = line.lstrip("- ").strip()
        textnode = text_to_children(line)
        children.append(ParentNode("li", textnode))
    return ParentNode("ul", children)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_mode(text_node)
        children.append(html_node)
    return children


def filter_empty_blocks(block):
    if block == "":
        return False
    return True


def strip_blocks(block):
    return block.strip()


def extract_title(markdown):
    index = markdown.find("# ")
    half = markdown[index+2:]
    nl_index = half.find("\n")
    result = half[:nl_index]
    return result
