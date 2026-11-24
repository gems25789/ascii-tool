# ascii-tool
⚡ A comprehensive CLI tool for ASCII decoding, encoding, and character reference — supports decimal, hex, binary, octal, SQL CHAR(), HTML    entities, URL encoding, and more.

 # ⚡ ascii-tool

  A powerful command-line ASCII utility for decoding, encoding, and exploring characters.
  Supports standard (0–127), control (0–31, 127), and extended (128–255) ASCII with beautiful rich terminal output.

  ## Features

  - 🔍 **Decode** ASCII values from decimal, hex, binary, octal, SQL `CHAR()`, HTML entities
  - 🔒 **Encode** any string to dec, hex, bin, oct, HTML, SQL, URL formats
  - 📋 **Reference tables** — printable, control, extended ASCII
  - 🔎 **Search** characters by name, symbol, HTML entity, or code
  - 🃏 **Inspect** any character with a full detail card
  - 🎨 Beautiful colored terminal output via [rich](https://github.com/Textualize/rich)

  ## Installation

  ```bash
  pip install rich rich-argparse

  Usage

  # Decode decimal values → "hello"
  python3 ascii.py 104 101 108 108 111

  # Decode hex values
  python3 ascii.py --hex 68 65 6c 6c 6f

  # Decode SQL injection string
  python3 ascii.py --sql "CHAR(104, 101, 108, 108, 111)"

  # Encode a string to all formats
  python3 ascii.py --encode "Hello World"

  # Encode only to SQL
  python3 ascii.py --encode "admin' OR 1=1--" --to sql

  # Show printable characters table
  python3 ascii.py --printable
  python3 ascii.py -p --category digits
  python3 ascii.py -p --compact
  python3 ascii.py -p --grid

  # Search by name, symbol, or entity
  python3 ascii.py --search "quote"
  python3 ascii.py -s "!"

  # Inspect a single character
  python3 ascii.py --info 33
  python3 ascii.py --info "!"

  # Show full tables
  python3 ascii.py --table           # Standard (0-127)
  python3 ascii.py --control-table   # Control chars
  python3 ascii.py --extended-table  # Extended (128-255)

  Options

  ┌──────────────────────┬───────────────────────────────────────────────────┐
  │         Flag         │                    Description                    │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -x, --hex            │ Input is hexadecimal                              │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -b, --binary         │ Input is binary                                   │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -o, --octal          │ Input is octal                                    │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -a, --auto           │ Auto-detect format                                │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ --sql                │ Decode SQL CHAR() / 0x hex strings                │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -E, --encode TEXT    │ Encode text to all formats                        │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ --to FORMAT          │ Target format: dec, hex, bin, oct, html, sql, url │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -p, --printable      │ Show printable ASCII table                        │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -t, --table          │ Show full standard ASCII table                    │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -C, --control-table  │ Show control characters                           │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -e, --extended-table │ Show extended ASCII (128-255)                     │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -s, --search QUERY   │ Search by name/symbol/entity                      │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -i, --info CODE      │ Show detail card for a character                  │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -v, --verbose        │ Per-character breakdown                           │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -F, --full           │ Full detail card per character                    │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -f, --file FILE      │ Read values from file                             │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │ -O, --output FILE    │ Write decoded output to file                      │
  └──────────────────────┴───────────────────────────────────────────────────┘

  Requirements

  - Python 3.7+
  - rich
  - rich-argparse (optional, for colored help)
```
