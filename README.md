# Distend
> generate targeted word lists for password cracking

![](https://github.com/not-sponsored/distend/blob/main/example_usage.gif)

Perhaps you have a stubborn hash that refuses to crack under a generic word list. Maybe you have specific intelligence about the person/password in question such as a

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

Why not combine the generic word list with the extra details for a more targeted list?

Distend can do that for you. It can even implement common leet speak character replacements.

Implemented with generators, Distend is memory efficient even on large word lists, and it may be a faster alternative to brute forcing on certain hash formats.

If you think Distend is useful, please `star` the repository and share the package.

-----
## Installation

You can install the package from PyPi using pip

```sh
pip install distend
```

or you can directly clone the repository then install locally

```sh
git clone [url_from_code_button_above]
cd [your_clone_location]
pip install .
```

Distend is supported on Python 3.6 and above. There are no dependencies other than the standard library packages (included by default with your Python install).

-----
## Usage

Basic Usage

```sh
distend infile.txt outfile.txt
```

For more details and options use the help flag

```sh
distend -h
```

-----
## Development setup

To run all unit tests, navigate to the test directory and run the following

```sh
python3 -m unittest
```
or
```sh
python3 test_all.py
```

To run individual tests

```sh
python3 test_modifier.py
```

Test files are not included in the pip install, so visit the repository to get the test files.

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

Don't forget to `star` the repository if you like it.
