# 🎨 Image Palette Generator 

A Python desktop application that extracts beautiful color palettes from your images using **KMeans clustering**.  
The app features a modern **Tkinter GUI** with hover effects, a color slider, and a loading animation for a smooth user experience.

## Features
- Upload images in **PNG, JPG, JPEG** formats  
- Select the **number of colors** (3–10) using an interactive slider  
- Generates **color swatches** from your image
- Displays **HEX codes** under each swatch for easy use
- **Copyable color codes** for design or development projects
- **Loading animation** while processing
- Hover effects on buttons for a modern UI feel.

---

## Installation

1. Clone the repository:
    ```bash
   git clone https://github.com/yourusername/image-palette-generator.git
   cd image-palette-generator
   
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
   

---

## Usage

Run the application:
    
    python main.py

1. Click “📁 Choose Image” to upload an image.

2. Adjust the number of colors using the slider.

3. Click “✨ Generate Palette” to generate the color palette.

4. View the HEX codes below the swatches and copy as needed.

---

## Technologies Used

- Python 3
- Tkinter
- Pillow (PIL)
- OpenCV (cv2)
- scikit-learn (KMeans)
- NumPy
- Matplotlib


