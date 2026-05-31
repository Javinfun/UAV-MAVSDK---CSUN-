# mission_builder.py

from mavsdk.mission import MissionItem, MissionPlan

from config import WAYPOINTS, ALTITUDE, SPEED


def build_mission():

    mission_items = []

    for lat, lon in WAYPOINTS:
        mission_items.append(
            MissionItem(
                lat,                               # latitude_deg
                lon,                               # longitude_deg
                ALTITUDE,                          # relative_altitude_m
                SPEED,                             # speed_m_s
                False,                              # is_fly_through
                float("nan"),                      # gimbal_pitch_deg
                float("nan"),                      # gimbal_yaw_deg
                MissionItem.CameraAction.NONE,     # camera_action
                5.0,                      # loiter_time_s
                float("nan"),                      # camera_photo_interval_s
                float("nan"),                      # acceptance_radius_m
                float("nan"),                      # yaw_deg
                float("nan"),                      # camera_photo_distance_m
                MissionItem.VehicleAction.NONE,    # vehicle_action
            )
        )

    return MissionPlan(mission_items)