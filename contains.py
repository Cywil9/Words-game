def freq_count(letters):
    """ Given a string of letters, return a dictionary
        which associates a frequency count with each letter. """
    f_count = {}
    for char in letters:
        f_count.setdefault(char, 0)
        f_count[char] += 1
    return f_count

def contains(source_word, what):
    """ Returns True if the letters that make up "what" are 
        contained in the letters that make up "source_word", 
        otherwise False is returned. """
    sc = freq_count(source_word)
    wc = freq_count(what)
    for letter, count in wc.items():
        if sc.get(letter, 0) < count:
            return False
    return True

if __name__ == "__main__":
    # A few tests/assertions to make sure things behave as expected.
    assert contains("admission", "sin") == True
    assert contains("admission", "soon") == False
    assert contains("admission", "miss") == True
    assert contains("admission", "moon") == False
    assert contains("admission", "admin") == True
    assert contains("admission", "dismiss") == False
    assert contains("admission", "sins") == True
    assert contains("admission", "missing") == False
