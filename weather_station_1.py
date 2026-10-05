notebook = get_component("notebook")
comms = get_component("comms")

weather_stations_id = [
    "weather_station_1",   
    "weather_station_2",   
    "weather_station_3",   
    "weather_station_4",   
    "weather_station_5",   
]

def observe():
    if self.last_report().age_gh() > 1:
        self.observe()

self.signal_board.clear()



def update_notebook():
    if self.id == "weather_station_1":      
        transmissions = get_transmissions()
        accepted_transmissions = filter_transmissions(transmissions)

        # for accepted_transmission,filtered_signals in accepted_transmissions.items():
        #     print(accepted_transmission)
        #     for packet,signal in filtered_signals.items():
        #         print("\t",packet,signal.data)


        write = dict(zip(accepted_transmissions.keys(),""))

        if write:
            print(write)
    pass

def get_transmissions()->list[SignalTransmission]:

    return [
        transmission
        for weather_station_id in weather_stations_id
        for transmission in get_component(weather_station_id).signal_receiver.transmissions()
    ]

def storm_crystal_broadcast(transmission:SignalTransmission):  
    pass


def filter_transmissions(transmissions:list[SignalTransmission])->dict[str,dict[int,SignalTransmission]]:
    filtered_transmissions:list[SignalTransmission]
    accepted_transmissions={}
    if transmissions:
        events_id = list(
            set(
            transmission.event_id
            for transmission in transmissions
            )
        )
        if events_id.length != 1:
            print(events_id)
        for event_id in events_id:
            if (
                event_id != self.signal_board.status().event_id
                and not event_id.startswith("storm_dust_")
            ):
                accepted_transmissions = {}
                for transmission in transmissions:
                    checksum = sum(
                        ord(
                            str(
                                char
                            )
                        ) for char in transmission.data)
                    if checksum == transmission.checksum:                    
                        data = transmission.data.split("|")
                        event = accepted_transmissions.setdefault(transmission.event_id, {})
                        event[int(data[1])] = transmission
                    else:
                        self.signal_board.reject(transmission)
               
    sleep(1)

    return accepted_transmissions




while True:
    self.observe()
    
    transmissions = get_transmissions()
    update_notebook()
    accepted_transmissions:dict
    
    if transmissions:
        events_ids = list(
            set(
            transmission.event_id
            for transmission in transmissions
            )
        )
        if events_ids.length != 1:
            print(events_ids)

        for events_id in events_ids:
            if (
                events_id != self.signal_board.status().event_id
                and events_id.startswith("storm_dust_")
            ):
                self.signal_board.clear()
                accepted_transmissions = {}
                for transmission in transmissions:
                    checksum = sum(
                        ord(
                            str(
                                char
                            )
                        ) for char in transmission.data)
                    if checksum == transmission.checksum:
                        self.signal_board.reveal(transmission).status
                    
                        data = transmission.data.split("|")
                        event = accepted_transmissions.setdefault(transmission.event_id, {})
                        event[int(data[1])] = transmission
                    else:

                        self.signal_board.reject(transmission)
            
    sleep(1)

self.signal_board.status()















    