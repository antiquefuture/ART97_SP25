# iOS AR Setup Guide - Converting GLB to USDZ

## The iOS AR Issue Explained

iOS Safari requires **USDZ format** for AR Quick Look, not GLB. This is why the "View in AR" button wasn't working - iOS can display GLB files in 3D but cannot use them for AR placement.

## Quick Solution: Model Conversion

### Option 1: Reality Converter (Mac Only - EASIEST)
1. Download **Reality Converter** from Apple (free)
   - Available on Mac App Store
   - Or download from: https://developer.apple.com/augmented-reality/tools/

2. Open Reality Converter
3. Drag your `.glb` file into the app
4. Click "File" → "Export"
5. Choose USDZ format
6. Save the file

### Option 2: Online Converters (Any Platform)
Several online tools can convert GLB to USDZ:

1. **Vectary** (https://www.vectary.com/3d-modeling-news/how-to-convert-gltf-glb-to-usdz/)
   - Upload GLB
   - Export as USDZ
   - Free with limitations

2. **Model Viewer Editor** (https://modelviewer.dev/editor/)
   - Load your GLB
   - Export → Download USDZ
   - Completely free

3. **Sketchfab** (if you have an account)
   - Upload GLB model
   - Download as USDZ

### Option 3: Command Line Tools (Advanced)
If you have USD tools installed:
```bash
# Install usdz tools (Mac with Homebrew)
brew install usd

# Convert GLB to USDZ
usdconv input.glb output.usdz
```

## Implementation in Your Gallery

### Update Your Student Data Structure:

```javascript
const studentsData = {
    "Alex Chen": {
        bio: "Artist bio...",
        compositions: [...],
        renders: [...],
        model: {
            url: "assets/models/alex-chen.glb",        // For web viewer & Android
            iosUrl: "assets/models/alex-chen.usdz",    // For iOS AR - ADD THIS!
            poster: "assets/models/alex-poster.jpg",
            alt: "Description"
        }
    }
};
```

### File Organization:
```
assets/
├── models/
│   ├── alex-chen.glb     (for web viewer & Android AR)
│   ├── alex-chen.usdz    (for iOS AR Quick Look)
│   ├── maria-garcia.glb
│   ├── maria-garcia.usdz
│   └── ...
```

## Testing Your AR Setup

### On iPhone/iPad:
1. Open Safari (must be Safari, not Chrome!)
2. Navigate to your gallery
3. Tap "View in AR"
4. Should open AR Quick Look
5. Scan floor and tap to place

### Common iOS Issues & Solutions:

**Issue**: "View in AR" does nothing
- **Solution**: Ensure USDZ file is provided and accessible
- **Check**: File permissions (must be publicly readable)

**Issue**: Model appears but can't be placed
- **Solution**: Check USDZ file size (keep under 10MB)
- **Solution**: Ensure good lighting for floor detection

**Issue**: Textures missing in AR
- **Solution**: Textures must be embedded in USDZ, not external

## USDZ Requirements & Best Practices

### Technical Requirements:
- **Max file size**: 10MB (iOS may reject larger files)
- **Textures**: Must be embedded, not referenced
- **Format**: USDZ (not USDA or USDC)
- **Animations**: Supported but increase file size

### Optimization Tips:
1. **Reduce polygon count**: Under 100k triangles ideal
2. **Compress textures**: 1024x1024 or smaller
3. **Single mesh**: Combine meshes when possible
4. **No transparency**: iOS AR handles transparency poorly

## Quick Debug Checklist

- [ ] USDZ files created for each student
- [ ] USDZ files under 10MB each
- [ ] Both GLB and USDZ files uploaded to server
- [ ] URLs are correct in studentsData
- [ ] Testing on Safari (not Chrome) on iOS
- [ ] Files are accessible (no CORS issues)
- [ ] HTTPS enabled (required for AR)

## Working Example URLs

For testing, you can use these working model URLs:

```javascript
model: {
    url: "https://modelviewer.dev/shared-assets/models/Astronaut.glb",
    iosUrl: "https://modelviewer.dev/shared-assets/models/Astronaut.usdz",
    poster: "poster.jpg",
    alt: "3D model"
}
```

## Alternative: Direct USDZ Links

If the AR button still doesn't work, you can add a fallback direct link:

```html
<!-- Add this as a fallback -->
<a href="assets/models/student-model.usdz" rel="ar">
    <img src="preview.jpg" alt="AR Model">
    <span>View in AR (Direct)</span>
</a>
```

This creates a direct AR Quick Look link that iOS will recognize.

## Server Configuration

Make sure your server has correct MIME types:

### Apache (.htaccess):
```apache
AddType model/vnd.usdz+zip .usdz
AddType model/gltf-binary .glb
```

### Nginx:
```nginx
types {
    model/vnd.usdz+zip usdz;
    model/gltf-binary glb;
}
```

## Summary

The key fix is:
1. **Convert all GLB files to USDZ**
2. **Host both versions**
3. **Add iosUrl to your data**
4. **Test on Safari iOS**

The updated HTML file I provided includes all the necessary iOS AR fixes and fallbacks. Once you have USDZ files, your AR feature will work perfectly on iOS!