"""functions to modify the string(s)"""

# add separator
def prepend_list(base: str, prepend: list, separator: str='') -> list:
    """Inserts list:prepend at beginning of str:base
    with default str:separator='', returns a list
    """
    return [f'{pre}{separator}{base}' for pre in prepend]

# add separator
def postpend_list(base: str, postpend: list, separator: str='') -> list:
    """Appends list:postpend to end of str:base
    with default str:separator='', returns a list.
    """
    return [f'{base}{separator}{post}' for post in postpend]

# add parameter separator
def prepend_str(base: str, prepend: str, separator: str='') -> str:
    """Inserts str:prepend at beginning of str:base
    with default str:separator='', returns a str
    """
    return f'{prepend}{separator}{base}'

# add parameter separator
def postpend_str(base: str, postpend: str, separator: str='') -> str:
    """Appends str:postpend to str:base
    with default str:separator, returns a str
    """
    return f'{base}{separator}{postpend}'

def multi_transform(base: str, rules: dict) -> list:
    """Substitutes characters in str:base based on dict:rules
    Multi_transform applies all rules at once instead of one rule at a time
    i.e. password -> p@ssw0rd instead of password -> p@ssword -> p@ssw0rd

    :param base: original string to modify
    :type base: string
    :param rules: rules in key:value format or original:substitution
    :type rules: dictionary

    :rtype: list, max length of 2
    :return: 1st element is str:base and 2nd element is all rules applied
    """
    all_rules_applied = base  # set at beginning to allow replacement later
    transformed = [base]
    for rule, substitute in rules.items():
        if rule in base:
            all_rules_applied = all_rules_applied.replace(rule, substitute)
    if all_rules_applied != base:          # make sure base is not repeated
        transformed.append(all_rules_applied)
    return transformed

def single_transform(base: str, rules: dict) -> list:
    """Substitutes characters in str:base using dict:rules
    Single_transform applies one rule at a time instead of all rules at once
    i.e. password -> p@ssword -> p@ssw0rd instead of password -> p@ssw0rd

    :param base: original string to modify
    :type base: string
    :param rules: rules in key:value format or original:substitution
    :type rules: dictionary

    :rtype: list, minimum length of 1
    :return: 1st element is str:base other elements vary based on applied rule
    """
    all_rules_applied = base            # set for replacement later
    transformed = [base]
    for rule, substitute in rules.items():
        if rule in base:
            transformed.append(base.replace(rule, substitute))  # single rule
            all_rules_applied = all_rules_applied.replace(rule, substitute)
    if all_rules_applied != transformed[-1]:  # prevent duplicate base or single rule
        transformed.append(all_rules_applied)
    return transformed

# add separator
def fuse_list_prepend_list_postpend(transformed: list, prepend: list,
                                    postpend: list, separator: str='') -> list:
    """With list:transformed, list:prepend, list:postpend, str:separator,
    returns a list:fused
    appends pre and postpends to the transformed strings and returns list:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepends to insert at beginning of each transformed string
    :type prepend: list, minimum length of 2
    :param postpend: postpends to append on end of each transformed string
    :type postpend: list, minimum length of 2
    :param separator: separator between base and prepends and postpends
    :type separator: string default of ''

    :rtype: list
    :return: pre/postpends applied, and uniquely transformed strings appended
    """
    fused = []
    for word in transformed:
        prepend_applied = prepend_list(word, prepend, separator)
        fused.extend(prepend_applied)
        fused.extend(postpend_list(word, postpend, separator))
        fused.extend([pre_post for pre in prepend_applied for pre_post in\
            postpend_list(pre, postpend, separator)])  # apply post on prepends
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused

# add separator
def fuse_list_prepend_str_postpend(transformed: list, prepend:list,
                                   postpend: str, separator: str='') -> list:
    """given list:transformed, list:prepend, str:postpend, str:separator,
    returns a list:fused
    fuses pre and postpends onto the transformed strings and returns list:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepends to insert at beginning of each transformed string
    :type prepend: list, minimum length of 2
    :param postpend: postpend to append on end of each transformed string
    :type postpend: string
    :param separator: separator between base and prepends and postpend
    :type separator: string default of ''

    :rtype: list
    :return: pre/postpends applied, and uniquely transformed strings appended
    """
    fused = []
    for word in transformed:
        prepend_applied = prepend_list(word, prepend, separator)
        fused.extend(prepend_applied)
        fused.append(postpend_str(word, postpend, separator))
        fused.extend([postpend_str(pre, postpend, separator) for pre in\
                      prepend_applied])  # apply postpend onto prepend_applied
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused

# add separator
def fuse_str_prepend_list_postpend(transformed: list, prepend: str,
                                   postpend: list, separator: str='') -> list:
    """given list:transformed, str:prepend, list:postpend, str:separator,
    returns a list:fused
    fuses pre and postpends onto the transformed strings and returns list:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepend to insert at beginning of each transformed string
    :type prepend: string
    :param postpend: postpends to append on end of each transformed string
    :type postpend: list, minimum length of 2
    :param separator: separator between base and prepend and postpends
    :type separator: string default of ''

    :rtype: list
    :return: pre/postpends applied, and uniquely transformed strings appended
    """
    fused = []
    for word in transformed:
        fused.append(prepend_str(word, prepend, separator))
        postpend_applied = postpend_list(word, postpend, separator)
        fused.extend(postpend_applied)
        fused.extend([prepend_str(post, prepend, separator) for post in\
                      postpend_applied])  # apply prepend on postpend_applied
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused

# add separator
def fuse_str_prepend_str_postpend(transformed: list, prepend: str,
                                  postpend: str, separator: str='') -> list:
    """given list:transformed, str:prepend, str:postpend, str:separator,
    returns a list:fused
    fuses pre and postpend onto the transformed strings and returns list:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepend to insert at beginning of each transformed string
    :type prepend: string
    :param postpend: postpend to append on end of each transformed string
    :type postpend: string
    :param separator: separator between base and prepend and postpend
    :type separator: string default of ''

    :rtype: list
    :return: pre/postpend applied, and uniquely transformed strings appended
    """
    fused = []
    for word in transformed:
        fused.append(prepend_str(word, prepend, separator))
        fused.append(postpend_str(word, postpend, separator))
        # apply both at the same time
        fused.append(f'{prepend}{separator}{word}{separator}{postpend}')
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused

# add separator
def fuse_list_prepend_no_postpend(transformed: list, prepend: list,
                                  separator: str='') -> list:
    """given list:transformed, list:prepend, str:separator returns a list:fused
    fuses prepends onto the transformed strings and returns list:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepends to insert at beginning of each transformed string
    :type prepend: list, minimum length of 2
    :param separator: separator between base and prepends
    :type separator: string default of ''

    :rtype: list
    :return: prepends applied, and uniquely transformed strings appended
    """
    fused = [prepend_str(word, pre, separator) for pre in prepend\
             for word in transformed]  # prepends for each transformed str
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused

# add separator
def fuse_str_prepend_no_postpend(transformed: list, prepend: str,
                                 separator: str='') -> list:
    """given list:transformed, str:prepend, str:separator returns a list:fused
    fuses prepends onto the transformed strings and returns list:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepend to insert at beginning of each transformed string
    :type prepend: string
    :param separator: separator between base and prepend
    :type separator: string default of ''

    :rtype: list
    :return: prepend applied, and uniquely transformed strings appended
    """
    fused = [prepend_str(word, prepend, separator) for word in transformed]
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused

# add separator
def fuse_no_prepend_list_postpend(transformed: list, postpend: list,
                                  separator: str='') -> list:
    """given list:transformed, list:postpend, str:separator,
    returns a list:fused
    fuses postpends onto the transformed strings and returns list:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param postpend: postpends to append on end of each transformed string
    :type postpend: list, minimum length of 2
    :param separator: separator between base and postpends
    :type separator: string default of ''

    :rtype: list
    :return: postpends applied, and uniquely transformed strings appended
    """
    fused = [postpend_str(word, post, separator) for post in postpend for word in\
             transformed]  # apply postpends for each word
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused

# changed name
def fuse_no_prepend_str_postpend(transformed: list, postpend: str,
                                 separator: str='') -> list:
    """given list:transformed, str:postpend, str:separator returns a list:fused
    fuses postpend onto the transformed strings and returns list:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param postpend: postpend to append on end of each transformed string
    :type postpend: string
    :param separator: separator between base and postpend
    :type separator: string default of ''

    :rtype: list
    :return: postpend applied, and uniquely transformed strings appended
    """
    fused = [postpend_str(word, postpend, separator) for word in transformed]
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused
