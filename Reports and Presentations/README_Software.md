# Software Documentation

## main.py

The `main.py` script is a Python program that reads data from a serial port and saves it to a CSV file. It assumes that the data being sent over the serial port is in the format of three comma-separated values representing the voltage, current, and temperature of a solar panel system. The script creates a new CSV file with a timestamp in the filename and writes the data to it as it is received from the serial port.

The script uses the `serial` and `csv` Python modules, so make sure they are installed on your system before running the script.

To use the script, simply run it from the command line with `python main.py` or `python3 main.py` depending on your setup. By default, it will attempt to read data from a file called `/Volumes/SOLAR PANEL/LOG.CSV` since we are reading from an SD card but to read directly from the arduino you'd just have to read from serial and use `/dev/ttyUSB0`, but this can be changed by modifying the `SERIAL_PORT` variable in the script.

## arduino_v1.ino

The `arduino_v1.ino` sketch is an Arduino program that reads data from several sensors and writes it to a CSV file on an SD card. The sensors used in this sketch include a current sensor, a thermistor for temperature measurement, and a battery voltage sensor. The sketch assumes that the SD card is connected to the Arduino's SPI bus and is mounted at pin 10.

The sketch starts by initializing the serial port and checking that the SD card is properly mounted. If the SD card is not mounted, the program will enter an infinite loop and stop running. If the SD card is mounted, the program will create a new CSV file on the card with the filename `panellog.csv`.

In the main loop of the sketch, the program reads the sensor data and calculates the temperature and current values. It then writes these values to the CSV file on the SD card and prints them to the serial port if the `serialPrint` variable is set to `true`. 

Note that the sketch uses a voltage divider to measure the battery voltage, and the values of `Rbat2` and `Vopencircuit` may need to be adjusted for different battery types and configurations.

To use the sketch, upload it to an Arduino board using the Arduino IDE and connect the sensors as specified in the sketch. You will also need to insert a properly formatted SD card into the SD card slot on the Arduino board. Once the sketch is running, it will continuously read sensor data and write it to the CSV file on the SD card.
