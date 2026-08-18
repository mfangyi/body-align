# BodyAlign

A Streamlit web app for yoga studio members to create before-and-after comparison photos. Supports photo upload, OpenCV-based auto-alignment, manual fine-tuning (scale/rotate/offset), touch canvas interaction, body measurement overlay, and PNG export.

## Features

- **Photo Upload** — Upload before and after practice photos (JPG/JPEG/PNG)
- **Auto Alignment** — OpenCV edge detection automatically aligns body height between two photos
- **Manual Fine-tuning** — Adjust scale, rotation, and offset for the after photo via sliders
- **Touch Canvas** — Interactive HTML5 Canvas with gesture support (single-finger drag, pinch-to-zoom, two-finger rotate)
- **Body Data Overlay** — Display body measurements (chest, waist, hip, etc.) on the comparison image
- **Labels** — Red "前" (Before) / "后" (After) labels automatically added
- **PNG Export** — Download the final comparison image as `Name_BodyPart_Date.png`

## Project Structure

```
body-align/
├── streamlit_app.py        # Main entry — Streamlit UI layout and interaction logic
├── core/
│   ├── processor.py        # Image processing: load, resize, horizontal concat, affine transform
│   ├── alignment.py        # Auto alignment: OpenCV edge detection, body height detection, scale calculation
│   ├── renderer.py         # Text rendering: Chinese font loading, label and data overlay
│   └── touch_canvas.py     # Touch canvas component: HTML5 Canvas with gesture support
├── utils/
│   └── helper.py           # Utilities: filename generation, date formatting
├── pyproject.toml          # Project config and dependencies (managed by uv)
└── README.md
```

## How to Run

Prerequisite: install [uv](https://docs.astral.sh/uv/) if you don't already have it.

```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

1. Clone the repository

   ```bash
   git clone <repo-url>
   cd body-align
   ```

2. Sync dependencies

   ```bash
   uv sync
   ```

3. Run the app

   ```bash
   uv run streamlit run streamlit_app.py
   ```

The app will be available at `http://localhost:8501`.

## Usage

1. Enter the member's name
2. Upload a **before** photo and enter body measurements (e.g., chest, waist, hip)
3. Upload an **after** photo and enter body measurements
4. Use auto-alignment or manually fine-tune the after photo with sliders
5. Interact with the canvas — drag to move, scroll/pinch to zoom, two-finger rotate
6. Click **Download PNG** to save the comparison image

## Dependencies

- **Streamlit** — Web UI framework
- **OpenCV** — Image processing and auto-alignment
- **NumPy** — Numerical operations
- **Pillow** — Image rendering and font handling
