# PTT Image Search Application  

A PyQt-based desktop application that allows users to search and download images from PTT (Taiwan's largest bulletin board system) boards.  

## Features  

- Input any PTT board URL for image searching  
- Search images by keywords  
- Specify the number of images to download  
- Preview downloaded images in the application  
- Navigate through downloaded images using Previous/Next buttons  
- Images are automatically saved to a local folder named after the search keyword  

## Technical Stack  

- **Python** - Core programming language  
- **PyQt5** - GUI framework  
  - QtWidgets: UI components  
  - QtGui: Image handling  
  - QtCore: Core functionality  
- **OpenCV (cv2)** - Image processing and resizing  
- **Requests** - HTTP requests handling  
- **BeautifulSoup4** - HTML parsing  
- **Regular Expressions** - URL pattern matching  

## Project Structure  

- `pttBeauty_start.py` - Application entry point  
- `pttBeauty_controller.py` - Main controller containing business logic  
- `pttBeauty_UI.py` - UI definition generated from Qt Designer  

## Key Components  

### Image Processing  
- Uses OpenCV for image loading and resizing  
- Supports JPG, JPEG, and PNG formats  
- Auto-resizes images to fit the preview window  

### Web Scraping  
- Handles PTT's age verification system  
- Extracts image URLs using BeautifulSoup4  
- Implements regex filtering to exclude certain image hosts  
- Downloads images asynchronously  

### User Interface  
- Clean and intuitive interface with:  
  - URL input field  
  - Keyword search field  
  - Image quantity selector  
  - Image preview area  
  - Navigation buttons  
  - Status indicators  

## Installation Requirements  

```bash  
pip install PyQt5  
pip install requests  
pip install beautifulsoup4  
pip install opencv-python  
```

## Usage  

- Run the application:  

```bash  
python pttBeauty_start.py
```

- Enter the PTT board URL (e.g., https://www.ptt.cc/bbs/Beauty/index.html)  
- Enter your search keyword  
- Specify the number of images to download  
- Click the Search button  
- Use Previous/Next buttons to navigate through downloaded images  

### Notes  
- The application automatically handles PTT's age verification  
- Images are saved in a folder named after your search keyword  
- Supports multiple image formats but excludes GIF files  
- Implements rate limiting and error handling for reliable downloading  
