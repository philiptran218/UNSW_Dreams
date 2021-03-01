Author: theme
    assumptions (indented to show where they lie)

John: channels_list_v1
    Channels_list should take users id
    Assume if id is invalid, then an input error occurs.
    If id is valid, needs to scan through the channel to find the persons id
    If id is in channel, it and all its information will be printed.
    Prints off channels dictionary, but created in a way that only contains the new ones.
    Potentially create new directory inside the function and print off that
    If id is not in channel, will not be added to new directory, therefore will not be finished. 


John: channels_listall_v1
    Pretty much same as channels_list. 
    Only difference is there's no need to check for id inside
    Just prints off channels disctionary, no need to create new one.
    