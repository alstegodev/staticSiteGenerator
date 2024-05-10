import re

from textnode import text_type_text, TextNode, text_type_image, text_type_link, text_type_bold, text_type_italic, \
    text_type_code


def text_to_textnodes(text):
    result = []
    first_textnode = TextNode(text, text_type_text)
    result = split_nodes_delimiter([first_textnode], '**', text_type_bold)
    result = split_nodes_delimiter(result, '*', text_type_italic)
    result = split_nodes_delimiter(result, '`', text_type_code)
    result = split_nodes_image(result)
    result = split_nodes_link(result)

    return result


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            result.append(node)
            continue

        text_list = node.text.split(delimiter)
        if len(text_list) % 2 == 0:
            raise Exception("Incorrect amount of delimiters")

        for index in range(0, len(text_list)):
            if text_list[index] == "":
                continue
            if index % 2 == 0:
                result.append(TextNode(text_list[index], text_type_text))
            else:
                result.append(TextNode(text_list[index], text_type))

    return result


def split_nodes_image(old_nodes):
    result = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            result.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            result.append(node)
            continue

        work_text = node.text
        for index in range(0, len(matches)):
            matches_tuple = matches[index]
            if len(matches_tuple) != 2:
                raise Exception("Incorrect Markdown Language")
            text_list = work_text.split(f"![{matches_tuple[0]}]({matches_tuple[1]})", 1)
            if text_list[0] != "":
                result.append(TextNode(text_list[0], text_type_text))
            result.append(TextNode(matches_tuple[0], text_type_image, matches_tuple[1]))
            work_text = text_list[1]

        if work_text != "":
            result.append(TextNode(work_text, text_type_text))

    return result


def split_nodes_link(old_nodes):
    result = []

    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            result.append(node)
            continue

        work_text = node.text
        for index in range(0, len(matches)):
            matches_tuple = matches[index]
            text_list = work_text.split(f"[{matches_tuple[0]}]({matches_tuple[1]})", 1)
            if text_list[0] != "":
                result.append(TextNode(text_list[0], text_type_text))
            result.append(TextNode(matches_tuple[0], text_type_link, matches_tuple[1]))
            work_text = text_list[1]

        if work_text != "":
            result.append(TextNode(work_text, text_type_text))

    return result


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)]\((.*?)\)", text)
    return matches
