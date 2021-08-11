Python version of the [Diceware][1] method for generating secure passwords.

Usage:

    python diceware.py [OPTIONS]

By default, 6 words  in lower case separated by spaces are generated. The script uses the [Diceware method][1], which is considered secure but only if a password contains a _minimum_ number of words for certain applications. Please read [this website][1] and its [FAQ][2].

The script can also generate a sequence of random alphanumeric characters, which can be mixed with extra special characters, depending on the option.

Currently, only two languages are covered: `en` and `pl`. 

[1]: https://theworld.com/~reinhold/diceware.html
[2]: https://theworld.com/~reinhold/dicewarefaq.html