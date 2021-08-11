#!/usr/bin/env python

import re
import os
import sys
import gnupg
import warnings
import platform
from secrets import randbelow as random
from os.path import join, expanduser, exists
from os import getenv
import argparse


# noinspection PyCompatibility
class DiceWare:
    class __PasswordResult:
        def __init__(self, password, codes):
            self.password = password
            self.codes = codes

        def __str__(self):
            return self.password

        def __repr__(self):
            return self.__str__()

    def __init__(self, gnupg_home=None, verbose=False, language=None):
        self.__verbose = verbose
        self.__file = None
        self.gnupg_error = None
        self.__gnu = self.__set_gnupg(gnupg_home)
        self.__lang = "en" if language is None else language
        self.dice_words = self.__init_list()

    def plain(self, n, spaces=True, capitals=False):
        password, codes = self.__password(n, spaces, capitals)
        return DiceWare.__PasswordResult(password, codes)

    def complex(self, n, w, spaces=True, capitals=False):
        password, codes = self.__password(n, spaces, capitals)
        return DiceWare.__PasswordResult(DiceWare.__insert_special_chars(w, password), codes)

    @staticmethod
    def alphanumeric(n):
        chars = [["ABCDEF", "GHIJKL", "MNOPQR", "STUVWX", "YZ0123", "456789"],
                 ["abcdef", "ghijkl", "mnopqr", "stuvwx", "yz"]]
        return DiceWare.__generate_random_characters(n, chars)

    @staticmethod
    def characters(n):
        chars = [["ABCDEF", "GHIJKL", "MNOPQR", "STUVWX", "YZ0123", "456789"],
                 ["abcdef", "ghijkl", "mnopqr", "stuvwx", "yz"],
                 ["!@#$%^", "&*()-=", "+[]{}\\", "|`;:'\"", "<>/?.,"]]
        return DiceWare.__generate_random_characters(n, chars)

    # Private methods
    def __init_list(self):
        re_obj = re.compile(r"(\d{5})[\t\s]+(.+)")
        file_name = join(DiceWare.get_script_path(),
                         "diceware-wordlist-{0}.asc".format(self.__lang))
        with open(file_name) as fh:
            text = fh.read()
        if self.__gnu:
            v = self.__gnu.verify(text)
            if not v.valid:
                self.gnupg_error = v.GPG_ERROR_CODES
                warnings.warn("Invalid signature of the Diceware word list", RuntimeWarning)
                print(self.gnupg_error)
        dice_words = {}
        for e in text.split("\n"):
            res = re_obj.match(e)
            if res:
                dice_words[res.group(1)] = res.group(2)
        return dice_words

    def __password(self, n, spaces, capitals):
        def _mapper(_code):
            _word = self.dice_words[_code]
            return _word[0].upper() + _word[1:] if capitals else _word
        codes = ["".join(str(random(6) + 1) for _ in range(5)) for _ in range(n)]
        password = (" " if spaces else "").join(map(_mapper, codes))
        return password, codes

    # noinspection PyMethodParameters,PyMethodMayBeStatic
    def __set_gnupg(self, gnupg_home):
        warn_msg = "GnuPG not configured for {}".format(platform.system())
        if any(sys.platform.startswith(e) for e in ["aix", "linux"]):
            gnupg_home = join(expanduser("~"), ".gnupg") if gnupg_home is None else gnupg_home
        elif sys.platform.startswith("darwin"):
            gnupg_home = join(expanduser("~"), ".gnupg") if gnupg_home is None else gnupg_home
        elif sys.platform.startswith("cygwin"):
            warnings.warn(warn_msg, RuntimeWarning)
        elif sys.platform.startswith("win"):
            gnupg_home = join(getenv("APPDATA"), "gnupg") if gnupg_home is None else gnupg_home
        else:
            warnings.warn(warn_msg, RuntimeWarning)
        if not exists(gnupg_home):
            return
        return gnupg.GPG(gnupghome=gnupg_home)

    @staticmethod
    def __generate_random_characters(n, seed):
        s = ""
        while n > 0:
            first_roll = random(len(seed))
            second_roll = random(len(seed[first_roll]))
            third_roll = random(len(seed[first_roll][second_roll]))
            s += seed[first_roll][second_roll][third_roll]
            n -= 1
        return s

    @staticmethod
    def __first_capital(word):
        return

    @staticmethod
    def __insert_special_chars(w, password):
        chars = ["~!#$%^", "&*()-=", "+[]\\{}",
                 ":;\"'<>", "?/0123", "456789"]
        words = password.split(" ")
        n = len(words)
        output = [e for e in words]
        w = len(words) if w > len(words) else w
        processed = set()
        while w > 0:
            n_w = random(n)
            if words[n_w] not in processed:
                processed.add(words[n_w])
                w -= 1
                ch = list(output[n_w])
                ch.insert(random(len(ch)), chars[random(6)][random(6)])
                output[n_w] = "".join(ch)
        return " ".join(output)

    @staticmethod
    def get_script_path():
        return os.path.dirname(os.path.realpath(sys.argv[0]))



def print_help():
    s = "Usage: python diceware.py [OPTIONS]\n\n" + \
        "-n, --number        number of words in the phrase, default 6" + \
        "-i, --inserts       number of words altered with special characters, default 0" + \
        "-l, --language      specified a language (en or pl), default en" + \
        "-p, --password      type of password: words (w), alphanumeric (a), or characters (c)" + \
        "-d, --delimiter     character for a delimiter, e.g. \" \"" + \
        "-c, --capitalised   words have capital letters"
    print(s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=6,
                        help="number of words/characters, which depends on the option -p")
    parser.add_argument("-i", "--inserts", type=int, default=0,
                        help="a number of words a special character is inserted to")
    parser.add_argument("-l", "--language", default="en",
                        help="Specify language (currently only en and pl is available")
    parser.add_argument("-p", "--password", default="w",
                        help="type of password: (w)words, (a)lphanumeric, or (c)characters")
    parser.add_argument("-d", "--delimiter", action="store_false",
                        help="Removes a space delimiter from a generated password")
    parser.add_argument("-c", "--capitalised", action="store_true",
                        help="Converts password to Camel Like")
    args = parser.parse_args()

    no_words = args.number
    no_changes = args.inserts
    pass_type = args.password
    lang = args.language if any(e == args.language for e in ["en", "pl"]) else "en"
    pass_type = args.password[0] if any(args.password.startswith(e) for e in ["w", "a", "c"]) else "w"
    dw = DiceWare(language=lang)
    if pass_type == "w":
        print("Password:")
        if no_changes == 0:
            print("  " + str(dw.plain(no_words, args.delimiter, args.capitalised)))
        else:
            print("  " + str(dw.complex(no_words, no_changes, args.delimiter, args.capitalised)))
    elif pass_type == "a":
        print("Password:")
        print("  " + str(dw.alphanumeric(no_words)))
    elif pass_type == "c":
        print("Password:")
        print("  " + str(dw.characters(no_words)))
    else:
        print("Error: unrecognised option for password")
    print()
