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
    if set(ct) - printable_set:
        return 0
    lowered = ct.lower()
    counted = Counter(lowered)
    etaoin = set(x for (x,y) in counted.most_common(6))

    score = len(etaoin & set(b"etaoinshrdlc"))
    score -= len(set(ct) - letters_and_space)
    return score


FREAK = {
    'E': .1270, 'T': .0906, 'A': .0817, 'O': .0751, 'I': .0697,
    'N': .0675, 'S': .0633, 'H': .0609, 'R': .0599, 'D': .0425,
    'L': .0403, 'C': .0278, 'U': .0276, 'M': .0241, 'W': .0236,
    'F': .0223, 'G': .0202, 'Y': .0197, 'P': .0193, 'B': .0129,
    'V': .0098, 'K': .0077, 'J': .0015, 'X': .0015, 'Q': .0010,
    'Z': .0007}

for c in string.punctuation + string.whitespace:
    FREAK[c] = .0005
FREAK[' '] = .0050


def score_cleartext(text):
    """ score a cleartext on its "English-ness".
    We use a chi-square distance between "expected" (probable) content of the string, and actual content.
    Weights for punctuation/whitespace are entirely imaginary but seem to produce good signal.
    """
    up = text.upper()
    ct = Counter(up)
    test_statistic = 0
    for k in range(256):
        expected = float(FREAK.get(chr(k), 0.00001) * len(text))
        observed = float(ct.get(k, 0))
        test_statistic += (observed - expected)**2/expected
    return test_statistic

def ranked_cleartext(text):
    """ choose the best line assuming line was encoded with single-character xor """
    choices = []
    t = bytes.fromhex(text)
    for k in bytes(range(256)):
        ct = make_cleartext(t, k)
        sc = score_cleartext(ct)
        choices.append((sc, k, ct))
    choices.sort()
    return choices[0]

def probe_file_for_secret(fn):
    """ find a line encoded with single-character xor """
    mebbe = []
    with open(fn) as f:
        for num, line in enumerate(f):
            line = line.strip()
            (s, k, t) = ranked_cleartext(line)
            mebbe.append((s, num, k, t))
    mebbe.sort()
    return mebbe[0]

def encode_rk_xor(key, cleartext):
    text = cleartext.encode('utf-8')
    keys = itertools.cycle(key.encode('ascii'))
    o = bytearray()
    for c in text:
        o.append(c ^ next(keys))
    return o.hex()


