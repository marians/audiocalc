audiocalc
=========

A few audio/sound calculation tools for Python.

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

### total_level_rated

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
>>> audiocalc.total_level_rated(octave_frequencies)
60.5054659
```

### distant_level

Given a reference sound pressure level in a reference distance, this function calculates the sound pressure level at a certain distance.

It is assumed that the sound source is point-shaped and energy spreads in a perfect ball shape.

```python
>>> l = audiocalc.distant_level(
        reference_level=100,
        distance=100,
        reference_distance=1)
>>> l
60.00000000000001
```

## Credits

Some calculations have been adapted from http://www.sengpielaudio.com/
