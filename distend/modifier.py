"""functions to modify the string(s)"""

# changed name
def prepend_list(base: str, prepend: list) -> list:
    """Inserts list:prepend at beginning of str:base, returns a list."""
    return [f'{pre}{base}' for pre in prepend]

# changed name
def postpend_list(base: str, postpend: list) -> list:
    """Appends list:postpend to end of str:base, returns a list."""
    return [f'{base}{post}' for post in postpend]

# changed name
def prepend_str(base: str, prepend: str) -> str:
    """Inserts str:prepend at beginning of str:base, returns a str"""
    return f'{prepend}{base}'

# changed name
def postpend_str(base: str, postpend: str) -> str:
    """Appends str:postpend to str:base, returns a str"""
    return f'{base}{postpend}'

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

# changed name
def fuse_list_prepend_list_postpend(transformed: list, prepend: list,
                                    postpend: list) -> list:
    """With lst:transformed, lst:prepend, lst:postpend returns a lst:fused
    appends pre and postpends to the transformed strings and returns lst:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepends to insert at beginning of each transformed string
    :type prepend: list, minimum length of 2
    :param postpend: postpends to append on end of each transformed string
    :type postpend: list, minimum length of 2

    :rtype: list
    :return: pre/postpends applied, and uniquely transformed strings appended
    """
    fused = []
    for word in transformed:
        prepend_applied = prepend_list(word, prepend)
        fused.extend(prepend_applied)
        fused.extend(postpend_list(word, postpend))
        fused.extend([pre_post for pre in prepend_applied for pre_post in\
            postpend_list(pre, postpend)])  # apply postpends on prepends
    fused.extend(transformed[1:])   # append uniquely transformed strings
    return fused

# changed name
def fuse_list_prepend_str_postpend(transformed: list, prepend:list,
                                   postpend: str) -> list:
    """given lst:transformed, lst:prepend, str:postpend returns a lst:fused
    fuses pre and postpends onto the transformed strings and returns lst:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepends to insert at beginning of each transformed string
    :type prepend: list, minimum length of 2
    :param postpend: postpend to append on end of each transformed string
    :type postpend: string

    :rtype: list
    :return: pre/postpends applied, and uniquely transformed strings appended
    """
    fused = []
    for word in transformed:
        prepend_applied = prepend_list(word, prepend)
        fused.extend(prepend_applied)
        fused.append(postpend_str(word, postpend))
        # apply postpend onto list:prepend_applied
        fused.extend([f'{pre}{postpend}' for pre in prepend_applied])
    fused.extend(transformed[1:])  # append uniquely transformed strings
    return fused

# changed name
def fuse_str_prepend_list_postpend(transformed: list, prepend: str,
                                   postpend: list) -> list:
    """given lst:transformed, str:prepend, lst:postpend returns a lst:fused
    fuses pre and postpends onto the transformed strings and returns lst:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepend to insert at beginning of each transformed string
    :type prepend: string
    :param postpend: postpends to append on end of each transformed string
    :type postpend: list, minimum length of 2

    :rtype: list
    :return: pre/postpends applied, and uniquely transformed strings appended
    """
    fused = []
    for word in transformed:
        fused.append(prepend_str(word, prepend))
        postpend_applied = postpend_list(word, postpend)
        fused.extend(postpend_applied)
        # apply prepend on list:postpend_applied
        fused.extend([f'{prepend}{post}' for post in postpend_applied])
    fused.extend(transformed[1:])  # append uniquely transformed strings
    return fused

# changed name
def fuse_str_prepend_str_postpend(transformed: list, prepend: str,
                                  postpend: str) -> list:
    """given lst:transformed, str:prepend, str:postpend returns a lst:fused
    fuses pre and postpend onto the transformed strings and returns lst:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepend to insert at beginning of each transformed string
    :type prepend: string
    :param postpend: postpend to append on end of each transformed string
    :type postpend: string

    :rtype: list
    :return: pre/postpend applied, and uniquely transformed strings appended
    """
    fused = []
    for word in transformed:
        fused.append(prepend_str(word, prepend))
        fused.append(postpend_str(word, postpend))
        fused.append(f'{prepend}{word}{postpend}')  # apply both at same time
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused

# changed name
def fuse_list_prepend_no_postpend(transformed: list, prepend: list) -> list:
    """given lst:transformed, lst:prepend returns a lst:fused
    fuses prepends onto the transformed strings and returns lst:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepends to insert at beginning of each transformed string
    :type prepend: list, minimum length of 2

    :rtype: list
    :return: prepends applied, and uniquely transformed strings appended
    """
    # apply prepends for each word in transformed
    fused = [prepend_str(word, pre) for pre in prepend for word in transformed]
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused

# changed name
def fuse_str_prepend_no_postpend(transformed: list, prepend: str) -> list:
    """given lst:transformed, str:prepend returns a lst:fused
    fuses prepends onto the transformed strings and returns lst:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepend to insert at beginning of each transformed string
    :type prepend: string

    :rtype: list
    :return: prepend applied, and uniquely transformed strings appended
    """
    fused = [prepend_str(word, prepend) for word in transformed]
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused

# changed name
def fuse_no_prepend_list_postpend(transformed: list, postpend: list) -> list:
    """given lst:transformed, lst:postpend returns a lst:fused
    fuses postpends onto the transformed strings and returns lst:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param postpend: postpends to append on end of each transformed string
    :type postpend: list, minimum length of 2

    :rtype: list
    :return: postpends applied, and uniquely transformed strings appended
    """
    fused = [postpend_str(word, post) for post in postpend for word in\
             transformed]  # apply postpends for each word
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused

# changed name
def fuse_no_prepend_str_postpend(transformed: list, postpend: str) -> list:
    """given lst:transformed, str:postpend returns a lst:fused
    fuses postpend onto the transformed strings and returns lst:fused

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param postpend: postpend to append on end of each transformed string
    :type postpend: string

    :rtype: list
    :return: postpend applied, and uniquely transformed strings appended
    """
    fused = [postpend_str(word, postpend) for word in transformed]
    fused.extend(transformed[1:])  # uniquely transformed strings
    return fused
