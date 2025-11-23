# OPAQUE Assets

This directory contains the official OPAQUE logo and brand assets.

## Logo Files

### Main Logo
- **logo.svg** - Full logo with wordmark and tagline (400x400px)
  - Use for: Documentation, presentations, social media posts
  
### Icon Only
- **logo-icon.svg** - Shield icon without text (300x300px)
  - Use for: Favicon, app icons, profile pictures, small spaces

### Horizontal Layout
- **logo-horizontal.svg** - Logo with horizontal layout (600x200px)
  - Use for: Headers, banners, wide layouts, documentation headers

## Design Concept

The OPAQUE logo represents:

- **Shield Shape**: Protection and security of sensitive data
- **Geometric Precision**: Mathematical validation (not AI guessing)
- **Hexagonal Pattern**: Data structures and encryption
- **Checkmark**: Validation and verification
- **Clean Lines**: Deterministic and precise approach

## Color Palette

- **Primary Navy**: `#1a2332` - Trust, security, professionalism
- **Accent Cyan**: `#00d4ff` - Technology, precision, clarity
- **Secondary Gray**: `#8b9dc3` - Depth and sophistication
- **Text Gray**: `#6c757d` - Readable, professional

## Usage Guidelines

### Do's ✅
- Use the logo on solid backgrounds (white, light gray, or dark navy)
- Maintain aspect ratio when resizing
- Ensure adequate clear space around the logo
- Use SVG format for web and print (scales perfectly)

### Don'ts ❌
- Don't distort or skew the logo
- Don't change the colors
- Don't add effects or shadows (already included in design)
- Don't use on busy backgrounds that reduce legibility

## File Formats

All logos are provided in **SVG format** (Scalable Vector Graphics):
- ✅ Scales to any size without quality loss
- ✅ Small file size
- ✅ Perfect for web and print
- ✅ Editable in vector graphics software

## Converting to Other Formats

If you need PNG or other formats, you can convert using:

**Online tools:**
- [CloudConvert](https://cloudconvert.com/svg-to-png)
- [Convertio](https://convertio.co/svg-png/)

**Command line (with ImageMagick):**
```bash
# Convert to PNG (high resolution)
magick logo.svg -density 300 -resize 1200x1200 logo.png

# Convert to favicon
magick logo-icon.svg -density 300 -resize 512x512 favicon.png
```

**Python (with cairosvg):**
```python
import cairosvg

cairosvg.svg2png(url='logo.svg', write_to='logo.png', scale=3)
```

## Questions?

For brand guidelines or custom logo requests, please open an issue on GitHub.

---

**Built with precision by Samuel Silva**
*Protecting data with mathematics, not magic* ✨
