import asyncio
import os

from dotenv import load_dotenv
from kasa import Discover

load_dotenv()

async def main():
  plug = await Discover.discover_single(
    os.environ["PLUG_IP"],
    username=os.environ["TAPO_USERNAME"],
    password=os.environ["TAPO_PASSWORD"],
  )
  await plug.update()
  print(f"{plug.alias} is currently {'ON' if plug.is_on else 'OFF'}")

  if plug.is_on:
    await plug.turn_off()
  else:
    await plug.turn_on()

  await plug.update()
  print(f"Now it is {'ON' if plug.is_on else 'OFF'}")
  await plug.disconnect()


asyncio.run(main())