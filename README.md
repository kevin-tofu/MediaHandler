
# MediaRouter  

## What this repository is going to solve

This library provides functions for routing media such as images and videos via FastAPI.

## How to install

### via poetry

```bash
poetry add git+https://github.com/kevin-tofu/MediaRouter.git
```

## How to test this module

```bash

poetry run python3 test/test_server.py

```

## Usage Example

```python
handler = MediaRouter.Router(myProcessor(), MediaRouter.Config(**test_config))
```

```python
class myProcessor(MediaRouter.Processor):
    def __init__(self):
        super().__init__()

    async def main_file(self, \
                  process_name: str, \
                  fpath_org: str, \
                  fpath_dst: str, \
                  **kwargs
    ):
        
        if process_name == "image":
            img = Image.open(fpath_org).convert('L')
            img.save(fpath_dst)
            return dict(status = "OK")

        elif process_name == "video":
            return dict(status = "OK")
        
        elif process_name == "zip":
            return dict(status = "OK")
        
```

```python
class myProcessor(MediaRouter.Processor):
    def __init__(self):
        super().__init__()

    async def main_files(self, \
                   process_name: str, \
                   fpath_files: List[str], \
                   fpath_dst: str, \
                   **kwargs
    ):
        if process_name == "files":
            return dict(status = "OK")
        
```
