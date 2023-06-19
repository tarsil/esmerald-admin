from esmerald import JSON, get


@get("/welcome")
async def welcome() -> JSON:
    return JSON({"detail": "Welcome to myproject"})
