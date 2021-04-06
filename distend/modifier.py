"""functions to modify the string(s)"""

def pre_list(base, prepend):
    """Inserts list:prepend at beginning of str:base, returns a list."""
    return [f'{pre}{base}' for pre in prepend]

def post_list(base, postpend):
    """Appends list:postpend to end of str:base, returns a list."""
    return [f'{base}{post}' for post in postpend]

def pre_str(base, prepend):
    """Inserts str:prepend at beginning of str:base, returns a str"""
    return f'{prepend}{base}'

def post_str(base, postpend):
    """Appends str:postpend to str:base, returns a str"""
    return f'{base}{postpend}'

def multi_transform(base, rules):
    """Substitutes characters in str:base based on dict:rules
    Multi_transform applies all rules at once instead of one rule at a time
    i.e. password -> p@ssw0rd instead of password -> p@ssword -> p@ssw0rd

    :param base: original string to modify
    :type base: string
    :param rules: rules in key:value format or original:substitution
    :type rules: dictionary

    :rtype: list, max length of 2
    :return: 1st element is str:base and 2nd is all rules applied
    """
    accumulated = base
    transformed = [base]
    for rule, subst in rules.items():
        if rule in base:
            accumulated = accumulated.replace(rule, subst)
    if accumulated != base:
        transformed.append(accumulated)
    return transformed

def single_transform(base, rules):
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
    accumulated = base
    transformed = [base]
    for rule, subst in rules.items():
        if rule in base:
            transformed.append(base.replace(rule, subst))
            accumulated = accumulated.replace(rule, subst)
    if accumulated != transformed[-1]:
        transformed.append(accumulated)
    return transformed

def fuse_lp_lp(transformed, prepend, postpend):
    """With lst:transformed, lst:prepend, lst:postpend returns a lst:fused
    Fuses pre and postpends onto the transformed strings and returns lst:fused
    Function name short hand for 'fuse list prepend list postpend'

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
        a_pre = pre_list(word, prepend)
        fused.extend(a_pre)
        fused.extend(post_list(word, postpend))
        fused.extend([pre_post for pre in a_pre for pre_post in\
                        post_list(pre, postpend)])
    # uniquely transformed strings not including base string
    fused.extend(transformed[1:])
    return fused

def fuse_lp_sp(transformed, prepend, postpend):
    """given lst:transformed, lst:prepend, str:postpend returns a lst:fused
    fuses pre and postpends onto the transformed strings and returns lst:fused
    fnct name short hand for 'fuse list pre string post'

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
        a_pre = pre_list(word, prepend)
        fused.extend(a_pre)
        fused.append(post_str(word, postpend))
        fused.extend([f'{pre}{postpend}' for pre in a_pre])
    # uniquely transformed strings not including base string
    fused.extend(transformed[1:])
    return fused

def fuse_sp_lp(transformed, prepend, postpend):
    """given lst:transformed, str:prepend, lst:postpend returns a lst:fused
    fuses pre and postpends onto the transformed strings and returns lst:fused
    fnct name short hand for 'fuse string pre list post'

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
        fused.append(pre_str(word, prepend))
        a_post = post_list(word, postpend)
        fused.extend(a_post)
        fused.extend([f'{prepend}{post}' for post in a_post])
    # uniquely transformed strings not including base string
    fused.extend(transformed[1:])
    return fused

def fuse_sp_sp(transformed, prepend, postpend):
    """given lst:transformed, str:prepend, lst:postpend returns a lst:fused
    fuses pre and postpend onto the transformed strings and returns lst:fused
    fnct name short hand for 'fuse string pre string post'

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
        fused.append(pre_str(word, prepend))
        fused.append(post_str(word, postpend))
        fused.append(f'{prepend}{word}{postpend}')
    # uniquely transformed strings not including base string
    fused.extend(transformed[1:])
    return fused

def fuse_lp_np(transformed, prepend):
    """given lst:transformed, lst:prepend returns a lst:fused
    fuses prepends onto the transformed strings and returns lst:fused
    fnct name short hand for 'fuse list pre no post'

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepends to insert at beginning of each transformed string
    :type prepend: list, minimum length of 2

    :rtype: list
    :return: prepends applied, and uniquely transformed strings appended
    """
    fused = [pre_str(word, pre) for pre in prepend for word in transformed]
    # uniquely transformed strings not including base string
    fused.extend(transformed[1:])
    return fused

def fuse_sp_np(transformed, prepend):
    """given lst:transformed, str:prepend returns a lst:fused
    fuses prepends onto the transformed strings and returns lst:fused
    fnct name short hand for 'fuse str pre no post'

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param prepend: prepend to insert at beginning of each transformed string
    :type prepend: string

    :rtype: list
    :return: prepend applied, and uniquely transformed strings appended
    """
    fused = [pre_str(word, prepend) for word in transformed]
    # uniquely transformed strings not including base string
    fused.extend(transformed[1:])
    return fused

def fuse_np_lp(transformed, postpend):
    """given lst:transformed, lst:postpend returns a lst:fused
    fuses postpends onto the transformed strings and returns lst:fused
    fnct name short hand for 'fuse no pre list post'

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param postpend: postpends to append on end of each transformed string
    :type postpend: list, minimum length of 2

    :rtype: list
    :return: postpends applied, and uniquely transformed strings appended
    """
    fused = [post_str(word, post) for post in postpend for word in transformed]
    # uniquely transformed strings not including base string
    fused.extend(transformed[1:])
    return fused

def fuse_np_sp(transformed, postpend):
    """given lst:transformed, str:postpend returns a lst:fused
    fuses postpend onto the transformed strings and returns lst:fused
    fnct name short hand for 'fuse no pre str post'

    :param transformed: strings with single/multi transform applied
    :type transformed: list
    :param postpend: postpend to append on end of each transformed string
    :type postpend: string

    :rtype: list
    :return: postpend applied, and uniquely transformed strings appended
    """
    fused = [post_str(word, postpend) for word in transformed]
    # uniquely transformed strings not including base string
    fused.extend(transformed[1:])
    return fused
