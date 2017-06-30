# python_openscope_example
example code for reading from the openscope oscilloscope channel 1.

## Dependencies

### openscope script

- requests
- re
- json
- numpy
- pprint

### Dash app

All the above, plus:

- dash
- dash_core_components
- dash_html_components
- plotly
- pandas

## Test with the openscope hardware

- open waveforms live and setup the AWG
- connect the AWG to the OSC CH1 (connect solid yellow to solid orange wires)
- set OSC trigger to Run
- Adjust the URL of the openscope to match your situation (local USB connection or wifi IP address)

### openscope script

- Tested in Python 3
- Run interactively in Spyder, Pycharm, etc 
- do something with the data! Plot it, save it, etc

### Dash app

- run `python openscopedash.py`
- open the appropriate page in the browsersuch as `http://localhost:8050/`
- graph should refresh every 5 seconds
