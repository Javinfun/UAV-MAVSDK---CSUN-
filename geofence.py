# geofence.py

from mavsdk.geofence import (
    Point,
    Polygon,
    GeofenceData,
    FenceType,
)

from config import GEOFENCE_POINTS, GEOFENCE_ACTION


def build_polygon():

    points = [
        Point(lat, lon)
        for lat, lon in GEOFENCE_POINTS
    ]

    return Polygon(points, GEOFENCE_ACTION)


async def upload_geofence(drone):

    print("Uploading geofence...")

    print("Fence points:")
    for i, point in enumerate(GEOFENCE_POINTS):
        print(f"  {i}: {point}")

    polygon = build_polygon()

    geofence_data = GeofenceData(
        [polygon],  # polygon fences
        []           # circle fences (EMPTY but required)
    )

    await drone.geofence.upload_geofence(geofence_data)

    print("Geofence uploaded")