# create list of my cart
inv = []

# create gameinfo dictionary
gameinfo = {}

map = {}
# instruction of the game, automatically output in your location.
gamefile = open("game1.txt", "r")
lines0 = [0]
lines1 = [1]
for pos, line in enumerate(gamefile):
    #lines = gamefile.readlines()
    word = line.strip()
    content = word.split(':')
    if pos in lines0:
        print('Welcome to', content[1])
    if pos in lines1:
        print('The goal of this game is to:' + content[1])

# initialize line=0
line = 0
with open("game1.txt") as game:
    for aline in game:
        aline = aline.strip()
        line = line + 1
        if aline == '---':
            break
        info = aline.split(':')
        gameinfo[info[0]] = info[1]
# initialize game size as x-axis and y-axis
x = int(gameinfo['game_xsize'])
y = int(gameinfo['game_ysize'])
# size of game = 3*3
size = x*y

with open("game1.txt") as game:
    for i in range(line):
        next(game)
    for i in range(size):
        map[i+1] = {}
        for aline in game:
            aline = aline.strip()
            if aline == '---':
                break
            # r represents _ after
            r = aline.split('_')[1]
            # rect separate the colon before and after to form a list
            # e.g['id', '1']
            # ['desc', ' standing next to a lake. The water is murky.']
            # ['obj', ' cart']
            # ['id', '2']
            rect = r.split(':')

            if rect[0] == 'obj':
                map[i+1]['obj'] = rect[1]

            else:
                map[i+1][rect[0]] = rect[1]
            #print(map[i])
# show your current location
def show_desc(k):
    for keys in map[k]:
        if keys == 'desc':
            return(map[k]['desc'].lstrip())
# search the hidden object, and turn it into visible
def hiddenobj(k):
    #for keys in map[k]:
        #if keys == 'hiddenobj':

            # Check if key exist in dict or not
            if 'obj' in map[k]:
                # Key exist in dict.
                # Check if type of value of key is list or not
                if not isinstance(map[k]['obj'], list):
                    # If type is not list then make it list
                    map[k]['obj'] = [map[k]['obj']]
                # Append the value in list
                map[k]['obj'].append(map[k]['hiddenobj'].lstrip())
            else:
                # As key is not in dict,
                # add key-value pair
                map[k]['obj'] = map[k]['hiddenobj']

            return "You found a" + map[k]['hiddenobj']

"""
map[7]['obj'] = [map[7]['obj']]
map[7]['obj'].append(map[7]['hiddenobj'])
print(map[7]['obj'])
"""
# check if there is a hiddenpath
def hiddenpath(k):
    for keys in map[k]:
        if keys == 'hiddenpath':
            return "You found a hidden path!"
# if there is a hiddenpath, move it
def movepath(k):
    for keys in map[k]:
        if keys == 'hiddenpath':
            return(map[k]['hiddenpath'])
# check if there is a object
def isobject(k):
   if 'obj' in map[k]:
       if not isinstance(map[k]['obj'], list):
           map[k]['obj'] = [map[k]['obj'].lstrip()]
       return 'There are' + str(map[k]['obj']) + ' ' + 'here'
   #else:
       #return 'nothing'



# take the object if it exists
def take_obj(cnoun, k):
    for keys in map[k]:
        if keys == 'obj':
            if cnoun in map[k]['obj']:
                inv.append(cnoun)
                map[k]['obj'].remove(cnoun)
# check if you win(when dropping helmet in secret house to Hans
def win():
    if 'obj' in map[8]:
        if 'helmet' in map[8]['obj']:
            return "You win!"
        else:
            return "You have not won"
    else:
        return "You have not won"
#hiddenobj(7)
#print(isobject(7))
"""
inv = ['milk']
take_obj(1)
print(inv)
"""
#def drop_obj(k):

    #inv.remove(map[k]['obj'])
#map[5]['obj'] = ' '+ 'haha'
#print(isobject(5))

"""
take_obj(1)
print(isobject(1))
print(inv)
"""
loc = int(gameinfo['game_start'])
print('you are', show_desc(loc))
while True:
    cmd = input("What's next?")
    if cmd == 'exit':
        break
    elif cmd == 'inv':
        print(" ", inv)
    elif cmd == 'goal':
        print(gameinfo['game_goal'])
    # search
    # 1. a hidden path
    elif cmd == 'search':
        if hiddenpath(loc) is not None:
            print(hiddenpath(loc))
        # 2. a hidden object
        # turn it visible
        print(hiddenobj(loc))
    else:
        # split the command into 2 parts
        cmd_parts = cmd.split()
        cverb = cmd_parts[0]
        cnoun = cmd_parts[1]
        # take the object if it exists in the location currently
        if cverb == 'take':
            if isobject(loc) is not None:
                #if cnoun == isobject(loc)[11:15]:
                    #print(cnoun)
                    #print(isobject(loc))
                take_obj(cnoun, loc)
            else:
                print('That object is not here.')
        # drop object if it exists in your inventort
        if cverb == 'drop':
            if cnoun in inv:
                map[loc]['obj'] = ' '+cnoun
                inv.remove(cnoun)
            else:
                print("There is no such object in your inventory!")
        if cverb == 'move':
            # move north
            if cnoun == 'north':
                if loc <= x:
                    loc = loc + size - x
                else:
                    loc = loc - x
            # move south
            # 5, 9 have different rules of moving
            if cnoun == 'south':
                if loc > x*(y-1) and loc != 9:
                    loc = loc + x - size
                # if loc=5,move south to 2
                elif loc == 5:
                    loc = loc - x
                elif loc == 9:
                    loc = loc
                else:
                    loc = loc + x
            # move wast
            # 9 has the different rule of moving
            if cnoun == 'west':
                if loc % x == 1 and loc != 9:
                    loc = loc + x - 1
                elif loc == 9:
                    loc = loc
                else:
                    loc = loc - 1
            # move east
            # 9 has the different rule of moving
            if cnoun == 'east' and loc != 9:
                if loc % x == 0:
                    loc = loc - x + 1
                elif loc == 9:
                    loc = loc
                else:
                    loc = loc + 1
            # if there is a hidden path, move path
            if cnoun == 'path':
                loc = int(movepath(loc))
            # tell you your current location
            print('you are ', show_desc(loc))
            # check the object in the location
            print(isobject(loc))
            # check if you win(There is a little redundant here, I am keeping adjusting it to not appear each time.Sorry)
            print(win())

