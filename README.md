# Python File Organizer

The most simple file organizer ever! :p

---

## Getting Started

These instructions will help you set up the project locally for development, testing, and generating the Windows executable.

---

## Prerequisites

You need the following installed on your machine:

```
Python 3.x
```

> Make sure Python was installed with `pip` support.

---

## Environment Setup (Recommended)

Use a virtual environment to avoid installing dependencies globally.

### Create virtual environment

```
python -m venv venv
```

### Activate virtual environment

**Windows**
```
.\venv\Scripts\Activate
```

**Linux / macOS**
```
source venv/bin/activate
```

### Deactivate environment

```
deactivate
```

---

## Installing Dependencies

With the virtual environment activated, install the required libraries:

```
pip install Pillow piexif pymediainfo pyinstaller
```

### Libraries used

- **Pillow** → Image processing (EXIF)
- **piexif** → Read image metadata
- **pymediainfo** → Extract metadata from video files
- **pyinstaller** → Generate executable (.exe)

---

## Running the Script

Call the script inside a folder with files you want to organize.

### Linux, macOS, BSD and most Unix-based systems

Make the script executable:

```
chmod +x file-organizer-by-date.py
```

Run it:

```
./file-organizer-by-date.py .
```

### Windows

Run directly with Python:

```
python file-organizer-by-date.py .
```

---

## Generating Windows Executable (.exe)

With the virtual environment activated:

```
pyinstaller -w -F file-organizer-by-date.py (do not use -w if you want to display the terminal)
```

The executable will be generated inside the `dist` folder.

---

## Windows Context Menu (Optional)

To integrate with Windows Explorer:

1. Generate `file-organizer-by-date.exe`
2. Add the registry keys manually or run `file-organizer.reg`
3. Copy the `.exe` file to:

```
C:\Program Files\PythonScripts\FileOrganizer
```

4. Add this folder to the **Path** environment variable in Windows

---

## Notes

- Dependencies are bundled automatically by PyInstaller
- The virtual environment (`venv`) should **not** be committed to Git
- Dates are extracted only from formats that support metadata (e.g. JPG, JPEG, MP4)
