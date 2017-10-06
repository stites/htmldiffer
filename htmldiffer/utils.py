from .settings import *


def html2list(html_string):
    """
    :param html_string: any ol' html string you've got
    :return: list of elements, making sure not to break up open tags (even if they contain attributes)
    Note that any blacklisted tag will not be broken up
    Example:
        html_str = "<h1>This is a simple header</h1>"
        result = html2list(html_str)
        result == ['<h1>', 'This ', 'is ', 'a ', 'simple ', 'header', '</h1>']

    Blacklisted tag example:
        BLACKLISTED_TAGS = ['head']
        html_str = "<head><title>Page Title</title></head>"
        result = html2list(html_str)
        result == ['<head><title>Page Title</title></head>']
    """
    # different modes for parsing
    CHAR, TAG = 'char', 'tag'

    mode = CHAR
    cur = ''
    out = []

    # TODO: use generators
    # iterate through the string, character by character
    for c in html_string:

        # tags must be checked first to close tags
        if mode == TAG:

            # add character to current element
            cur += c

            # if we see the end of the tag
            if c == '>':
                out.append(cur)  # add the current element to the output
                cur = ''         # reset the character
                mode = CHAR      # set the mode back to character mode

        elif mode == CHAR:

            # when we are in CHAR mode and see an opening tag, we must switch
            if c == '<':

                # clear out string collected so far
                if cur != "":
                    out.append(cur)   # if we have already started a new element, store it
                cur = c               # being our tag
                mode = TAG            # swap to tag mode

            # when we reach the next 'word', store and continue
            # FIXME: use isspace() instead of c == ' ', here
            elif c == ' ':
                out.append(cur+c)   # NOTE: we add spaces here so that we preserve structure
                cur = ''

            # otherwise, simply continue building up the current element
            else:
                cur += c

    # TODO: move this to its own function `merge_blacklisted` or `merge_tags` return to a generator instead of list
    cleaned = list()
    blacklisted_tag = None
    blacklisted_string = ""

    for x in out:
        if not blacklisted_tag:
            for tag in BLACKLISTED_TAGS:
                if verified_blacklisted_tag(x, tag):
                    blacklisted_tag = tag
                    blacklisted_string += x
                    break
            if not blacklisted_tag:
                cleaned.append(x)
        else:
            if x == "</{0}>".format(blacklisted_tag):
                blacklisted_string += x
                cleaned.append(blacklisted_string)
                blacklisted_tag = None
                blacklisted_string = ""
            else:
                blacklisted_string += x

    return cleaned


def verified_blacklisted_tag(x, tag):
    """
    check for '<' + blacklisted_tag +  ' ' or '>'
    as in: <head> or <head ...> (should not match <header if checking for <head)
    """
    initial = x[0:len(tag) + 1 + 1]
    blacklisted_head = "<{0}".format(tag)
    return initial == (blacklisted_head + " ") or initial == (blacklisted_head + ">")


def add_style_str(html_list, custom_style_str=None):
    style_str = custom_style_str if custom_style_str else STYLE_STR

    for idx,el in enumerate(html_list):
        if "</head>" in el:
            head = el.split("</head>")
            new_head = head[0] + style_str + "</head>" + "".join(head[1:])
            html_list[idx] = new_head

    return html_list


# ===============================
# Predicate functions
# ===============================
# Note: These make assumptions about consuming valid html text. Validations should happen before these internal
# predicate functions are used -- these are not currently used for parsing.

def is_comment(text):
    return "<!--" in text


def is_closing_tag(text):
    return '</' in text


def is_ignorable(text):
    return is_comment(text) or is_closing_tag(text) or text.isspace()


def is_whitelisted_tag(x):
    def in_x(tag):
        return "<%s" % tag in x

    return any(in_x, WHITELISTED_TAGS)


def is_open_script_tag(x):
    return "<script " in x


def is_closed_script_tag(x):
    return "<\script " in x


def is_tag(x):
    return len(x) > 0 and x[0] == "<" and x[-1] == ">"


def is_div(x):
    return x[0:4] == "<div" and x[-6:] == "</div>"
