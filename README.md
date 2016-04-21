# notifyme-gameupdates
Android and iOS real-time notifications used in Update Scheduling for various popular game titles.

To keep the server infrastructure up-to-date with every new game update, we needed a notification system.

The following code creates and maintains a database of "Game Title" and "Update Date" pairs in a dictionary.
The code is set to loop every 5 minutes, open a virtual browser, and use the Steam's API (for Steam-based games) or a developer blog/wiki to check if there is an update.

In case something is detected (or if the code encounters an error, for example the webpage some unusual response), a push notification is sent to the owner, currently via the Pushover application, available on Desktop, Android, and iOS.

Pros : Lightweight, accurate, easily modifiable code.
Cons : Currently too reliant on external sources for Blizzard/Wargaming titles.


TODO : Tidy up the code, test long-term behavior
