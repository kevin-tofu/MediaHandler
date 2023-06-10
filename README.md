
# mediarouter  

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
handler = mediarouter.router(myprocessor(), mediarouter.config(**test_config))
```

```python
class myprocessor(mediarouter.processor):
    def __init__(self):
        super().__init__()

    async def main_file(
        self,
        process_name: str,
        fpath_org: str,
        fpath_dst: str,
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


    async def post_BytesIO_process(
        self,
        process_name :str,
        fBytesIO: io.BytesIO,
        fname_org: str,
        extension: str = 'jpg',
        **kwargs
    ):

        img_pil = Image.open(fBytesIO)
        img_np = np.asarray(img_pil)
        # print(img_np.shape) # (h, w, 3)
        
        # do stuff

        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        _, img_np = cv2.imencode(f'.{extension}', img_np)
        # print(img_np.shape) # (h*w*3)
        return Response(
            content = img_np.tostring(),
            media_type = f'image/{extension}'
        )
        
```

```python
class myprocessor(mediarouter.processor):
    def __init__(self):
        super().__init__()

    async def main_files(
        self,
        process_name: str,
        fpath_files: List[str],
        fpath_dst: str,
        **kwargs
    ):
        if process_name == "files":
            return dict(status = "OK")
        
```
