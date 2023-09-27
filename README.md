# Python File Organizer

The most simple file organizer ever! :p

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

```
Python 3.x
```

### Installing

A step by step series of examples that tell you how to get a development env running

Install Python 3.x with pip

Install PyInstaller, to generate .exe file (for Windows)

```
pip install pyinstaller
```


## Running the tests

### Linux, Mac OS X, BSD and most OSes except Windows
Turn script executable:

```
chmod +x file-organizer.py
```

Call script inside a folder with files:

```
./file-organizer.py .
```

### Windows

To run a test, call the script inside a folder with files.

```
python file-organizer.py .
```

**For Windows in Context Menu:**

1. To generate *file-organizer.exe* file to run on Windows.

```
pyinstaller -w -F file-organizer.py
```

2. Add the keys on Registry or run *file-organizer.reg*.
3. Copy .exe file on *C:\Program Files\Python Scripts\File Organizer*
4. Add *C:\Program Files\Python Scripts\File Organizer* in the *Path* on Windows Environment Variable.