From our group's interpretation of the project spec, we are making several 
assumptions about the users, the limit of information inputted into the program,
assumptions about the requirements of Dreams itself and the functions we are 
testing in this iteration.

We are assuming:
- Users can create a channel only after they log in.
- ### One user can create multiple channels, and they're members and owners of 
  ### that channel.
- If a user is already in the channel, channel_invite and channel_join will not 
  add the user
  again into the channel.
- For channel_messages_v1, if the start value is equal to the number of messages 
  in the channel, 
  the function will return an empty 'messages' list.
- Auth_register will remove newline or tabs from generated handles.
<<<<<<< HEAD
- ### Removing a dm will not delete it from the database
- Empty channels (When the last member leaves) will not be deleted.
- When owners of dreams are invited to or join a channel, they will 
  automatically be made an owner of the channel.
- channel_owner_v1 will make a user an owner of the channel only if the user is 
  currently a member of the channel.
- search_v1() will remove any leading/trailing whitespace in the query_string
- For search_v1(), if the query_string is empty or contains only whitespaces,
  search_v1() will return a dictionary containing an empty list under the key
  'messages'

- removing a dm will not delete it from the database.
- Owner of a dm dont necessarily have to be a member of that dm.
- Members of DM are stored in the order they are entered, not alphabetical order.
- The name of the DM does not change when people are invited / removed / leave. 

