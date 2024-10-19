# Integrating STJ with FFmpeg

This guide explains how to use STJ files with FFmpeg to embed subtitles into videos.

## Overview

FFmpeg is a powerful tool for processing audio and video files. While FFmpeg doesn't natively support STJ files, you can convert STJ to a compatible subtitle format (e.g., SRT or WebVTT) and then use FFmpeg to embed the subtitles into a video.

## Steps

1. **Convert STJ to SRT or VTT**: Use the provided scripts to convert your STJ file to an SRT or VTT file.

   ```bash
   python tools/python/stj_to_srt.py examples/complex.stj.json subtitles.srt
   ```

2. **Embed Subtitles into Video**: Use FFmpeg to embed the subtitles into your video file.

   For SRT subtitles:

   ```bash
   ffmpeg -i input_video.mp4 -vf subtitles=subtitles.srt output_video.mp4
   ```

   For WebVTT subtitles:

   ```bash
   ffmpeg -i input_video.mp4 -i subtitles.vtt -c copy -c:s mov_text output_video.mp4
   ```

3. **Advanced Styling**: If you have styling information in your STJ file, note that SRT and VTT have limited styling capabilities. For more advanced styling, you might need to use ASS/SSA subtitles.

   - Convert STJ to ASS format (additional script required).
   - Use FFmpeg to embed ASS subtitles:

     ```bash
     ffmpeg -i input_video.mp4 -vf ass=subtitles.ass output_video.mp4
     ```

## Notes

- **Subtitle Positioning**: SRT and VTT formats support limited positioning. If your STJ file includes positioning, you may need to adjust the subtitles manually or use a format that supports advanced positioning like ASS.

- **Subtitle Encoding**: Ensure that your subtitle files are encoded in UTF-8 to prevent character encoding issues.

- **Multiple Subtitle Tracks**: To add multiple subtitle tracks (e.g., different languages), include each subtitle file as an input:

  ```bash
  ffmpeg -i input_video.mp4 -i subtitles_en.srt -i subtitles_es.srt -map 0 -map 1 -map 2 -c copy -c:s mov_text -metadata:s:s:0 language=eng -metadata:s:s:1 language=spa output_video.mp4
  ```

## Example

Here's a complete example:

```bash
# Step 1: Convert STJ to SRT
python tools/python/stj_to_srt.py examples/complex.stj.json subtitles.srt

# Step 2: Embed SRT subtitles into video
ffmpeg -i input_video.mp4 -vf subtitles=subtitles.srt output_video.mp4
```

## Additional Resources

- [FFmpeg Documentation](https://ffmpeg.org/ffmpeg.html)
- [Embedding Subtitles with FFmpeg](https://trac.ffmpeg.org/wiki/HowToBurnSubtitlesIntoVideo)
```
