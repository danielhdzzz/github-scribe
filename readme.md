# 🪶 Github Scribe

Prints out a small image into the contributions graph of a GitHub profile.

## Usage

```bash
python3 main.py --image <path> --start-date <YYYY-MM-DD> [options]
```

### Required Arguments

| Argument       | Short | Description                                        |
| -------------- | ----- | -------------------------------------------------- |
| `--image`      | `-i`  | Path to source image (7px tall, black/white only)  |
| `--start-date` | `-s`  | Start date in YYYY-MM-DD format (must be a Sunday) |

### Optional Arguments

| Argument              | Short | Default | Description                    |
| --------------------- | ----- | ------- | ------------------------------ |
| `--commits-per-pixel` | `-c`  | 220     | Commits per dark pixel         |
| `--commits-per-blank` | `-b`  | 0       | Commits per blank pixel        |
| `--dry-run`           | `-n`  | false   | Preview without making commits |

### Examples

Dry run to preview:

```bash
python3 main.py --image ./messages/hello.png --start-date 2025-08-17 --dry-run
```

Run with custom commit intensity:

```bash
python3 main.py -i ./messages/hello.png -s 2025-08-17 -c 150
```

### Notes

- The source image should be exactly 7 pixels in height (one row per day of the week)
- The image should only contain black or white pixels
- The start date must be a Sunday (first row of the contributions graph)
- Accounts with many existing commits may need a higher `--commits-per-pixel` value for the image to be visible
- Before running, an ASCII preview of the image and settings summary will be displayed
- You will be prompted to confirm before commits are made

## Demo

https://github.com/danielhdzzz/github-scribe/assets/16919739/2541a502-e655-4b49-b5a0-11d6ce032bbc
