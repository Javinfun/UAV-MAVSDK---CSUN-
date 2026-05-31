# main.py

import asyncio

from config import ALTITUDE
from drone_connection import connect_drone
from mission_builder import build_mission
from geofence import upload_geofence
from safety import (
    wait_for_gps,
    check_battery,
    wait_for_altitude,
    safe_rtl,
)


async def run():

    drone = await connect_drone()

    # Safety checks
    await wait_for_gps(drone)
    await check_battery(drone)
    await upload_geofence(drone) # Upload geofence BEFORE arming
    await drone.action.set_takeoff_altitude(ALTITUDE)

    # Upload mission
    mission = build_mission()

    print("Uploading mission...")
    await drone.mission.upload_mission(mission)

    # Arm
    print("Arming...")
    try:
        await drone.action.arm()

    except Exception as e:
        await safe_rtl(drone)
        raise e

    # Takeoff
    print("Taking off...")
    await drone.action.takeoff()
    await wait_for_altitude(drone)

    # Start mission
    print("Starting mission...")
    await drone.mission.start_mission()

    try:
        async for progress in drone.mission.mission_progress():
            print(
                f"Mission: "
                f"{progress.current}/{progress.total}"
            )

            if progress.current == progress.total:
                print("Mission complete")
                break

    except Exception as e:
        print("Mission error:", e)

        await safe_rtl(drone)
        return

    print("Returning home...")
    await drone.action.return_to_launch()

    async for in_air in drone.telemetry.in_air():
        if not in_air:
            print("Landed safely")
            break


if __name__ == "__main__":
    asyncio.run(run())