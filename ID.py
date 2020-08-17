import random, hashlib

def generate():

    abc="abcdefghijklmnopqrstuvwxyz"
    abc_up = abc.upper()
    number = "0123456789"
    symbols = "!@@#$%^&*()_-+=:;{}[]/\\><.,"
    j = []
    for x in abc:
        j.append(x)
        random.shuffle(j)
    for x in abc_up:
        j.append(x)
        random.shuffle(j)
    for x in number:
        j.append(x)
        random.shuffle(j)
    for x in symbols:
        j.append(x)
        random.shuffle(j)

    ret = "".join(j)
    h = hashlib.sha256()
    h.update(ret.encode())
    return h.hexdigest()

if __name__=="__main__":

    while True:
        print(generate())