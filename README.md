# Tetra Editor

Modular code editor with graphical user interface. In the editor you can create, save and switch between files using tabbar. There's also syntax highlighting and turnable statusbar displaying information about current opened file. There're 6 modules out-of-the box, 3 of which are customizable.

Main editor features:
- Creation, saving and switching between files.
- Syntax highlighting, line numbers, current line highlighting
- Theme choosing and editor appearance customization
- Configuration of the shown statusbar blocks
- Exporting and importing editor settings
- Enabling, disabling and configuring different program components

## Running

### Via nix package manager

Whichever Linux distribution you have, if you have nix package manager installed, you may run tetra with this command:

``` sh
nix --extra-experimental-features "nix-command flakes" run github:markmelix/tetra
```

Or add it as an input to your flake.nix and then throw it to the Home Manager package list to have it permanently installed on your system.

If you'd like to contribute to the tetra, clone the repository and run `nix develop`. Then make your changes having all development dependencies provided by the flakes environment. 

### Other Linux distributions

Download binary from the [releases](https://github.com/markmelix/tetra/releases) page.

Otherwise, if you have Python installed, clone the repository and build tetra with `./build.sh` command. Then you'll have the binary located at `./target/linux/dist` directory.

If you'd like to contribute, create Python environment whichever way you like and install dependecies listed in `requirements.txt`. Then make your changes.

## Implementation

Now there're about 30 classes in the project. Every class's being used for implementation of a specific function.

### Description of the main classes

1. `Core`: editor core which controls all the editor processes. Every module has access to that class
2. `Event`: enumeration where all the possible events are specified
3. `Module`: determines every module as a set of the common methods giving an ability to interact with it through the common interface
4. `Buffer`: an abstract text buffer. The user can communicate with it using GuiBuffer
5. `BufferManager`: abstract buffer management-storage
6. `GuiBuffer`: a graphical text editing buffer. The user types text here
7. `Setting`: a common presenter of every module setting
8. `Settings`: independent widget through which the user can control module settings

### Event system

Whenever there's something to happen in the editor (e. g. a file gets opened), just after that a new event is going to be appended to the special list (`Core.events`) and all editor refresh methods (`Module.refresh`) get triggered. The system linking all these processes is an Event-system. The Event-system isn't represented as a separate class, but instead it's injected right into the editor core and one can interact with it through special Core methods.

To raise a new event and notify all the modules about that `Core.raise_event(event)` method's used, where event is one of the `Event` enumeration variants. Also there's a convenient decorator `Event.apply_event` which wraps the needed `Core` method so that after one gets called the applied events gets raised.

### Project stack

The project is written on the Python completely with the use of PyQt5 GUI library.

Used libraries:
- PyQt5: Qt wrapper for GUI programs creation
- QScintilla: Scintilla wrapper for functional text editing buffer creation
- charset-normalizer: library used to determine opened file encoding

## Project author

Mark Meliksetyan <markmelix@gmail.com>

## License

[MIT](License)
