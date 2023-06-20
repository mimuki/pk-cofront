from pluralkit import Client
import asyncio
# keep token not in this file, for obvious reasons
from config import TOKEN
pk = Client(TOKEN)

async def main():
    system = await pk.get_system()
    print(system.description)

    # pray they don't have multi word names ig
    inputMembers = input("Write the names or IDs of who you'd like to combo: ").lower().split(' ')
    # remove extra strings from stuff like double spaces
    inputMembers = list(filter(None, inputMembers))
    print(inputMembers)
    # As we loop through and find members we know, we remove them from unknownMembers
    unknownMembers = inputMembers

    # Get all the members in system
    members = pk.get_members()
    # Make combo members a dummy list
    # helps with making the order good later
    comboMembers = []
    i = 0
    while i < len(inputMembers):
        comboMembers.append("")
        i = i + 1

    # For each member in the system...
    async for member in members:
        # print(f"{member.name} (`{member.id}`)")
        # For each member you manually wrote
        for inputMember in inputMembers:
            # If it matches
            # this doesn't make sure you didn't enter the same name twice, rip
            if inputMember == member.name.lower():
                # What order the member was mentioned in the input
                # first = 0, second = 1, etc
                # this breaks a lot and idk why
                index = inputMembers.index(inputMember)
                print("Recognized " + member.name + " at position " + str(index))
                comboMembers[index] = member
                # removing by name, because index won't be kept
                # (i.e. if theres 2 people and you remove the first one,
                # the second would get mad bc its index doesnt exist now
                unknownMembers.remove(member.name.lower())

    # If after all of that, some input members werent removed
    if unknownMembers != []:
        print("There were some members I couldn't match.")
        print("Check that you wrote these names correctly, as in PK:")
        for member in unknownMembers:
            print("  " + member)
        print("If you are sure that's right, maybe you entered that name twice idk")
        print("do you expect me to catch that kind of error in a project like this")
    elif comboMembers == []:
        print("No members specified")
    elif len(comboMembers) == 1:
        print("you cant combine one member tf")
    else: # seems legit
        names = []
        print("Looks good! Going to combine these members:")
        for member in comboMembers:
            print("  " + str(member.name))
            names.append(str(member.name))
        print("・".join(names))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
