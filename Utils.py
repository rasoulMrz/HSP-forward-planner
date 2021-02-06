def read_lines(file_name):
    lines = open(file_name).readlines()
    lines = filter(lambda l: l != "\n", lines)
    lines = list(map(lambda l: l[:-1].lower(), lines))
    lines.reverse()
    return lines

def read_def(lines, title=None):
    t, count = lines.pop().split(":")

    if(title is None):
        return t, int(count)

    assert t == title
    return int(count)