# 🪶 Github Scribe

Prints out a small image into the contributions graph of a github profile.

### Settings

| Prop        | Type                 |
| ----------- | -------------------- |
| `commits_per_pixel`| `integer`      |
| `commits_per_blank_pixel`| `integer`|
| `deploy`    | `boolean`            |
| `source_img`| `string`             |
| `start_date`: `y`, `m`, `d`| `integer`|

#### commits_per_pixel
Determines how many commits will be made per "pixel". Accounts with a large number of commits will have to set a high value in order to display a clear image.

#### commits_per_blank_pixel
Determines how many commits will be made per blank "pixel". This should typically be set to 0, unless you want a light green backdrop in the contributions graph.

#### source_img
Path to the image that will be printed. It should only contain either black or white pixels and should be exactly 7 pixels in height.

#### start_date
The `start_date` in which the message will be printed. It has to be a sunday, since it is the first row of the contributions graph.

#### deploy
Set `deploy` to true to enable commiting and pushing to your github repo. I recommend running it once with this option disabled, to check that it runs without any errors.

---

### Run the script

```bash
python3 main.py
```

### Demo

https://github.com/danielhdzzz/github-scribe/assets/16919739/2541a502-e655-4b49-b5a0-11d6ce032bbc
