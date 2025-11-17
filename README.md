# Algorithmic Garden AR Gallery - Setup Guide

## Overview
A data-driven AR gallery system that loads all artist information from an external JSON file, making it easy to update content without modifying any HTML code.

## Quick Start

### 1. File Structure
Place these files in your project folder:
```
your-gallery-folder/
├── index.html              (the main gallery page)
├── exhibition-data.json    (all your artist data)
└── assets/
    ├── compositions/       (scanned composition images)
    ├── renders/           (3D render images)
    └── models/            (GLB and USDZ files)
```

### 2. Edit the JSON File
Open `exhibition-data.json` and update with your data:
- Exhibition title and description
- Artist names and bios
- Image URLs and titles
- Model file paths

### 3. Test Locally
Open `index.html` in a browser to test. For AR testing, you'll need to host it online (see deployment section).

## JSON File Structure

### Basic Structure
```json
{
  "exhibition": {
    "title": "Your Exhibition Title",
    "subtitle": "Your subtitle",
    "description": "Exhibition description"
  },
  "artists": [
    {
      "name": "Artist Name",
      "bio": "Artist biography",
      "compositions": [...],
      "renders": [...],
      "model": {...}
    }
  ]
}
```

### Adding a New Artist
Add this object to the `artists` array:
```json
{
  "name": "New Artist",
  "bio": "Artist's project description",
  "compositions": [
    {
      "url": "assets/compositions/artist-comp-1.jpg",
      "title": "Composition Title 1"
    },
    {
      "url": "assets/compositions/artist-comp-2.jpg",
      "title": "Composition Title 2"
    },
    {
      "url": "assets/compositions/artist-comp-3.jpg",
      "title": "Composition Title 3"
    }
  ],
  "renders": [
    {
      "url": "assets/renders/artist-render-1.jpg",
      "title": "Render Title 1"
    },
    {
      "url": "assets/renders/artist-render-2.jpg",
      "title": "Render Title 2"
    },
    {
      "url": "assets/renders/artist-render-3.jpg",
      "title": "Render Title 3"
    }
  ],
  "model": {
    "url": "assets/models/artist-model.glb",
    "iosUrl": "assets/models/artist-model.usdz",
    "poster": "assets/models/artist-poster.jpg",
    "alt": "Description for accessibility"
  }
}
```

## Configuration Options

In `index.html`, find the CONFIG object to adjust settings:

```javascript
const CONFIG = {
    dataFile: 'exhibition-data.json',  // Path to your JSON file
    usePlaceholders: false,            // Set to true for testing with placeholder images
    debugMode: false,                   // Set to true for console debugging
    cacheTimeout: 300000               // Cache timeout in milliseconds
};
```

### Using Different JSON Files
You can have multiple JSON files for different exhibitions:
```javascript
dataFile: 'spring-2024.json'  // or 'fall-2024.json', etc.
```

### Testing with Placeholders
Set `usePlaceholders: true` to test with placeholder images before your real assets are ready.

## File Formats & Requirements

### Images
- **Format**: JPG or PNG
- **Recommended size**: 1200x1200px for gallery images
- **Compression**: Use TinyPNG or similar to optimize file sizes

### 3D Models
- **GLB files**: For web viewer and Android AR (max 10MB recommended)
- **USDZ files**: Required for iOS AR (max 10MB)
- **Poster images**: 600x400px JPG for loading preview

## Deployment

### Option 1: GitHub Pages (Free)
1. Create a GitHub repository
2. Upload all files
3. Enable GitHub Pages in Settings
4. Your gallery will be at: `https://[username].github.io/[repository-name]/`

### Option 2: Netlify (Free)
1. Zip your project folder
2. Go to netlify.com
3. Drag and drop the zip file
4. Instant deployment with custom URL

### Option 3: Your Own Server
Upload all files to your web server. Ensure:
- HTTPS is enabled (required for AR)
- Correct MIME types are set for GLB and USDZ files

## Advanced Features

### Multiple Exhibitions
Create different JSON files for different exhibitions:
```
exhibitions/
├── spring-2024.json
├── fall-2024.json
└── thesis-show.json
```

Then change the `dataFile` in CONFIG to switch exhibitions.

### External Asset Hosting
You can host images and models on CDNs:
```json
{
  "url": "https://cdn.example.com/models/artist-model.glb",
  "iosUrl": "https://cdn.example.com/models/artist-model.usdz"
}
```

### Custom Styling
The CSS is contained in the HTML file. To modify:
1. Find the `<style>` section
2. Update CSS variables in `:root` for colors
3. Modify specific classes as needed

## Troubleshooting

### JSON File Not Loading
- Check file path in CONFIG
- Ensure JSON is valid (use jsonlint.com to validate)
- Check browser console for errors
- If testing locally, some browsers block local file access

### AR Not Working on iOS
- Must use Safari browser (not Chrome)
- Need USDZ file specified in `iosUrl`
- File must be under 10MB
- Must be served over HTTPS

### Images Not Showing
- Check file paths are correct
- Ensure images are in the right folders
- Check browser console for 404 errors

### Model Not Loading
- Verify GLB file is valid
- Check file size (keep under 10MB)
- Ensure textures are embedded in GLB

## JSON Validation

Before deploying, validate your JSON:
1. Go to jsonlint.com
2. Paste your JSON content
3. Click "Validate JSON"
4. Fix any errors shown

Common JSON errors:
- Missing commas between items
- Extra comma after last item
- Unclosed quotes
- Incorrect bracket matching

## Examples

### Minimal Artist Entry
```json
{
  "name": "Student Name",
  "bio": "Project description",
  "compositions": [
    {"url": "image1.jpg", "title": "Title 1"}
  ],
  "renders": [
    {"url": "render1.jpg", "title": "Render 1"}
  ],
  "model": {
    "url": "model.glb",
    "alt": "3D model"
  }
}
```

### Full Artist Entry with All Options
```json
{
  "name": "Advanced Student",
  "bio": "Complex project with multiple iterations",
  "compositions": [
    {"url": "comp1.jpg", "title": "Initial Scan"},
    {"url": "comp2.jpg", "title": "Processed Version"},
    {"url": "comp3.jpg", "title": "Final Composite"}
  ],
  "renders": [
    {"url": "render1.jpg", "title": "Clay Render"},
    {"url": "render2.jpg", "title": "Textured Version"},
    {"url": "render3.jpg", "title": "Environmental Shot"}
  ],
  "model": {
    "url": "model.glb",
    "iosUrl": "model.usdz",
    "poster": "preview.jpg",
    "alt": "Interactive 3D sculpture with scanned textures"
  }
}
```

## Benefits of This Approach

1. **No Code Editing**: Update content by editing JSON only
2. **Version Control**: Keep different JSON files for different shows
3. **Team Friendly**: Non-programmers can update content
4. **Backup Friendly**: One JSON file contains all your data
5. **Portable**: Move between hosting providers easily
6. **Scalable**: Add unlimited artists without touching HTML

## Support

If you encounter issues:
1. Check browser console for error messages
2. Validate your JSON file
3. Test with placeholder data first
4. Ensure all file paths are correct
5. Try the CONFIG debug mode for more information

Good luck with your exhibition! 🎨