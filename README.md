# Star-Citizen-commodities-averages
This is a discord bot that uses the uexcorp api to find up-to-date commodities. this was made by me and Ossuno for personal use up until now

# How to use the bot
You will want to replace the bot_token with your actual discord bot token. Then run it in python!

# What commands are available
currently the only functioning command is     !commodities_averages     followed by the integer ID of your commodity
However, the uexcorp has a bunch of other commands available with their API so you are welcome to edit this code to add any commands from https://uexcorp.space/api/documentation/id/commodities

# Important Notices!
the chunk_size function should remain at 1800, anything different may result in cutting off the text before sending the second message. And anything above 1900+ would cause discord to block the message
