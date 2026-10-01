import cStorage as cStor


clock = get_component("clock")
station = get_component("drone_station_lrg_1")

wh = get_component("warehouse_5")


THROTTLE = 1


self.go_to(350,0)
self.set_throttle(THROTTLE)



while self.get_distance_to(350,0) > 2:
    print(self.status())


FAILED_ROUTE_STATES = [
  "stalled_no_battery",
  "stalled_no_oil",
  "stalled_no_route",
  "scrambled",
]
print(self.undock())
print(self.set_throttle(THROTTLE))
print(self.go_to(350,0))

# while True:
#     pass

if station is None:
  print("station not found")
else:
  destination_id = station.id
  self.set_throttle(THROTTLE)
  route = self.go_to_station(destination_id)

  if route.status != "ok":
    print(route.message)
  else:
    started = clock.elapsed_game_hours()
    while self.current_station() != destination_id:
      state = self.status()
      if state in FAILED_ROUTE_STATES:
        print("route blocked:", state)
        break
      if clock.elapsed_game_hours() - started >= 24:
        print("route timed out:", state)
        break
      sleep(clock.real_seconds_per_hour() * 0.1)