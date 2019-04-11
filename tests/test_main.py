from vroutes import Routes


def test_main():
    locations = {
        'origin': {'lat': -6.2173207, 'lng': 106.8315268},
        'destinations': [
            {'lat': -6.1826708, 'lng': 106.8679899},  # Cempaka putih
            {'lat': -6.3627638, 'lng': 106.8270482},  # UI
            {'lat': -6.239025, 'lng': 106.990927},  # MM bekasi
            {'lat': -6.265075, 'lng': 106.782857},  # Pondok indah mall
        ]
    }
    num_vehicles = 2
    route = Routes(locations, num_vehicles)
    res = route.calculate()
    assert len(res) > 0
    for item in res:
        assert item.get('sequence', None) is not None
        assert item.get('vehicle_id', None) is not None
        assert item.get('total_distance', None) is not None
