# Screen Capture and Change Detection

This application allows you to continuously monitor a selected area of your screen and automatically saves a screenshot whenever a change is detected in that area.

## Features

*   **Selectable Capture Area:** Use your mouse to select any rectangular area on your screen.
*   **Change Detection:** The application continuously monitors the selected area and only saves a screenshot when the content changes. This is done by comparing perceptual hashes of the images.
*   **Continuous Capture:** The application runs in a loop, capturing and comparing images at a set interval.
*   **Timestamped Filenames:** Screenshots are saved with a timestamp in the filename, making it easy to track changes over time.

## Proposed Architecture

The current implementation is a single Python script. To enhance usability and robustness, a more advanced architecture is proposed, separating the user interface from the core capture logic.

### Frontend (Client)

A graphical user interface (GUI) that allows the user to:
*   Start and stop the capture process.
*   Select and manage one or more capture areas.
*   Configure settings, such as the capture interval and output directory.
*   View a gallery of captured screenshots.
*   Receive notifications when a change is detected.

The frontend could be developed using a modern GUI framework like PyQt, PySide, or a web-based technology like Electron.

### Backend (Server)

A background process (or service) that handles the core functionality:
*   Manages the screen capture loop.
*   Performs image hashing and comparison for change detection.
*   Saves images to the filesystem.
*   Exposes a simple API (e.g., a local REST API with Flask/FastAPI) that the frontend can use to control the backend and retrieve information.

This client-server architecture ensures that the core capture functionality can run independently of the UI, making the application more stable and scalable.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Install the dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Usage

To run the application, execute the `main.py` script from your terminal and provide the path to an output folder where you want to save the screenshots.

```bash
python main.py /path/to/your/output/folder
```

When you run the command, a translucent overlay will appear on your screen. Click and drag your mouse to select the area you want to monitor. Once you release the mouse button, the application will start monitoring that area for changes.

To stop the application, press `Ctrl+C` in the terminal.
