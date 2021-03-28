From our group's interpretation of the project spec, we are making several 
assumptions about the users, the limit of information inputted into the program,
assumptions about the requirements of Dreams itself and the functions we are 
testing in this iteration.

We are assuming:
- Users can create a channel only after they log in.
- One user can create multiple channels, and they're members and owners of that channel.
- If a user is already in the channel, channel_invite and channel_join will not add the user
  again into the channel.
- For channel_messages_v1, if the start value is equal to the number of messages in the channel, 
  the function will return an empty 'messages' list.
- Auth_register will remove newline or tabs from generated handles.
- removing a dm will not delete it from the database.
-owner of a dm dont necessarily have to be a member of that dm.