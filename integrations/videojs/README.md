# Integrating STJ with Video.js

This guide explains how to use STJ files with Video.js to display subtitles on web videos.

## Overview

Video.js is a popular open-source HTML5 video player. It supports WebVTT subtitles, which can be generated from STJ files.

## Steps

1. **Convert STJ to WebVTT**: Use the provided script to convert your STJ file to a VTT file.

   ```bash
   python tools/python/stj_to_vtt.py examples/latest/complex.stj.json subtitles.vtt
   ```

2. **Include Subtitles in Your HTML**:

   ```html
   <video id="my-video" class="video-js" controls preload="auto" width="640" height="264" data-setup="{}">
     <source src="video.mp4" type="video/mp4">
     <track kind="subtitles" src="subtitles.vtt" srclang="en" label="English" default>
   </video>
   ```

3. **Initialize Video.js**:

   ```html
   <script src="https://vjs.zencdn.net/7.11.4/video.min.js"></script>
   ```

## Notes

- **Multiple Languages**: To add subtitles in multiple languages, include multiple `<track>` elements with different `srclang` and `label` attributes.

- **Styling**: WebVTT supports limited styling. For advanced styling, you may need to use additional JavaScript or CSS.

## Example

Here's a complete HTML example:

```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://vjs.zencdn.net/7.11.4/video-js.css" rel="stylesheet" />
</head>
<body>
  <video id="my-video" class="video-js" controls preload="auto" width="640" height="264" data-setup="{}">
    <source src="video.mp4" type="video/mp4">
    <track kind="subtitles" src="subtitles_en.vtt" srclang="en" label="English" default>
    <track kind="subtitles" src="subtitles_es.vtt" srclang="es" label="Español">
  </video>
  <script src="https://vjs.zencdn.net/7.11.4/video.min.js"></script>
</body>
</html>
```

## Additional Resources

- [Video.js Documentation](https://videojs.com/)
- [Adding Subtitles and Captions](https://docs.videojs.com/tutorial-captioning.html)
```
