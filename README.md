Python version of the [Diceware][1] method for generating secure passwords.

**Usage**

    python diceware.py [OPTIONS]

By default, 6 words  in lower case separated by spaces are generated. The script uses the [Diceware method][1], which is considered secure but only if a password contains a _minimum_ number of words for certain applications. Please read [this website][1] and its [FAQ][2].

The script can also generate a sequence of random alphanumeric characters, which can be mixed with extra special characters, depending on the option.

Currently, only two languages are covered: `en` and `pl`.

As a side note, [Password strength test][4] is one of the tools to have a rough idea about how strong a passphrase is. While the _application is neither perfect nor foolproof_, as describer states, it still points out potential weak parts of a password.

**The files `diceware-wordlist-XX.asc`**

Both files which contain a list of words are signed by this key: [9AFEEB85ADC62CA12B99E500309F1EAF0848DCA3][3], whose content is following:

```
pub   rsa4096 2018-05-08 [C] [expires: 2022-07-26]
      9AFEEB85ADC62CA12B99E500309F1EAF0848DCA3
uid           [ultimate] Zbigniew Koziel (PhD candidate ...) <zbigniew.koziel@manchester.ac.uk>
uid           [ultimate] Zbigniew Koziel (PhD candidate ...) <zbigniew.koziel@postgrad.manchester.ac.uk>
sub   rsa4096 2018-05-08 [E] [expires: 2022-07-26]
      7D43A1193EE28688AB5AACCEAC35AEA0103F7353
sub   rsa4096 2018-05-08 [S] [expires: 2022-07-26]
      BD3A53EE9AF6BE2C6F49E6D0D10EE09E46AF2416
sub   rsa4096 2018-05-08 [A] [expires: 2022-07-26]
      E7F9724627161171CFC4B0E0796B182A63595EDB
```

The following command imports the key from a server `https://keys.openpgp.org/`:

    gpg --recv-keys 9AFEEB85ADC62CA12B99E500309F1EAF0848DCA3

It can also be downloaded using this [direct link][3] and imported. 

    gpg --import <file name>.asc

[1]: https://theworld.com/~reinhold/diceware.html
[2]: https://theworld.com/~reinhold/dicewarefaq.html
[3]: https://keys.openpgp.org/vks/v1/by-fingerprint/9AFEEB85ADC62CA12B99E500309F1EAF0848DCA3
[4]: https://www.uic.edu/apps/strong-password/