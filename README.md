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

Do you have a good word list? Perhaps you also have specific intel about the password in question such as

- Date of birth
- Mother's maiden name
- Pet names
- Age
- Address
- Other important dates
- Business specific terms
- Favorite foods
- Catch phrases
- Etc

Why not combine the word list with the extra details?

If you agree, then Distend is for you. It can even implement common leet speak replacements.

-----
## Installation

You can install the package from PyPi using pip

```sh
pip install distend
```

or you can directly clone the repository then run the setup

```sh
cd [your_clone_location]
pip install .
```

Distend is supported on Python 3.6 and above. Also, there are no dependencies
other than a few standard library packages (included by default with your python install).

-----
## Usage

Basic Usage

```sh
distend infile.txt outfile.txt
```

For more details use the help flag

```sh
distend -h
```

-----
## Development setup

To run the unit tests, navigate to the test directory and run the following

```sh
python3 -m unittest test_modifier.py
python3 -m unittest test_io_utils.py
python3 -m unittest test_serializer.py
python3 -m unittest test_cli.py
```

You may have to visit the repository to get the test files because they are not included with the pip install.
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
