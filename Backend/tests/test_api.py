import pytest
import os
from httpx import AsyncClient
from app.main import app
import io
from PIL import Image


#run cd backend pytest -q


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/healthz")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_upload_and_get_and_stats(tmp_path):
    # create a small dummy image
    img = Image.new("RGB", (64,64), color=(120,130,140))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        files = {"file": ("test.jpg", buf, "image/jpeg")}
        r = await ac.post("/upload", files=files)
        assert r.status_code == 200
        data = r.json()
        assert "id" in data
        item_id = data["id"]

        # get item
        r2 = await ac.get(f"/items/{item_id}")
        assert r2.status_code == 200
        assert r2.json()["id"] == item_id

        # stats
        r3 = await ac.get("/stats")
        assert r3.status_code == 200
        s = r3.json()
        assert s["total"] >= 1
