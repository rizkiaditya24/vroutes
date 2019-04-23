VRoutes
=======

A simple implementation of Vehicle Routing Problem based on Google OR-Tools.

To find the best routes, we need to calculate the distances on every possible routes, there are several methods to do that,
but currently it only supports Haversine


Installation
------------

::

  $ virtualenv venv --python=python3
  $ source venv/bin/active
  $ (venv) pip install git+https://github.com/rizkiaditya24/vroutes


Example
-------

.. code-block:: python

  from vroutes import Routes

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
  print(res)
