"""functions to modify the string(s)"""

# add separator
def prepend_list(base_word: str, prepend: list, separator: str='') -> list:
    """Inserts list:prepend at beginning of str:base_word
    with default str:separator='', returns a list
    """
    return [f'{pre}{separator}{base_word}' for pre in prepend]

# add separator
def postpend_list(base_word: str, postpend: list, separator: str='') -> list:
    """Appends list:postpend to end of str:base_word
    with default str:separator='', returns a list.
    """
    return [f'{base_word}{separator}{post}' for post in postpend]

# add parameter separator
def prepend_str(base_word: str, prepend: str, separator: str='') -> str:
    """Inserts str:prepend at beginning of str:base_word
    with default str:separator='', returns a str
    """
    return f'{prepend}{separator}{base_word}'

# add parameter separator
def postpend_str(base_word: str, postpend: str, separator: str='') -> str:
    """Appends str:postpend to str:base_word
    with default str:separator, returns a str
    """
    return f'{base_word}{separator}{postpend}'

def replace_multiple(base_word: str, all_replacements: dict) -> list:
    """replaces characters in str:base_word with dict:all_replacements
    replace_multiple replaces all at once instead of one at a time
    i.e. password -> p@ssw0rd instead of password -> p@ssword -> p@ssw0rd

    :param base_word: original string to modify
    :type base_word: string
    :param all_replacements: format of original:replacement
    :type all_replacements: dictionary

    :rtype: list, max length of 2
    :return: 1st element is str:base_word and 2nd element is all replaced
    """
    fully_replaced = base_word  # set to base_word and replace all later
    replaced = [base_word]
    for original, replacement in all_replacements.items():
        if original in base_word:
            fully_replaced = fully_replaced.replace(original, replacement)
    if fully_replaced != base_word:  # make sure base_word is not repeated
        replaced.append(fully_replaced)
    return replaced

def replace_single(base_word: str, all_replacements: dict) -> list:
    """replaces characters in str:base_word using dict:all_replacements
    replace_single replaces one at a time instead of all at once
    i.e. password -> p@ssword -> passw0rd -> p@ssw0rd
    instead of password -> p@ssw0rd

    :param base_word: original string to modify
    :type base_word: string
    :param all_replaced: format of original:replacement
    :type all_replaced: dictionar

    :rtype: list, minimum length of 1
    :return: 1st element is str:base_word other elements vary by replacement
    """
    fully_replaced = base_word  # set for replacement later
    replaced = [base_word]
    for original, replacement in all_replacements.items():
        if original in base_word:
            replaced.append(base_word.replace(original, replacement))
            fully_replaced = fully_replaced.replace(original, replacement)
    # no duplicates of base_word or a single replaced word
    if fully_replaced != replaced[-1]:
        replaced.append(fully_replaced)
    return replaced

# add separator
def fuse_list_prepend_list_postpend(replaced: list, prepend: list,
                                    postpend: list, separator: str='') -> list:
    """With list:replaced, list:prepend, list:postpend, str:separator,
    returns a list:fused
    appends pre and postpends to the replaced strings and returns list:fused

    :param replaced: strings with single/multi transform applied
    :type replaced: list
    :param prepend: prepends to insert at beginning of each replaced string
    :type prepend: list, minimum length of 2
    :param postpend: postpends to append on end of each replaced string
    :type postpend: list, minimum length of 2
    :param separator: separator between base_word and prepends and postpends
    :type separator: string default of ''

    :rtype: list
    :return: pre/postpends applied, and uniquely replaced strings appended
    """
    fused = []
    for word in replaced:
        prepend_applied = prepend_list(word, prepend, separator)
        fused.extend(prepend_applied)
        fused.extend(postpend_list(word, postpend, separator))
        fused.extend([pre_post for pre in prepend_applied for pre_post in\
            postpend_list(pre, postpend, separator)])  # apply post on prepends
    fused.extend(replaced[1:])  # uniquely replaced strings
    return fused

# add separator
def fuse_list_prepend_str_postpend(replaced: list, prepend:list,
                                   postpend: str, separator: str='') -> list:
    """given list:replaced, list:prepend, str:postpend, str:separator,
    returns a list:fused
    fuses pre and postpends onto the replaced strings and returns list:fused

    :param replaced: strings with single/multi transform applied
    :type replaced: list
    :param prepend: prepends to insert at beginning of each replaced string
    :type prepend: list, minimum length of 2
    :param postpend: postpend to append on end of each replaced string
    :type postpend: string
    :param separator: separator between base_word and prepends and postpend
    :type separator: string default of ''

    :rtype: list
    :return: pre/postpends applied, and uniquely replaced strings appended
    """
    fused = []
    for word in replaced:
        prepend_applied = prepend_list(word, prepend, separator)
        fused.extend(prepend_applied)
        fused.append(postpend_str(word, postpend, separator))
        fused.extend([postpend_str(pre, postpend, separator) for pre in\
                      prepend_applied])  # apply postpend onto prepend_applied
    fused.extend(replaced[1:])  # uniquely replaced strings
    return fused

# add separator
def fuse_str_prepend_list_postpend(replaced: list, prepend: str,
                                   postpend: list, separator: str='') -> list:
    """given list:replaced, str:prepend, list:postpend, str:separator,
    returns a list:fused
    fuses pre and postpends onto the replaced strings and returns list:fused

    :param replaced: strings with single/multi transform applied
    :type replaced: list
    :param prepend: prepend to insert at beginning of each replaced string
    :type prepend: string
    :param postpend: postpends to append on end of each replaced string
    :type postpend: list, minimum length of 2
    :param separator: separator between base_word and prepend and postpends
    :type separator: string default of ''

    :rtype: list
    :return: pre/postpends applied, and uniquely replaced strings appended
    """
    fused = []
    for word in replaced:
        fused.append(prepend_str(word, prepend, separator))
        postpend_applied = postpend_list(word, postpend, separator)
        fused.extend(postpend_applied)
        fused.extend([prepend_str(post, prepend, separator) for post in\
                      postpend_applied])  # apply prepend on postpend_applied
    fused.extend(replaced[1:])  # uniquely replaced strings
    return fused

# add separator
def fuse_str_prepend_str_postpend(replaced: list, prepend: str,
                                  postpend: str, separator: str='') -> list:
    """given list:replaced, str:prepend, str:postpend, str:separator,
    returns a list:fused
    fuses pre and postpend onto the replaced strings and returns list:fused

    :param replaced: strings with single/multi transform applied
    :type replaced: list
    :param prepend: prepend to insert at beginning of each replaced string
    :type prepend: string
    :param postpend: postpend to append on end of each replaced string
    :type postpend: string
    :param separator: separator between base_word and prepend and postpend
    :type separator: string default of ''

    :rtype: list
    :return: pre/postpend applied, and uniquely replaced strings appended
    """
    fused = []
    for word in replaced:
        fused.append(prepend_str(word, prepend, separator))
        fused.append(postpend_str(word, postpend, separator))
        # apply both at the same time
        fused.append(f'{prepend}{separator}{word}{separator}{postpend}')
    fused.extend(replaced[1:])  # uniquely replaced strings
    return fused

# add separator
def fuse_list_prepend_no_postpend(replaced: list, prepend: list,
                                  separator: str='') -> list:
    """given list:replaced, list:prepend, str:separator returns a list:fused
    fuses prepends onto the replaced strings and returns list:fused

    :param replaced: strings with single/multi transform applied
    :type replaced: list
    :param prepend: prepends to insert at beginning of each replaced string
    :type prepend: list, minimum length of 2
    :param separator: separator between base_word and prepends
    :type separator: string default of ''

    :rtype: list
    :return: prepends applied, and uniquely replaced strings appended
    """
    fused = [prepend_str(word, pre, separator) for pre in prepend\
             for word in replaced]  # prepends for each replaced str
    fused.extend(replaced[1:])  # uniquely replaced strings
    return fused

# add separator
def fuse_str_prepend_no_postpend(replaced: list, prepend: str,
                                 separator: str='') -> list:
    """given list:replaced, str:prepend, str:separator returns a list:fused
    fuses prepends onto the replaced strings and returns list:fused

    :param replaced: strings with single/multi transform applied
    :type replaced: list
    :param prepend: prepend to insert at beginning of each replaced string
    :type prepend: string
    :param separator: separator between base_word and prepend
    :type separator: string default of ''

    :rtype: list
    :return: prepend applied, and uniquely replaced strings appended
    """
    fused = [prepend_str(word, prepend, separator) for word in replaced]
    fused.extend(replaced[1:])  # uniquely replaced strings
    return fused

# add separator
def fuse_no_prepend_list_postpend(replaced: list, postpend: list,
                                  separator: str='') -> list:
    """given list:replaced, list:postpend, str:separator,
    returns a list:fused
    fuses postpends onto the replaced strings and returns list:fused

    :param replaced: strings with single/multi transform applied
    :type replaced: list
    :param postpend: postpends to append on end of each replaced string
    :type postpend: list, minimum length of 2
    :param separator: separator between base_word and postpends
    :type separator: string default of ''

    :rtype: list
    :return: postpends applied, and uniquely replaced strings appended
    """
    fused = [postpend_str(word, post, separator) for post in postpend for word in\
             replaced]  # apply postpends for each word
    fused.extend(replaced[1:])  # uniquely replaced strings
    return fused

# changed name
def fuse_no_prepend_str_postpend(replaced: list, postpend: str,
                                 separator: str='') -> list:
    """given list:replaced, str:postpend, str:separator returns a list:fused
    fuses postpend onto the replaced strings and returns list:fused

    :param replaced: strings with single/multi transform applied
    :type replaced: list
    :param postpend: postpend to append on end of each replaced string
    :type postpend: string
    :param separator: separator between base_word and postpend
    :type separator: string default of ''

    :rtype: list
    :return: postpend applied, and uniquely replaced strings appended
    """
    fused = [postpend_str(word, postpend, separator) for word in replaced]
    fused.extend(replaced[1:])  # uniquely replaced strings
    return fused
