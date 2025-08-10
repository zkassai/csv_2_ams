import csv
import json
import os

def read_csv_to_dict_list(file_path, delimiter=';'):
    data = []
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=delimiter)
            header = [h.strip() for h in next(reader)]
            for row in reader:
                if not row or not any(row):
                    continue
                row_data = {h: v for h, v in zip(header, row)}
                data.append(row_data)
    except FileNotFoundError:
        print(f"Warning: File not found at {file_path}")
    return data

def read_channels(input_dir):
    channels = {}
    with open(f"{input_dir}/Channels.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        header = [h.strip() for h in next(reader)]
        for row in reader:
            if not row or not any(row):
                continue
            channel_data = dict(zip(header, row))
            if "ServiceId" in channel_data and channel_data["ServiceId"]:
                channels[channel_data["ServiceId"]] = channel_data
    return channels

def read_service_genres(input_dir):
    # This one has a special structure, so I'll keep its custom function for now.
    service_genres = {"serviceGenre": [], "replayGenre": [], "genre": []}
    with open(f"{input_dir}/ServiceGenre.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # Skip header
        for row in reader:
            if not row:
                continue
            genre_type = row[0]
            if genre_type == "service":
                service_genres["serviceGenre"].append(
                    {
                        "id": row[1],
                        "name": row[2],
                        "applications": [],
                        "default": "false",
                        "order": int(row[3]),
                    }
                )
            elif genre_type == "replay":
                service_genres["replayGenre"].append(
                    {
                        "id": row[1],
                        "name": row[2],
                        "order": int(row[3]),
                    }
                )
            elif genre_type == "mapping":
                genre = {
                        "id": row[1],
                        "name": row[2],
                        "order": int(row[3]),
                    }
                if len(row) > 4 and row[4]:
                    genre["parentId"] = row[4]
                if len(row) > 5 and row[5]:
                    genre["replayGenreId"] = row[5]
                service_genres["genre"].append(genre)
    return service_genres

def read_channel_lineup(input_dir):
    lineups_data = read_csv_to_dict_list(f"{input_dir}/Channel Lineup.csv")
    lineups = {}
    for row in lineups_data:
        lineup_id = row.get("LineupID")
        if lineup_id:
            if lineup_id not in lineups:
                lineups[lineup_id] = {
                    "id": lineup_id,
                    "name": row.get("LineupName"),
                    "channels": [],
                }
            lineups[lineup_id]["channels"].append(
                {"serviceId": row.get("ServiceID"), "channelNumber": int(row.get("ChannelNumber"))}
            )
    return list(lineups.values())

def read_qam_locations(input_dir):
    data = read_csv_to_dict_list(f"{input_dir}/QAM Channel Location.csv")
    locations = {}
    for row in data:
        service_id = row.get("ServiceId")
        if service_id:
            if service_id not in locations:
                locations[service_id] = []
            locations[service_id].append(row)
    return locations

def read_ott_locations(input_dir):
    data = read_csv_to_dict_list(f"{input_dir}/ottlocation.csv")
    locations = {}
    for row in data:
        service_id = row.get("ServiceId")
        if service_id:
            if service_id not in locations:
                locations[service_id] = []
            locations[service_id].append(row)
    return locations

def read_linear_products(input_dir):
    # This file has two header lines, so a custom reader is needed
    products = []
    with open(f"{input_dir}/Linear Products.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # Skip header
        next(reader) # skip another header
        for row in reader:
            if row:
                products.append({"id": row[0], "edsId": row[1]})
    return products

def read_replay_products(input_dir):
    # This file has two header lines, so a custom reader is needed
    products = []
    with open(f"{input_dir}/Replay Products.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # Skip header
        next(reader) # skip another header
        for row in reader:
            if row:
                products.append({"id": row[0], "edsId": row[1]})
    return products

def read_apps(input_dir):
    apps = {}
    with open(f"{input_dir}/Apps.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        for row in reader:
            if not row or len(row) < 3:
                continue
            channel_id = row[0]
            if channel_id not in apps:
                apps[channel_id] = {}

            apps[channel_id][row[1]] = row[2]
    return apps

def read_providers(input_dir):
    return read_csv_to_dict_list(f"{input_dir}/providers.csv")

def read_avad(input_dir):
    avad = {}
    with open(f"{input_dir}/AVAD.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        for row in reader:
            if not row or len(row) < 3:
                continue
            service_id = row[0]
            if service_id not in avad:
                avad[service_id] = {}

            avad[service_id][row[1]] = row[2]
    return avad

def read_tstv(input_dir):
    tstv = {}
    with open(f"{input_dir}/TSTV.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        for row in reader:
            if not row or len(row) < 3:
                continue
            service_id = row[0]
            if service_id not in tstv:
                tstv[service_id] = {}

            tstv[service_id][row[1]] = row[2]
    return tstv

def read_trickplaycontrol(input_dir):
    trickplay = {}
    with open(f"{input_dir}/Trickplaycontrol.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        for row in reader:
            if not row or len(row) < 3:
                continue
            service_id = row[0]
            if service_id not in trickplay:
                trickplay[service_id] = {}

            trickplay[service_id][row[1]] = row[2]
    return trickplay

def read_city_mapping(input_dir):
    city_mapping = {}
    with open(f"{input_dir}/EDS City Mapping.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader) # skip header
        for row in reader:
            if len(row) >= 2:
                city_mapping[row[0]] = row[1]
    return city_mapping

def generate_json(input_dir, output_file):
    channels_data = read_channels(input_dir)
    service_genres_data = read_service_genres(input_dir)
    lineups_data = read_channel_lineup(input_dir)
    qam_locations_data = read_qam_locations(input_dir)
    ott_locations_data = read_ott_locations(input_dir)
    linear_products_data = read_linear_products(input_dir)
    replay_products_data = read_replay_products(input_dir)
    apps_data = read_apps(input_dir)
    providers_data = read_providers(input_dir)
    avad_data = read_avad(input_dir)
    tstv_data = read_tstv(input_dir)
    trickplaycontrol_data = read_trickplaycontrol(input_dir)
    city_mapping_data = read_city_mapping(input_dir)

    all_locations = []

    final_json = {
        "diagnostics": {
            "source": "IE_STARHUB",
            "generationDate": "2025-08-01T09:00:00.000Z"
        },
        "classifications": service_genres_data,
        "recommendationTopics": [],
        "deployment": {
            "id": "IE_STARHUB",
            "deploymentDate": "2025-08-01T09:00:00.000Z"
        },
        "cityIdMapping": city_mapping_data,
        "productizing": {
            "linear": linear_products_data,
            "replay": replay_products_data
        },
        "channels": [],
        "lineups": lineups_data,
        "locations": all_locations,
        "relatedMaterials": [],
        "applications": [],
        "providers": providers_data
    }

    # Populate channels
    for channel_id, channel_info in channels_data.items():
        # Locations
        locations = []
        if channel_id in qam_locations_data:
            for loc in qam_locations_data[channel_id]:
                location = {
                    "type": "qam",
                    "frequency": int(loc["Frequency"]) if loc.get("Frequency") else None,
                    "symbolRate": int(loc["SymbolRate"]) if loc.get("SymbolRate") else None,
                    "modulation": int(loc["Modulation"]) if loc.get("Modulation") else None,
                    "fecInner": int(loc["FecInner"]) if loc.get("FecInner") else None,
                    "fecOuter": int(loc["FecOuter"]) if loc.get("FecOuter") else None,
                    "programNumber": int(loc["ProgramNbr"]) if loc.get("ProgramNbr") else None,
                    "ipLocationUrl": loc.get("IPLocationURL"),
                    "cpeType": loc.get("CpeType"),
                    "drmProtectionKey": loc.get("DRMProtectionKey"),
                    "streamingProtocol": loc.get("StreamingProtocol")
                }
                locations.append(location)
                all_locations.append(location)

        if channel_id in ott_locations_data:
             for loc in ott_locations_data[channel_id]:
                location = {
                    "type": "ott",
                    "url": loc.get("Url"),
                    "cpeType": loc.get("CpeType"),
                    "drmProtectionKey": loc.get("DRMProtectionKey"),
                    "streamingProtocol": loc.get("StreamingProtocol")
                }
                locations.append(location)
                all_locations.append(location)

        # Applications
        applications = []
        if channel_id in apps_data:
            app_info = apps_data[channel_id]
            app = {
                "id": app_info.get("deeplink"),
                "trigger": app_info.get("trigger"),
                "delay": int(app_info.get("delay", 0)),
                "displayTime": int(app_info.get("displaytime", 0)),
                "repeat": int(app_info.get("repeat", 0)),
                "channelBound": app_info.get("channelbound").split(",") if app_info.get("channelbound") else [],
                "logo": app_info.get("applogo"),
                "poster": app_info.get("posterlogo"),
                "synopsis": {
                    "en-IE": app_info.get("synopsis.en-IE")
                } if app_info.get("synopsis.en-IE") else None,
                "toasterMessage": {
                    "en-IE": app_info.get("toastermessage.en-IE")
                } if app_info.get("toastermessage.en-IE") else None,
            }
            applications.append(app)

        # AVAD
        avad = avad_data.get(channel_id, {})

        # TSTV
        tstv = tstv_data.get(channel_id, {})

        # Trickplay
        trickplay = trickplaycontrol_data.get(channel_id, {})

        final_json["channels"].append({
            "id": channel_id,
            "title": channel_info.get("Name"),
            "description": channel_info.get("Description"),
            "longDescription": channel_info.get("LongDescription"),
            "type": channel_info.get("Type"),
            "serviceGenreIds": channel_info.get("ServiceGenre", "").split(",") if channel_info.get("ServiceGenre") else [],
            "replayable": channel_info.get("Replayable", "false").lower() == "true",
            "startOver": channel_info.get("StartOver", "false").lower() == "true",
            "catchUp": channel_info.get("CatchUp", "false").lower() == "true",
            "ottFollow": channel_info.get("OTTFollow", "false").lower() == "true",
            "casId": channel_info.get("CasId"),
            "providerId": channel_info.get("ProviderId"),
            "logo": channel_info.get("FocusedLogo"),
            "poster": channel_info.get("Poster"),
            "locations": locations,
            "applications": applications,
            "avad": avad,
            "tstv": tstv,
            "trickplay": trickplay
        })

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, "w") as f:
        json.dump(final_json, f, indent=4)

if __name__ == "__main__":
    generate_json("input_csv", "output/output.json")
