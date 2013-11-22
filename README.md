audiocalc
=========

A few audio/sound calculation utilities for Python.

Caution: I am not a sound engineer. This comes without any sort of guarantee. See file "LICENSE" for details.

If you find a bug, please post a remark in the issues section. Thanks!

## Function overview

### damping

Caclulates the damping (dissipation, absorption) in dependence of air pressure, temperature, humidity and frequency. The return value is the damping in dB/m (decibel per meter).

```python
>>> d = audiocalc.damping(temp=20, relhum=80, freq=8000)
>>> d
0.06945538
```

### total_level

Given sound pressure levels for octave frequencies, calculates the total sound pressure level.

```python
>>> octave_frequencies = {
    'f63': 71.5,
    'f125': 68.5,
    'f250': 64,
    'f500': 58,
    'f1000': 53,
    'f2000': 47,
    'f4000': 40,
    'f8000': 32}
>>> audiocalc.total_level(octave_frequencies)
73.91092323
```

### total_rated_level

Given sound pressure levels for octave frequencies, calculates the A-rated total sound pressure level.

```python
>>> octave_frequencies = {
    'f63': 71.5,
    'f125': 68.5,
    'f250': 64,
    'f500': 58,
    'f1000': 53,
    'f2000': 47,
    'f4000': 40,
    'f8000': 32}
>>> audiocalc.total_rated_level(octave_frequencies)
60.5054659
```

### distant_level

Given a reference sound pressure level (`reference_level`) in a `reference_distance`, this function calculates the sound pressure level at a certain distance.

The unit for sound level parameter and return value is dB, the unit for distances is meters.

Assumptions:

* No air damping
* The sound source is point-shaped
* energy spreads equally to all directions

```python
>>> l = audiocalc.distant_level(
        reference_level=100,
        distance=100,
        reference_distance=1)
>>> l
60.00000000000001
```

### distant_total_damped_rated_level

This combines the powers of some of the functions above. It calculates the total A-rated sound pressure level, based on a reference distance and octave sound pressure levels, given a distance, temperature and relative humidity.

```python
>>> octave_frequencies = {
    'f63': 71.5,
    'f125': 68.5,
    'f250': 64,
    'f500': 58,
    'f1000': 53,
    'f2000': 47,
    'f4000': 40,
    'f8000': 32}
>>> audiocalc.distant_total_damped_rated_level(
    octave_frequencies=octave_frequencies,
    reference_distance=300,
    distance=2000,
    temp=20, relhum=80)
40.860935587070635
```

### level_to_power

Converts logarithmic sound pressure level (dB) values to metric power (W/m²) values.

```python
>>> audiocalc.level_to_power(100)
0.01
```

## Credits

Some basic calculations have been adapted from http://www.sengpielaudio.com/
