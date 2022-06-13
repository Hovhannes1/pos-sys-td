from rssi_data import APSample, RSSI_Database, ReferencePoint, Orientation, OrientedLocation, Location, AccessPoint


def compute_FBCM_index(distance: float, rssi_values: APSample) -> float:
    """
    Function compute_FBCM_index computes a FBCM index based on the distance (between transmitter and receiver)
    and the AP parameters. We consider the mobile device's antenna gain is 2.1 dBi.
    :param distance: the distance between AP and device
    :param rssi_values: the RSSI values associated to the AP for current calibration point. Use their average value.
    :return: one value for the FBCM index
    """
    index = 0
    # TODO: your code here
    return index


def main():
    rssi_db = RSSI_Database()
    rssi_db.import_from_file("data.csv")
    non_oriented_db = rssi_db.new_non_oriented_db()

    ap_locations = {
        "00:13:ce:8f:77:43": Location(4.13, 7.085, 0.8),
        "00:13:ce:97:78:79": Location(20.05, 28.31, 3.74),
        "00:13:ce:8f:78:d9": Location(5.74, 30.25, 2.04),
        "00:13:ce:95:de:7e": Location(4.83, 10.88, 3.78),
        "00:13:ce:95:e1:6f": Location(4.93, 25.81, 3.55)
    }

    ap_fbcm_indices: dict[str, list[float]] = {}
    for rp in non_oriented_db.reference_points:
        for sample in rp.samples:
            ap = sample.access_point
            distance = ap_locations[ap.mac_address].distance(rp.location)
            ap_fbcm_indices[ap.mac_address].append(compute_FBCM_index(distance, sample))
    # TODO: print the average FBCM index value for each access point


if __name__ == '__main__':
    main()

