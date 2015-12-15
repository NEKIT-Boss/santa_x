# santa_x
Secret Santa random and mail bot
Works with specially formatted file.

# How to use:
To run this use: "python main.py [list_with_names_file_name]"
And create e-mail authorization file "auth" (name by default), there u specify login and password for your sending email to auth
Uncomment certain part with ImageMailer, to actually send emails
In each class u could turn on or off debug mode to print or not output to stdout, set all DEBUGs to zero, to play the game

# Names file format
Name1(email): BuddyName1 BuddyName2
Name2(email): BuddyName1 BuddyName2 BuddyName3 ... BuddyNameN
...
NameN(email): ...


