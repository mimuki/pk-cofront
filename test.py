RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
RESET = '\033[0m'

comboMembers = [] # The member objects of each member to combine
names = [] # The names of each member to combine
nicks = [] # The display names of each member to combine
ids = [] # The IDs of each member to combine


from pluralkit import Client, Privacy, AutoproxyMode
# keep token not in this file, for obvious reasons
try:
    from config import TOKEN, MODE
except ModuleNotFoundError:
    print(f"{RED}Could not find config.py.{RESET}")
    config = open("config.py", "w")
    config.write("TOKEN = '' # get yours by running `pk;token` in Discord\nMODE = 'autoproxy' # options: 'autoproxy', 'switch' ")
    config.close()
    print("You need to manually edit that file, and put your token in it.")
    exit()
pk = Client(TOKEN, async_mode=False)

system = pk.get_system()
if system.name == None:
    print("Connected successfully!")
else:
    print(f"Hi, {CYAN}{system.name}{RESET}!")
print("This is a tool that combines members into a single member,")
print("so you can proxy as all of them.\n")
# Ask for combo members
inputMembers = input("Enter names of members to combine: ").lower().split(' ')
# remove extra strings from stuff like double spaces
inputMembers = list(filter(None, inputMembers))

print("Thanks.\nI'm going to try and combine these members:")
for member in inputMembers:
    print(f"- {CYAN}{member}{RESET}")
# Actually get your system list from pk
members = pk.get_members()

for inputMember in inputMembers:
    print(f"Searching for {CYAN}{inputMember}{RESET} in your system.")
    print(f"{CYAN}{(inputMembers.index(inputMember))}{RESET} of {CYAN}{len(inputMembers)}{RESET} members processed so far.")
    found = False
    for member in members:
        if inputMember == member.name.lower():
            print(f"{GREEN}Success!{RESET} Found {CYAN}{inputMember}{RESET} in system list.")
            comboMembers.append(member)
            found = True
    if not found:
        print(f"{RED}Couldn't find {inputMember}.{RESET}")
        exit()

print("Input processed! I'm going to combine these members:")
for member in comboMembers:
    print(f"- {CYAN}{member.name}{RESET} (nickname: {CYAN}{member.display_name}{RESET})")
    names.append(member.name)
    if member.display_name:
        nicks.append(member.display_name)
    else:
        nicks.append(member.name)

comboName = "+".join(names)
comboNameDesc = "`\n`pk;m ".join(names)
comboNick = "・".join(nicks)

# If it would break PK (doesn't check server tag)
if len(comboNick) + len(system.tag) + 1 > 80 or len(comboName) > 80:
    print("{RED}This combination's name or display name is too long for Pluralkit.{RESET}")
    print(f"Member name length: {len(comboName)} characters")
    print(f"Display name length: {len(comboNick)} characters")
    print(f"System tag length: {(len(system.tag) +1)}")
    print(f"Combined webhook name length: {(len(comboNick) + 1 + len(system.tag))}")
    print("\nOne of these is above the limit of 80 characters.")
    exit()
else: # Should be fine
    print("Their name when sending messages is:")
    print(f"- {CYAN}{comboNick}{RESET}")
    print("Their name for running commands is:")
    print(f"- {CYAN}{comboName}{RESET}")
    found = False
    for member in members:
        if member.name == comboName:
            print(f"Combo member {CYAN}{member.name}{RESET} already exists in pluralkit.")
            comboMember = member
            found = True
    if found == False:
        desc = f'This is the combination of multiple seperate members into a single Pluralkit proxy.\n\nFor more information, see:\n`pk;m {comboNameDesc}`'
        print(f"Combo member {CYAN}{comboName}{RESET} doesn't exist in pluralkit, let me make them for you!")
        comboMember = pk.new_member(
                comboName, 
                display_name=comboNick, 
                description=desc, 
                visibility=Privacy.PRIVATE,
                )
        print(f"Created {CYAN}{comboName}{RESET} successfully!")
    if MODE == 'autoproxy':
        print(f"Autoproxy mode selected. This works like running pk;ap {comboName} does in Discord.")
        print(f"Because I'm not discord, I need you to tell me what server you want to autoproxy in. (If you don't want to run this for every server you're in, consider trying {CYAN}MODE = 'switch'{RESET} in config.py.)")
        guild = input("Enter the server ID for the server you want to proxy in: ")
        pk.update_autoproxy_settings(guild, AutoproxyMode.MEMBER, autoproxy_member=comboMember)
    elif MODE == 'switch':
        print(f"Switching in {CYAN}{comboName}{RESET}...")
        pk.new_switch(comboMember)
        print(f"{GREEN}Switch successful!{RESET} Make sure to run {CYAN}pk;ap front{RESET} in any servers you want to autoproxy in, if you haven't already.")
    else:
        print(f"{RED}Invalid mode selected.{RESET}")
        print(f"Check your config.py; the only options I take are {CYAN}MODE = 'autoproxy'{RESET}")
        print(f"and {CYAN}MODE = 'switch'{RESET}\n")
        exit()
