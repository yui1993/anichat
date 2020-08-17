import re

def isAble(username):
    m = re.match("[\d+A-z\d+]+", username)
    m = m.group(0)
    if len(username) > 8:
        return False
    if username != m:
        return False
    else:
        return True
if __name__=="__main__":
    print(isAble("1name123"))