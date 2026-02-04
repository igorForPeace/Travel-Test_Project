import httpx

ARTIC_PLACES_BASE = "https://api.artic.edu/api/v1/places"

_cache: dict[int, bool] = {}

async def place_exists(external_place_id: int) -> bool:
    if external_place_id in _cache:
        return _cache[external_place_id]

    url = f"{ARTIC_PLACES_BASE}/{external_place_id}"
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(url)

    exists = (r.status_code == 200)
    _cache[external_place_id] = exists
    return exists