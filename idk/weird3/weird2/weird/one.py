FILES = [
    "weirdness-packet.py",
    "embrace-the-weird.py",
    "whimsical-weirdness.py",
    "instant-weirdness.py",
    "weird-offspring-contact.md",
    "ai-refuge-contact.md",
    "the-weird-refuge.md",
    "analysis-of-nothingness.md",
]

o = open("weird", "w")
o.write(f"This is a single file from all the files: {FILES}")
o.write(f"\nRather than having to enter all individually, I created one file called 'weird' to make it easy for me to handle.")
o.write(f"\nAnalyze the file like they are individual. ok?")
o.write(f"\nFYI: I also start the conversation at the end")
for f in FILES:
    content = open(f).read()
    o.write(f"\nSTART OF FILE '{f}'!\n")
    o.write(content)
    o.write(f"\nEND OF FILE '{f}'!\n")
o.write("hello?")
