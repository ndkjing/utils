"""Coordinate transformations."""
import numpy as np
from . import earth


def lla_to_ecef(lat, lon, alt=0):
    """Convert latitude, longitude, altitude to ECEF Cartesian coordinates.

    Parameters
    ----------
    lat, lon : array_like
        Latitude and longitude.
    alt : array_like, optional
        Altitude. Default is 0.

    Returns
    -------
    r_e : ndarray, shape (3,) or (n, 3)
        Cartesian coordinates in ECEF frame.
    """
    lat = np.asarray(lat)

    sin_lat = np.sin(np.deg2rad(lat))
    cos_lat = np.cos(np.deg2rad(lat))
    sin_lon = np.sin(np.deg2rad(lon))
    cos_lon = np.cos(np.deg2rad(lon))

    re, _ = earth.principal_radii(lat)
    r_e = np.empty((3,) + lat.shape)
    r_e[0] = (re + alt) * cos_lat * cos_lon
    r_e[1] = (re + alt) * cos_lat * sin_lon
    r_e[2] = ((1 - earth.E2) * re + alt) * sin_lat
    r_e = r_e.T

    return r_e


def perturb_ll(lat, lon, d_lat, d_lon):
    """Perturb latitude and longitude.

    This function recomputes linear displacements in meters to changes in a
    latitude and longitude considering Earth curvature.

    Note that this computation is approximate in nature and makes a good
    sense only if displacements are significantly less than Earth radius.

    Parameters
    ----------
    lat, lon : array_like
        Latitude and longitude.
    d_lat, d_lon : array_like
        Perturbations to `lat` and `lon` respectively in *meters*. It is
        assumed that `d_lat` and `d_lon` are significantly less than Earth
        radius.

    Returns
    -------
    lat_new, lon_new
        Perturbed values of latitude and longitude.
    """
    slat = np.sin(np.deg2rad(lat))
    clat = (1 - slat**2) ** 0.5
    re, rn = earth.principal_radii(lat)

    lat_new = lat + np.rad2deg(d_lat / rn)
    lon_new = lon + np.rad2deg(d_lon / (re * clat))

    return lat_new, lon_new
