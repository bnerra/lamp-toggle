import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from kasa import Discover

load_dotenv()

BASE_DIR = Path(__file__).parent

app = FastAPI()

async def get_plug():
  plug = await Discover.discover_single(
    os.environ["PLUG_IP"],
    username=os.environ["TAPO_USERNAME"],
    password=os.environ["TAPO_PASSWORD"],
  )
  await plug.update()
  return plug


@app.get("/")
async def index():
  return FileResponse(BASE_DIR / "index.html")


@app.get("/state")
async def state():
  plug = await get_plug()
  is_on = plug.is_on
  await plug.disconnect()
  return {"on": is_on}


@app.post("/toggle")
async def toggle():
  plug = await get_plug()
  if plug.is_on:
    await plug.turn_off()
  else:
    await plug.turn_on()
  await plug.update()
  is_on = plug.is_on
  await plug.disconnect()
  return {"on": is_on}


