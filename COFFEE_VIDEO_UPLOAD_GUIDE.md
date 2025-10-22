# Coffee Product Video Upload Guide

This guide explains how to upload video files directly to coffee products in the Pilgrims Kitchen & Inn website.

## Overview

The `CoffeeProduct` model supports uploading video files (MP4, WebM, OGV) directly to the server. Videos will be displayed on the product detail page with HTML5 video player controls.

## Features

### 1. Database Field
- **Field Name**: `video`
- **Type**: FileField
- **Upload Path**: `media/products/videos/`
- **Optional**: Yes (blank=True, null=True)
- **Supported Formats**: MP4, WebM, OGV
- **Location**: `coffee/models.py` line 94

### 2. Template Display
- **Location**: `coffee/templates/coffee/coffee-detail.html` lines 498-529
- **Features**:
  - HTML5 video player with native controls
  - Responsive design
  - Multiple video format support
  - Product image as video poster
  - Download prevention option
  - Only displays if video file is uploaded

### 3. Admin Interface
- **Location**: `coffee/admin.py` line 86
- **Features**:
  - Easy file upload interface
  - Clear/Delete option
  - File size and format validation

---

## How to Upload Videos

### Step 1: Prepare Your Video File

#### Recommended Specifications:
- **Format**: MP4 (H.264 codec recommended)
- **Resolution**: 1280x720 (720p) or 1920x1080 (1080p)
- **File Size**: Under 50MB for web performance
- **Duration**: 30 seconds to 2 minutes for product demos
- **Frame Rate**: 24-30 fps
- **Bit Rate**: 2-5 Mbps

#### Optimize Your Video:
Use video compression tools to reduce file size:
- **Online Tools**: CloudConvert, Online-Convert, Clideo
- **Desktop Software**: HandBrake, FFmpeg, Adobe Media Encoder
- **Mobile Apps**: Video Compressor, Video Converter

**FFmpeg Command Example:**
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset slow -crf 23 -c:a aac -b:a 128k -vf scale=1280:720 output.mp4
```

### Step 2: Upload via Django Admin

1. **Login to Django Admin**
   - URL: `http://localhost:8000/admin/`
   - Use your superuser credentials

2. **Navigate to Coffee Products**
   - Click on "Coffee" section
   - Click on "Coffee products"

3. **Edit the Product**
   - Find the coffee product
   - Click on its name to edit

4. **Upload the Video**
   - Scroll to the "ຂໍ້ມູນພື້ນຖານ" (Basic Information) section
   - Find the **Video** field
   - Click "Choose File" or "Browse"
   - Select your video file
   - Wait for upload to complete

5. **Save**
   - Click "Save" button at the bottom
   - Video will be saved to `media/products/videos/`

### Step 3: Verify on Frontend

1. Visit the coffee product detail page
2. Scroll down past the tabs section
3. You should see the video player with "Product Video" heading
4. Click play to test the video

---

## Supported Video Formats

### Primary Format (Recommended):
- **MP4 (H.264)**: `.mp4`
  - Best compatibility across all browsers
  - Good compression and quality balance
  - Recommended codec: H.264 with AAC audio

### Alternative Formats:
- **WebM**: `.webm`
  - Open-source format
  - Good quality and compression
  - Codec: VP8 or VP9 with Vorbis/Opus audio

- **OGG**: `.ogg` or `.ogv`
  - Open-source format
  - Codec: Theora with Vorbis audio

### Browser Compatibility:
| Format | Chrome | Firefox | Safari | Edge |
|--------|--------|---------|--------|------|
| MP4    | ✅     | ✅      | ✅     | ✅   |
| WebM   | ✅     | ✅      | ❌     | ✅   |
| OGG    | ✅     | ✅      | ❌     | ❌   |

**Recommendation**: Always use MP4 for maximum compatibility.

---

## Video Player Features

### Built-in Controls:
- ▶️ Play/Pause button
- 🔊 Volume control
- ⏩ Seek/Timeline bar
- ⏱️ Current time / Duration display
- ⛶ Fullscreen toggle
- ⚙️ Playback speed (browser dependent)

### Custom Features:
- **Poster Image**: Product image shows before video plays
- **Preload**: Video metadata loads on page load
- **No Download**: Right-click download is disabled
- **Responsive**: Video scales to fit screen size

---

## File Size Recommendations

### By Video Length:
| Duration | Max File Size | Resolution |
|----------|---------------|------------|
| 15-30s   | 10-15 MB      | 720p       |
| 30-60s   | 20-30 MB      | 720p       |
| 1-2 min  | 40-50 MB      | 720p       |
| 2-5 min  | 60-100 MB     | 1080p      |

### Server Limits:
- **Django**: Check `settings.py` for `DATA_UPLOAD_MAX_MEMORY_SIZE`
- **Nginx/Apache**: Check `client_max_body_size` configuration
- **PHP (if applicable)**: Check `upload_max_filesize` and `post_max_size`

---

## Troubleshooting

### Video Doesn't Upload

**Issue**: File too large
- **Solution**: Compress video using FFmpeg or online tools
- **Check**: Server upload limits in `settings.py`

**Issue**: Wrong file format
- **Solution**: Convert to MP4 using video converter
- **Verify**: File extension is `.mp4`, `.webm`, or `.ogv`

**Issue**: Upload timeout
- **Solution**: Increase server timeout settings
- **Alternative**: Use smaller video file

### Video Doesn't Play

**Issue**: Video file corrupted
- **Solution**: Re-export video from editing software
- **Test**: Try playing video in VLC media player first

**Issue**: Codec not supported
- **Solution**: Re-encode with H.264 codec
- **Command**:
  ```bash
  ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
  ```

**Issue**: File path incorrect
- **Solution**: Check if file exists in `media/products/videos/`
- **Verify**: Check Django `MEDIA_URL` and `MEDIA_ROOT` settings

### Video Shows But Won't Play

**Issue**: Browser compatibility
- **Solution**: Use MP4 format with H.264 codec
- **Test**: Try different browser

**Issue**: Missing codec
- **Solution**: Install browser codecs or use supported format
- **Check**: Browser console for errors

---

## Best Practices

### 1. Video Content
✅ **Do:**
- Show coffee brewing process
- Highlight product features
- Include tasting notes demonstration
- Show grind size and color
- Display packaging and labeling

❌ **Don't:**
- Make videos too long (> 3 minutes)
- Include copyrighted music
- Use low-quality footage
- Add excessive text overlays

### 2. Technical Quality
✅ **Do:**
- Use good lighting
- Stabilize camera (use tripod)
- Record in landscape orientation
- Use clear audio
- Edit for conciseness

❌ **Don't:**
- Upload shaky footage
- Use portrait orientation
- Include background noise
- Skip compression
- Upload in 4K (too large)

### 3. Performance
✅ **Do:**
- Compress videos before upload
- Use MP4 with H.264
- Keep under 50MB
- Test on mobile devices
- Optimize for web

❌ **Don't:**
- Upload raw uncompressed files
- Use exotic codecs
- Exceed 100MB per video
- Forget to test loading speed

### 4. SEO & Accessibility
✅ **Do:**
- Add descriptive product descriptions
- Use clear video titles
- Consider adding captions (future)
- Optimize page load time

---

## Configuration

### Django Settings

Check `config/settings/base.py` for media configuration:

```python
# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Maximum upload size (50MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB in bytes
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB in bytes
```

### Allowed File Types

The model accepts any file type, but only these will play:
- `video/mp4` - MP4 files
- `video/webm` - WebM files
- `video/ogg` - OGG/OGV files

### Storage Location

Videos are stored in:
```
media/
└── products/
    └── videos/
        ├── coffee-arabica-roast-123.mp4
        ├── coffee-robusta-dark-456.mp4
        └── ...
```

---

## Video Management

### Delete Video

1. Go to Django Admin
2. Edit the coffee product
3. Check "Clear" checkbox next to video field
4. Click "Save"
5. Old video file will be deleted from server

### Replace Video

1. Go to Django Admin
2. Edit the coffee product
3. Click "Choose File" and select new video
4. Click "Save"
5. Old video will be replaced automatically

### Bulk Upload

For multiple videos, consider:
1. Upload videos via FTP to `media/products/videos/`
2. Use Django shell to assign videos:

```python
from coffee.models import CoffeeProduct

coffee = CoffeeProduct.objects.get(slug='coffee-slug')
coffee.video = 'products/videos/filename.mp4'
coffee.save()
```

---

## Security Considerations

### 1. File Validation
- Only accept video file types
- Check file size limits
- Scan for malicious content (future)

### 2. Access Control
- Only admin users can upload
- Frontend users can only view
- No direct download links exposed

### 3. Storage Security
- Files stored outside web root
- Served through Django (if configured)
- Can add authentication layer (future)

---

## Performance Optimization

### Server-Side:
1. **Enable Gzip Compression**
   - Compress video files during transfer
   - Configure in Nginx/Apache

2. **Use CDN** (Optional)
   - Serve videos from CDN
   - Reduces server load
   - Faster delivery worldwide

3. **Lazy Loading** (Future)
   - Load videos only when needed
   - Improves initial page load

### Client-Side:
1. **Preload Metadata**
   - Currently enabled: `preload="metadata"`
   - Loads video info without full video

2. **Responsive Quality** (Future)
   - Serve different quality based on connection
   - Adaptive bitrate streaming

---

## Example Videos

### Good Product Video Examples:
1. **Coffee Brewing Tutorial** (30-60s)
   - Show water temperature
   - Display grind size
   - Pour technique
   - Final cup presentation

2. **Unboxing & Packaging** (15-30s)
   - Open sealed bag
   - Show coffee beans
   - Highlight packaging features
   - Close-up of roast level

3. **Tasting Notes** (45-90s)
   - Smell the aroma
   - Take a sip
   - Describe flavor profile
   - Show body and acidity

---

## Future Enhancements

Possible improvements:

1. **Video Thumbnails**
   - Auto-generate thumbnails
   - Custom thumbnail upload
   - Preview images

2. **Multiple Videos**
   - Video gallery per product
   - Different angles/brewing methods
   - Customer review videos

3. **Video Analytics**
   - Track play count
   - Measure watch time
   - Conversion tracking

4. **Streaming Support**
   - HLS/DASH streaming
   - Adaptive bitrate
   - Better performance for large files

5. **Captions/Subtitles**
   - Multi-language support
   - Accessibility features
   - WebVTT format support

---

## Technical Details

### Model Configuration:
```python
video = models.FileField(
    upload_to='products/videos/',
    blank=True,
    null=True,
    help_text='Upload a small video file (MP4, WebM, OGV)'
)
```

### Template Implementation:
```django
{% if coffee.video %}
<video class="w-full h-auto" controls preload="metadata"
       poster="{{ coffee.images.url }}" controlsList="nodownload">
    <source src="{{ coffee.video.url }}" type="video/mp4">
    <source src="{{ coffee.video.url }}" type="video/webm">
    <source src="{{ coffee.video.url }}" type="video/ogg">
    {% trans "Your browser does not support the video tag." %}
</video>
{% endif %}
```

### CSS Styling:
- `rounded-2xl` - Rounded corners
- `shadow-2xl` - Drop shadow
- `bg-gray-900` - Dark background
- `w-full h-auto` - Responsive sizing
- `overflow-hidden` - Clip corners

---

## Support Resources

- **FFmpeg Documentation**: https://ffmpeg.org/documentation.html
- **HandBrake Guide**: https://handbrake.fr/docs/
- **HTML5 Video**: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video
- **Django FileField**: https://docs.djangoproject.com/en/stable/ref/models/fields/#filefield

---

## Changelog

**Version 1.0** (October 22, 2025)
- Initial implementation
- MP4, WebM, OGV support
- HTML5 video player
- Admin upload interface
- Migration 0018 applied

---

**Last Updated**: October 22, 2025
**Version**: 1.0
**Migration**: 0018_remove_coffeeproduct_embed_video_url_and_more
