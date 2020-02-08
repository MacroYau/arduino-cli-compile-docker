# Arduino CLI Compile

[![https://img.shields.io/docker/pulls/macroyau/arduino-cli-compile](https://img.shields.io/docker/pulls/macroyau/arduino-cli-compile)](https://hub.docker.com/r/macroyau/arduino-cli-compile)

Dockerized [`arduino-cli`](https://github.com/arduino/arduino-cli) sketch 
compilation tool with per-project core and library dependencies support.


## Getting Started

1.  Install [Docker Engine](https://docs.docker.com/install/) on your machine.

2.  Go to your Arduino sketch folder which contains the main `.ino` file.

3.  Create `project.yaml` with the following content:

    ```yaml
    # Filename of the project's main sketch
    sketch: Blink.ino
    # Sketch version (optional; appended to filename of compiled binary file)
    version: 1.0.0

    # Compilation target
    target:
      # Arduino core name
      core: arduino:samd            # Installs the latest version; or
      # core: arduino:samd==1.6.21  # Installs v1.6.21
      # Arduino board FQBN string (obtained from `arduino-cli board list`)
      board: arduino:samd:mkrzero
      # Additional board manager URL for core installation (optional)
      url: https://arduino.esp8266.com/stable/package_esp8266com_index.json

    # Libraries to be included for compilation
    libraries:
      - Arduino Low Power           # Installs the latest version; or
      # - Arduino Low Power==1.2.1  # Installs v1.2.1
    ```

4.  Download `arduino-cli-compile` to a `PATH` directory and make it executable.

5.  Run `arduino-cli-compile path/to/sketch/folder`.

6.  The compiled binary file will appear in `dist/` inside the sketch folder.

7.  Upload the compiled binary file to your Arduino board. This part is not 
    (yet) Dockerized. For example, you can use `arduino-cli` installed on your 
    machine connecting to the board:

    ```bash
    arduino-cli upload -p /dev/ttyACM0 -b arduino:samd:mkrzero -i path/to/bin/file
    ```

8.  Watch your board blinking!
