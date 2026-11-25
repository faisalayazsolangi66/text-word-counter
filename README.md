# Text Word Counter

Count words, characters (with and without spaces), lines,
sentences and paragraphs in text files. Give one or more files,
or pipe text in on standard input. With several files a total row
is printed; `--json` prints the results as JSON instead of a table.

## Requirements

- Python 3 (standard library only, no extra packages)

## Usage

```bash
python3 main.py essay.txt
python3 main.py chapter1.txt chapter2.txt
echo "Hello world." | python3 main.py
python3 main.py essay.txt --json
```

## Example

```bash
$ python3 main.py essay.txt
File                             Words   Chars NoSpace  Lines  Sent.  Paras
--------------------------------------------------------------------------------
essay.txt                            9      47      38      2      3      1
```

## License

MIT — see [LICENSE](LICENSE).
