from fastapi import FastAPI

from fastapi_cache import FastAPICache, default_key_builder, JsonCoder

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    cache_instance = FastAPICache.get_backend()
    cache_key = default_key_builder(prefix='cache_say_hello', func=say_hello, parameter={'name': name})
    cache_value = cache_instance.get(cache_key)

    if cache_value is None:
        res = {"message": f"Hello {name}"}
        cache_instance.set(cache_key, JsonCoder.encode(res), expire=60 * 60)
        return {"value": res}
    else:
        return JsonCoder.decode(cache_value)
