# 🪶 Github Scribe

Prints out a small image into the contributions graph of a github profile.

### Settings and running the script

Set the `start_date` in which the message will be printed. Link a black and white `source_img` of 7 pixels in height. Set `commits_per_pixel` to determine how many commits will be made per "pixel". Accounts with a large number of commits will have to use a high `commits_per_pixel` value in order to display a clear image. Set `deploy` to true to enable commiting and pushing to your github repo.

```python
settings = {
  "commits_per_pixel": 400,
  "commits_per_blank_pixel": 0,
  "deploy": False,
  "source_img": './messages/message2.png',
  "start_date": {
    "y": 2023,
    "m": 4,
    "d": 2
  }
}
```

Run the script

```bash
python3 main.py
```

### Demo

https://github.com/danielhdzzz/github-scribe/assets/16919739/2541a502-e655-4b49-b5a0-11d6ce032bbc
