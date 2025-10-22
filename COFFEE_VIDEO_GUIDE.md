# Coffee Product Video Embed Guide

This guide explains how to add video embeds to coffee products in the Pilgrims Kitchen & Inn website.

## Overview

The `CoffeeProduct` model now supports embedding videos from YouTube and Vimeo. Videos will be displayed on the product detail page in a responsive 16:9 aspect ratio player.

## Features Added

### 1. Database Field
- **Field Name**: `embed_video_url`
- **Type**: URLField (max length: 500 characters)
- **Optional**: Yes (blank=True)
- **Location**: `coffee/models.py` line 94

### 2. Template Display
- **Location**: `coffee/templates/coffee/coffee-detail.html` lines 498-525
- **Features**:
  - Responsive 16:9 video player
  - Only displays if video URL is provided
  - Positioned between product tabs and similar coffees section
  - Beautiful header with icon and decorative lines
  - Supports fullscreen playback
  - Dark theme compatible

### 3. Migration
- **File**: `coffee/migrations/0017_coffeeproduct_embed_video_url.py`
- **Status**: Applied successfully ✅

---

## How to Add Videos to Coffee Products

### Step 1: Get the Correct Embed URL

#### For YouTube Videos:

1. Go to your YouTube video
2. Click the **Share** button
3. Click **Embed**
4. Copy the `src` URL from the iframe code

**Example:**
```
Original URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Embed URL: https://www.youtube.com/embed/dQw4w9WgXcQ
```

**Correct Format:**
```
https://www.youtube.com/embed/VIDEO_ID
```

#### For Vimeo Videos:

1. Go to your Vimeo video
2. Click the **Share** button
3. Look for the embed code
4. Copy the `src` URL from the iframe

**Example:**
```
Original URL: https://vimeo.com/123456789
Embed URL: https://player.vimeo.com/video/123456789
```

**Correct Format:**
```
https://player.vimeo.com/video/VIDEO_ID
```

### Step 2: Add Video URL via Django Admin

1. **Login to Django Admin**
   - URL: `http://localhost:8000/admin/`
   - Use your superuser credentials

2. **Navigate to Coffee Products**
   - Click on "Coffee" section
   - Click on "Coffee products"

3. **Edit the Product**
   - Find the coffee product you want to add a video to
   - Click on its name to edit

4. **Add the Embed URL**
   - Scroll down to the **Embed video url** field
   - Paste the embed URL (NOT the watch URL!)
   - Example: `https://www.youtube.com/embed/dQw4w9WgXcQ`

5. **Save**
   - Click "Save" button at the bottom

### Step 3: Verify on Frontend

1. Visit the coffee product detail page
2. Scroll down past the tabs section
3. You should see the video player with the heading "Product Video"
4. Test that the video plays correctly

---

## Example URLs

### ✅ Correct Embed URLs

```
https://www.youtube.com/embed/dQw4w9WgXcQ
https://www.youtube.com/embed/abc123xyz
https://player.vimeo.com/video/123456789
https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1
https://www.youtube.com/embed/abc123?si=xyz123&autoplay=1
```

### ❌ Incorrect URLs (Won't Work)

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ  ← Watch URL
https://youtu.be/dQw4w9WgXcQ                 ← Short URL
https://vimeo.com/123456789                  ← Direct Vimeo URL
www.youtube.com/embed/abc123                 ← Missing https://
```

---

## Optional Video Parameters

### YouTube Parameters

You can add parameters to the embed URL for additional features:

```
https://www.youtube.com/embed/VIDEO_ID?autoplay=1&mute=1&loop=1
```

**Common Parameters:**
- `autoplay=1` - Auto-play video on page load
- `mute=1` - Mute audio (recommended with autoplay)
- `loop=1` - Loop the video
- `controls=0` - Hide video controls
- `rel=0` - Don't show related videos at the end
- `modestbranding=1` - Minimal YouTube branding

**Example with parameters:**
```
https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1&mute=1&rel=0
```

### Vimeo Parameters

```
https://player.vimeo.com/video/VIDEO_ID?autoplay=1&loop=1
```

**Common Parameters:**
- `autoplay=1` - Auto-play video
- `loop=1` - Loop the video
- `muted=1` - Mute audio
- `title=0` - Hide video title
- `byline=0` - Hide author name
- `portrait=0` - Hide author portrait

---

## Troubleshooting

### Video Doesn't Display

1. **Check if URL is saved in admin**
   - Go to Django admin
   - Check if the `Embed video url` field has a value

2. **Verify URL format**
   - Must be an embed URL, not a watch URL
   - Must start with `https://`
   - Check for typos

3. **Clear browser cache**
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

### Video Shows Error in Player

1. **Video is private or deleted**
   - Check if the video exists on YouTube/Vimeo
   - Ensure the video is public or unlisted (not private)

2. **Embedding is disabled**
   - Some videos don't allow embedding
   - Try a different video

3. **URL format is incorrect**
   - Double-check you're using the embed URL format
   - Remove any extra parameters that might be breaking it

---

## Design Features

### Responsive Design
- Video maintains 16:9 aspect ratio on all screen sizes
- Mobile-friendly and tablet-optimized
- Fullscreen support enabled

### Visual Design
- Rounded corners (rounded-2xl)
- Drop shadow for depth
- Decorative header with play icon
- Consistent with site's amber color scheme
- Dark mode compatible

### User Experience
- Only shows when video is available
- Positioned logically after product information
- Smooth integration with existing design
- Supports all standard video player controls

---

## Technical Details

### Model Field Configuration

```python
embed_video_url = models.URLField(
    max_length=500,
    blank=True,
    help_text="YouTube or Vimeo embed URL (e.g., https://www.youtube.com/embed/VIDEO_ID)"
)
```

### Template Code

```django
{% if coffee.embed_video_url %}
<div class="border-t border-gray-200 dark:border-gray-700 pt-12 mt-12">
    <div class="text-center mb-8">
        <!-- Header with decorative lines -->
    </div>

    <div class="max-w-4xl mx-auto">
        <div class="relative pb-[56.25%] h-0 overflow-hidden rounded-2xl shadow-2xl bg-gray-900">
            <iframe
                src="{{ coffee.embed_video_url }}"
                class="absolute top-0 left-0 w-full h-full"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
            </iframe>
        </div>
    </div>
</div>
{% endif %}
```

### CSS Classes Used

- `pb-[56.25%]` - 16:9 aspect ratio (56.25% = 9/16 * 100%)
- `rounded-2xl` - Extra rounded corners
- `shadow-2xl` - Large shadow for depth
- `dark:border-gray-700` - Dark mode support
- `max-w-4xl` - Constrained width for better viewing

---

## Best Practices

### 1. Video Content
- Keep videos under 5 minutes for product demos
- Show the coffee brewing process
- Highlight unique features of the product
- Include tasting notes and flavor profiles

### 2. Video Quality
- Use at least 720p HD quality
- Ensure good lighting and clear audio
- Professional or semi-professional production recommended
- Add subtitles for accessibility

### 3. SEO Considerations
- Add descriptive video titles on YouTube/Vimeo
- Include relevant tags and descriptions
- Use custom thumbnails that are eye-catching
- Enable embedding in video settings

### 4. Performance
- Don't auto-play videos (unless muted)
- Use video thumbnails that load quickly
- Consider lazy loading for pages with multiple videos
- Test on mobile devices for performance

---

## Future Enhancements

Possible improvements for future versions:

1. **Multiple Videos**
   - Add a gallery of videos per product
   - Carousel or tabs for multiple videos

2. **Video Analytics**
   - Track video views and engagement
   - Measure conversion impact

3. **Custom Player**
   - Branded video player
   - Custom controls and styling

4. **Video Thumbnails**
   - Generate/upload custom thumbnails
   - Display thumbnail before video loads

---

## Support

If you encounter issues:

1. Check this guide first
2. Verify URL format matches examples
3. Test with a known working video
4. Check browser console for errors
5. Ensure migrations are applied

For additional help, refer to:
- Django documentation: https://docs.djangoproject.com/
- YouTube Embed API: https://developers.google.com/youtube/player_parameters
- Vimeo Embed: https://developer.vimeo.com/player/sdk

---

**Last Updated**: October 22, 2025
**Version**: 1.0
**Migration**: 0017_coffeeproduct_embed_video_url
