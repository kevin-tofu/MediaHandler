# MediaHandler
 

###
```
pip install git+https://github.com/kevin-tofu/MediaHandler.git
```

###
```
handler = MediaHandler.Router(myProcessor(), MediaHandler.Config(**test_config))
```

```
class myProcessor(MediaHandler.Processor):
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

```
class myProcessor(MediaHandler.Processor):
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