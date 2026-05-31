# safety.py

from config import ALTITUDE


async def wait_for_gps(drone):
    print("Checking GPS health...")

    async for health in drone.telemetry.health():
        if (
            health.is_global_position_ok
            and health.is_home_position_ok
            and health.is_local_position_ok
        ):
            print("GPS + EKF OK")
            return


async def check_battery(drone):
    async for battery in drone.telemetry.battery():

        percent = battery.remaining_percent

        print(f"Battery: {percent:.1f}%")

        if percent < 30:
            raise RuntimeError("Battery too low for mission")

        return


async def wait_for_altitude(
    drone,
    target=ALTITUDE,
    tolerance=2.0,
):
    print("Waiting for takeoff altitude...")

    async for pos in drone.telemetry.position():

        if pos.relative_altitude_m is None:
            continue

        print(f"Altitude: {pos.relative_altitude_m:.1f} m")

        if abs(pos.relative_altitude_m - target) < tolerance:
            print("Target altitude reached")
            return


async def safe_rtl(drone):
    print("Initiating SAFE RTL...")

    try:
        await drone.mission.pause_mission()
    except Exception:
        pass

    await drone.action.return_to_launch()