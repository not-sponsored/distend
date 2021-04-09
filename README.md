# Distend
> generate targeted word lists for password cracking

<div align="center">
<pre>
██████╗ ██╗███████╗████████╗███████╗███╗   ██╗██████╗
██╔══██╗██║██╔════╝╚══██╔══╝██╔════╝████╗  ██║██╔══██╗
██║  ██║██║███████╗   ██║   █████╗  ██╔██╗ ██║██║  ██║
██║  ██║██║╚════██║   ██║   ██╔══╝  ██║╚██╗██║██║  ██║
██████╔╝██║███████║   ██║   ███████╗██║ ╚████║██████╔╝
╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═════╝
</pre>
</div>

The fan finally whirred to a stop as the sun peeked over the horizon. After cracking an entire night, my tired laptop had given up. Wiping the sleep from my eyes, I noted that 0 hashes were cracked. I was frustrated because I knew some details about the password behind the hash, but I could not find a simple solution that would allow me to generate a targeted word list by modifying an existing generic list with the extra details. Thus, Distend was born.

If you have a good word list, and you have some extra details surrounding the password in question such as

- Date of birth
- Mother's maiden name
- Pet names
- Age
- Address
- Other important dates
- Favorite words
- Business specific terms
- Favorite foods
- Catch phrases
- etc

then Distend is for you. It can even implement common leet speak substitutions as well!

-----
## Installation

You can install the package from PyPi using pip or directly clone the repository.

```sh
pip install distend
```

Distend is supported on Python 3.6 and above.
-----
## Usage

If installed with pip:
```sh
distend infile.txt outfile.txt
```

If cloned:
```sh
python3 distend.py infile.txt outfile.txt
```

-----
## Development setup

To run the unit tests, navigate to the test directory and run the following

```sh
python3 -m unittest test_modifier.py
python3 -m unittest test_io_utils.py
python3 -m unittest test_serializer.py
python3 -m unittest test_drive.py
python3 -m unittest test_cli.py
```
-----
## Meta
Hanwen Zuo – HanwenZuo1@gmail.com

Distend is distributed under the Apache License, Version 2.0. See ``LICENSE`` for more information.

[https://github.com/not-sponsored](https://github.com/not-sponsored)

Special thanks to [@dbader_org](https://twitter.com/dbader_org) for the readme template.

## Contributing

1. Fork it (<https://github.com/not-sponsored/distend/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Disclaimer

Please refrain from malicious use of the software.
For full details view the ``LICENSE``.
