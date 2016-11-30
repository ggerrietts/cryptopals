
import unittest
from src import set1 as s1

class TestChallenge1(unittest.TestCase):
    def test_hex_to_b64(self):
        given = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        expected = b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        received = s1.hex_to_b64(given)
        self.assertEqual(received, expected)

    def test_hexxor(self):
        given_1 = "1c0111001f010100061a024b53535009181c"
        given_2 = "686974207468652062756c6c277320657965"
        expected = "746865206b696420646f6e277420706c6179"
        received = s1.hexxor(given_1, given_2)
        self.assertEqual(received, expected)

    def test_ranked_cleartext(self):
        given = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
        expected = b"Cooking MC's like a pound of bacon"
        score, key, cleartext = s1.ranked_cleartext(given)
        self.assertEqual(expected, cleartext)
        self.assertEqual(88, key)

    def test_probe_file(self):
        given = "src/4.txt"
        result = s1.probe_file_for_secret(given)
        score, line, key, cleartext = result
        self.assertEqual(b"Now that the party is jumping\n", cleartext)
        self.assertEqual(170, line)
        self.assertEqual(53, key)

    def test_encode_rk_xor(self):
        given = (
            "Burning 'em, if you ain't quick and nimble\n"
            "I go crazy when I hear a cymbal"
        )
        expected = (
            "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272"
            "a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
        )
        o = s1.encode_rk_xor('ICE', given)
        self.assertEqual(expected, o)





