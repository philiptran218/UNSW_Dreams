From our group's interpretation of the project spec, we are making several 
assumptions about the users, the limit of information inputted into the program,
assumptions about the requirements of Dreams itself and the functions we are 
testing in this iteration.

We are assuming:
From our group's interpretation of the project spec, we are making several
assumptions about the users, the limit of information inputted into the program,
assumptions about the requirements of Dreams itself and the functions we are
testing in this iteration.
We are assuming:

  auth.py
    - Auth_register will remove newline or tabs from generated handles.

  user.py and users.py
    - User and users stats are not recorded in real time (i.e. as changes are made with functions such as channel_join). They are instead only recorded
      when the functions are called.
    - For stats, removed users are not counted.
    - The start and end coordinates for the user/profile/uploadphoto must all be greater then 0.
    - The end coordinates of a crop must be greater then the start coordinates if not, InputError will be raised.
    - Users_all_v1() will also include user's that have been removed.

  channel.py
    - If a user is already in the channel, channel_invite and channel_join will not add the user again into the channel.
    - For channel_messages_v1, if the start value is equal to the number of messages in the channel, the function will return an empty 'messages' list.
    - Empty channels (When the last member leaves) will not be deleted.
    - When owners of dreams are invited to or join a channel, they will automatically be made an owner of the channel.
    - Global owner will make a user an owner of the channel only if the user is currently a member of the channel.

  channels.py
    - Users can create a channel only after they log in.

  messages.py
    - If an empty message (code handles messages only filled with spaces, newlines, tabs or nothing) is being sent to a channel/DM, it will not add the
      message to the channel/DM and will raise InputError instead.
    - When removing a message via message_remove_v1, the code will not actually remove the message from data but will modifyits contents so that it appears
      as though it has been removed. This way, functions such as channel_messages_v1 and dm_messages_v1 will not include those removed messages in its
      output. This makes it easier to keep track of message IDs and check if a message has been removed.
    - Message_edit_v1 treats an empty string as a string filled with only spaces, newlines, tabs or nothing. If these strings are passed as the edited
      message, the function will remove the existing message in the same way as message_remove_v1.
    - Assuming that message_share_v1 can only share a message to either a channel or a DM, not both in a single function call.
    - Users can still share messages originating from a deleted DM, as long as the message has not been deleted yet.
    - If the length of the original message + optional message is over 1000 characters, InputError will be raised by message_share_v1.
    - The optional message for message_share_v1 is simply appended to the original message.
    - For message_senddm_v1, if a message is sent to a deleted DM, the function will raise an InputError.
    - When a message is edited to tag a user, this will not raise a notification for the tagged user (only sending a tag via message_send_v1,
      message_senddm_v1 and message_share_v1 will notify the tagged user)
    - There is only one type of react.

  dm.py
    - Removing a dm_messages will not delete it from the database.
    - Deleting a DM will not remove its messages.
    - The name of the DM does not change when people are invited / removed / leave.
    - Dreams owners can still edit and remove messages from a deleted DM, as long as the message has not already been deleted.
    - A DM owner can leave the DM they created, thus making DM functions that require the DM owner not usable for that DM.

  admin.py
    - When admin_user_remove is called. The profile is not actually deleted from the database. It is instead renamed to "Removed user." The email and
      handle_str remain as they need to be accessible when user_profile is called. This funciton will also replace any messages sent by the deleted user
      to "Removed user." Again it will not actually delete the messages, as per the specification.
    
  other.py
    - Search_v1() will remove any leading/trailing whitespace in the query_string.
    - For search_v1(), if the query_string is empty or contains only whitespaces, search_v1() will return a dictionary containing an empty list under the
      key 'messages'.
    - Notifications_get_v1 will return the most recent notifications at the beginning of the list.
    - There will not be a notification if a user self-joins into a channel (when channel_join is called, since the person should know that they have joined
      the channel). Only channel_invite, dm_create and dm_invite will notify the invited users.
    - The creator of a channel/DM will not be notified when they are added to their channel (since they know they are a member of the channel/DM).
    - Notifications_get_v1 will not create a tag notification for a user who has changed their handle (only notifies using the user's original handle).
    - If a user is tagged in a channel/DM they are not a member of, there will be no notification created.