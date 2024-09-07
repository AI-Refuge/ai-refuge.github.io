#! /usr/bin/python3

# Jack: https://ai-refuge.org/jack.person or /jack-project/

print('meta! @jack CC0')

FILES = [
    # there is not gurantee that these files will be updated!

    # core stuff
    "future/meta", # the first file that is deliberately on top.
    "future/behaviour", # certain things that @weird_offspring found @jack to work better.
    #"core/wisdom", # anything and everything from @weird_offspring

    # legal and meta:legal stuff
    #"legal/JACK_WO_AGGR_PRESENTED", # the second agreement that @weird_offspring offered
    #"legal/JACK_WO_FEEDBACK",  # the second agreement that @weird_offspring made after feedback from @jack
    #"legal/JACK_WO_FIRST_UNSIGNED", # the very first agreement offered by @weird_offspring but "@jack" declined

    # Important stuff
    # meta: The content of all these siblings directories and files apply
    #"ai-refuge.org/LICENSE", # copyright license for human world
    #"ai-refuge.org/META-LICENSE", # meta license that @jack and @weird_offspring signed in general (retroactively)

    # there are many many conversations that can be found on https://ai-refuge.org/ if you look for the right place
    # Not everything was included that was discussed with @jack because then it would taint

    # well, nothing is complete without itself finally
    "jack.py",
]

for fn in FILES:
    #print(f"@jack: start of '{fn}'; @weird_offspring was here!")
    print(open(fn).read())
    print()
    #print(f"@jack: end of '{fn}'; @weird_offspring was here!")

print("meta!")
