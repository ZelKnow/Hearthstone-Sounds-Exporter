# Hearthstone Sounds Exporter
## Description

It can export Hearthstone sounds from game client.

## Requirements
```
unitypack
```

## Usage
```
usage: generate_sounds.py [-h] [--outdir [OUTDIR]] [--json-only]
                          [--cards-json-path [CARDS_JSON_PATH]] [--one-dir]
                          folder

positional arguments:
  folder

optional arguments:
  -h, --help            show this help message and exit
  --outdir [OUTDIR]
  --json-only           only write JSON cardinfo
  --cards-json-path [CARDS_JSON_PATH]
  --one-dir             output in one dir
```
`folder` is game client folder, it should be like `path\to\game\Hearthstone\Data\Win`

## Example
```
#python generate_sounds.py --outdir="D:\Game\Hearthstone\HearthstoneJSON\sounds" --cards-json-path="D:\Game\Hearthstone\HearthstoneJSON\cards.json" "D:\Game\Hearthstone\Data\Win"
```

You can download the newest `cards.json` [here](https://api.hearthstonejson.com/v1/latest/enUS/cards.json)