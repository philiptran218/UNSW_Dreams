def generate_handle(name_first, name_last):
    handle = name_first + name_last

    handle = handle.lower()
    handle = handle.replace("@", "")
    handle = handle.replace(" ", "")

    if len(handle) > 20:
        handle = handle[:20]
    else:
        pass
    
    handle_num = 0

    while is_handle_taken(handle):
        if handle_num >= 1:
            handle = handle.replace(handle[len(handle) - 1], "")
        
            handle = handle + str(handle_num)
            handle_num += 1

        return handle


def is_handle_taken(handle):
    for user in data['users']:
        if user['handle'] == handle:
            return True

    return False