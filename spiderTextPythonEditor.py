with open("spiderManIn") as f:
    with open("spiderManOut", "w") as out:
        for line in f:
            if len(line.split()) == 14:
                out.write("vertex "+line)
            elif len(line.split()) == 4 and line[0] == "3":
                out.write("polygon "+line)
            else:
                out.write(line)
