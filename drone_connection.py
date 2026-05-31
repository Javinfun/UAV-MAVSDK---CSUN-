# drone_connection.py

from mavsdk import System
from config import SYSTEM_ADDRESS


async def connect_drone():

    drone = System()

    print("Connecting...")
    await drone.connect(system_address=SYSTEM_ADDRESS)

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected")
            break

    return drone