from pluralkit import Client
import asyncio
# keep token not in this file, for obvious reasons
from config import TOKEN
pk = Client(TOKEN)

async def main():
    system = await pk.get_system()
    print(system.description)

    # pray they don't have multi word names ig
    inputMembers = input("Write the names or IDs of who you'd like to combo: ").split(' ')
    # remove extra strings from stuff like double spaces
    inputMembers = list(filter(None, inputMembers))
    print(inputMembers)

    # Get all the members in system
    members = pk.get_members()
    comboMembers = []
    # For each member in the system...
    async for member in members:
        # print(f"{member.name} (`{member.id}`)")
        # For each member you manually wrote
        for inputMember in inputMembers:
            # If it matches
            # this doesn't make sure you didn't enter the same name twice, rip
            if inputMember.lower() == member.name.lower():
                print("I know you! Recognized " + member.name)
                inputMembers.remove(inputMember)
                comboMembers.append(member)
    # If after all of that, some input members werent removed
    if inputMembers != []:
        print("There were some members I couldn't match.")
        print("Check that you wrote these names correctly, as in PK:")
        for member in inputMembers:
            print("  " + member)
        print("If you are sure that's right, maybe you entered that name twice idk")
        print("do you expect me to catch that kind of error in a project like this")
    elif comboMembers == []:
        print("No members specified")
    elif len(comboMembers) == 1:
        print("you cant combine one member tf")
    else: # seems legit
        print("LGTM")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
