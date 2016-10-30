# Bio365-Group-Project

### Setup
All information for each html page is contained in pages.json. To generate all html,
run `pages.py`.

There is a variable to define the path used at the top of the file:
```
dev = False
if dev:
    path = '/pages/'
else:
    path = '/Bio365-Group-Project/pages/'

```

Change `dev` to be `True` for local development (to get the paths to line up). Be sure to change
it back to `False` before generating final pages for commit.
