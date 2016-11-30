import base64
import string
import itertools
from collections import Counter

def hex_to_b64(instr):
    """ converts hex to base64 """
    bytesin = bytes.fromhex(instr)
    bytesout = base64.b64encode(bytesin)
    return bytesout

def hexxor(in1, in2):
    """ does xor on in1 and in2 (equal length hex strings) """
    b1 = bytes.fromhex(in1)
    b2 = bytes.fromhex(in2)
    ob = bytearray()
    for ix in range(len(b1)):
        ob.append(b1[ix] ^ b2[ix])
    return ob.hex()


def make_cleartext(t, k):
    """ utility for doing a bytewise xor """
    o = bytearray()
    for c in t:
        o.append(c ^ k)
    return bytes(o)

letters_and_space = set(ord(x) for x in string.ascii_letters + ' ')
printable_set = set(ord(x) for x in string.printable)

def score_cleartext(ct):
    """ score a cleartext on its "English-ness".
    Zero anything with non-printable characters.
    A point for every one of the 12 most common letters amongst the text's 6 most common letters. Subtract a point for every
    character that is not a letter or space.
    """
    if set(ct) - printable_set:
        return 0
    lowered = ct.lower()
    counted = Counter(lowered)
    etaoin = set(x for (x,y) in counted.most_common(6))

    score = len(etaoin & set(b"etaoinshrdlc"))
    score -= len(set(ct) - letters_and_space)
    return score

def ranked_cleartext(text):
    """ choose the best line assuming line was encoded with single-character xor """
    choices = []
    t = bytes.fromhex(text)
    for k in bytes(range(256)):
        ct = make_cleartext(t, k)
        sc = score_cleartext(ct)
        choices.append((sc, k, ct))
    choices = [c for c in choices if c[0]]
    choices.sort(reverse=True)
    return choices

def probe_file_for_secret(fn):
    """ find a line encoded with single-character xor """
    mebbe = []
    with open(fn) as f:
        for num, line in enumerate(f):
            line = line.strip()
            results = ranked_cleartext(line)
            for (s, k, t) in results:
                if s > 0:
                    mebbe.append((s, num, k, t))
    mebbe.sort(reverse=True)
    return mebbe

def encode_rk_xor(key, cleartext):
    text = cleartext.encode('utf-8')
    keys = itertools.cycle(key.encode('ascii'))
    o = bytearray()
    for c in text:
        o.append(c ^ next(keys))
    return o.hex()


