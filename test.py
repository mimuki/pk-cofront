from pluralkit import Client

# keep token not in this file, for obvious reasons
from config import TOKEN
pk = Client(TOKEN, async_mode=False)

system = pk.get_system()
print(f"Hi, {system.name}!")

# Ask for combo members
inputMembers = input("Write the names or IDs of who you'd like to combo: ")
# Lowercase it, so that it's not case sensitive
inputMembers = inputMembers.lower()
# Turn it into a list, split by spaces
# This breaks multi word names, but those suck anyway
inputMembers = inputMembers.split(' ')
# remove extra strings from stuff like double spaces
inputMembers = list(filter(None, inputMembers))

comboMembers = [] 
names = [] # For member making
nicks = [] # For display name making
print(f"Thanks.\nI'm going to try and combine these members:")
for member in inputMembers:
    print(f"- {member}")
# Actually get your system list from pk
members = pk.get_members()

for inputMember in inputMembers:
    print(f"Searching for \033[96m{inputMember} \033[0min your system.")
    print(f"{(inputMembers.index(inputMember))} of {len(inputMembers)} members processed so far.")
    found = False
    for member in members:
        if inputMember == member.name.lower():
            print(f"\033[32mSuccess!\033[0m Found \033[36m{inputMember}\033[0m in system list.")
            comboMembers.append(member)
            found = True
    if not found:
        print(f"Couldn't find {inputMember}.")
        break

print("Input processed! I'm going to combine these members:")
for member in comboMembers:
    print(f"- {member.name} (nickname: {member.display_name})")
    names.append(member.name)
    if member.display_name:
        nicks.append(member.display_name)
    else:
        nicks.append(member.name)

comboName = "+".join(names)
comboNick = "・".join(nicks)
print(system.tag)
if len(comboNick) + len(system.tag) + 1 > 80 or len(comboName) > 80:
    print("This combination's name or display name is too long for Pluralkit.")
    print(f"The combo member's name has {len(comboName)} characters, their display name has {len(comboNick)} characters, and your system tag has {(len(system.tag)+1)} characters.")
    print(f"The max total webhook length is 80 characters, but you have {(len(comboNick) + len(system.tag) +1)}. Your name length is {len(comboName)}.")
else:
    print("Their name when sending messages is:")
    print(comboNick)
    print("Their name for running commands is:")
    print(comboName)
    found = False
    for member in members:
        if member.name == comboName:
            print(f"{member.name} already has a member!")
            found = True
    if found == False:
        print("You don't have a PK member yet")
    else:
        print("You already have a member!")
