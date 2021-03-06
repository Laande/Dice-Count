import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction, HMessage

extension_info = {
    "title": "Count dice",
    "description": "Count the total for you",
    "version": "2.0",
    "author": "Lande"
}

ext = Extension(extension_info, sys.argv)
ext.start()


cata_dice = ["886735784", "284", "886738926", "886732682"]

"""
    little list of dice :

    dice magique : 284
    dice or : 886738926
    dice marijuana : 886732682
    dice casino : 886735784

    dice vert : 886733119
    dice rouge&blanc : 886732711
    dice néon jaune : 886732697
    dice usa : 886732696
    dice profondeur : 886732695
    dice néon bleu : 886732694
    dice skrillex : 886732691


    newdice : 886732714
    wired dice : 886736185
"""

count = 0
around = []


def dice_moove(message):
    global count
    (_, idd, x, y, _, _, _, _, _, etat, _, _, _) = message.packet.read("iiiiissiisiii")
    idd = str(idd)
    if idd in cata_dice:
        if int(etat) > 0:
            if around:
                if around[0]-1 <= x <= around[0]+1:
                    if around[0]-1 <= y <= around[0]+1:
                        count += int(etat)
                        ext.send_to_client('{l}{h:1446}{i:0}{s:" ' + etat + ' => ' + str(count) + ' "}{i:0}{i:1}{i:0}{i:0}')
            else:
                count += int(etat)
                ext.send_to_client('{l}{h:1446}{i:0}{s:" '+etat+' => '+str(count)+' "}{i:0}{i:1}{i:0}{i:0}')


def speech(message):
    global count
    global around
    (text, color, index) = message.packet.read('sii')
    if text == ":creset":
        message.is_blocked = True
        count = 0
        ext.send_to_client('{l}{h:1446}{i:0}{s:"Count reset"}{i:0}{i:1}{i:0}{i:0}')
    if text == ":around reset":
        around = []
        return ext.send_to_client('{l}{h:1446}{i:0}{s:"Around reset"}{i:0}{i:1}{i:0}{i:0}')
    if text.startswith(":around "):
        message.is_blocked = True
        text = text[8:]
        try:
            x, y = text.split(";")
        except ValueError:
            return ext.send_to_client('{l}{h:1446}{i:0}{s:"Format : `:around x;y`"}{i:0}{i:1}{i:0}{i:0}')
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            return ext.send_to_client('{l}{h:1446}{i:0}{s:"Only number available"}{i:0}{i:1}{i:0}{i:0}')

        around = [x, y]
        ext.send_to_client('{l}{h:1446}{i:0}{s:"Around to: '+str(x)+'x and '+str(y)+'y"}{i:0}{i:1}{i:0}{i:0}')


def room_change(message):
    around.clear()


ext.intercept(Direction.TO_CLIENT, dice_moove, 3776)
ext.intercept(Direction.TO_SERVER, speech, 1314)
ext.intercept(Direction.TO_CLIENT, room_change, 1301)
