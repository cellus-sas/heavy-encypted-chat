heavy-encypted-chat
===================

python encrypted chat based on auto-changing key encryption every n seconds



The wish of this program is to limit the avaibility of DPI technology owner to easily catch and decrypt the flow of packets between two or more chatters. 

how it s done ?
With sharing an big list of timestampted keys then changing the key every n seconds.
In that way more long you want to decrypt, less affordable (& more expansive) is it.

This method force to allow brutforce-only method for decrypt content.

Some default are present:

- more you want to be secured more the list of key is bigger
(if you want changing the key every 10 second you have to think about 4 Go/years for keys)

- the time/cost for the generation of keys 
it s relative to the key regeneration delta time

- the necessity that both devices use by chatter are safe 
If not: the bad people could get the list of keys then with some studies use it to decode the encrypted content in packet 
or read directly the clear text on harddrive.

- default relative to the consequence of sharing an heavy list of timestamped key
 > the best way is to use usb drive/flash/sd/dvd to share hand by hand and person to person. (read only format like DVD or CD is better and more easy to destroy than hdd)
 > it is important to never share the key list by internet !!! 
    if you have no other solution try using with (VPN) + SSH + HTTPS + (smart card) but don't use weak way like http seving or ftp or every other online hosting service

- default relative to NAT rule if you want to be able to receive content if you are behind a router 


The program is composed with a main program using 5 sub element:
 main program
 sub element:
  - a part to maintain the good timestamped key
   serve the good key at good moment for encrypt content to send or decrypt content to receive
  - a part for web-gui (based on html+jquery)
   web page with function which reload the content from a json file
  - a part for gui back office
   - part who update the json file with clear content receive
   - part who is subdiviside in 3 part
    - part who serve an http server to receive parameter from gui
    - part who serve an http server to receive encrypted data from remote server and decrypt
    - part who serve an http server to receive clear data then encrypt and send to remote server
  - a part for telecomunication beetween the different gui-back-office part
  - a part for generating key table required for enryption

