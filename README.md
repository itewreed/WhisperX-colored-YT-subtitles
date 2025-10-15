# WhisperX-colored-YT-subtitles
Python script, that color codes speaker tags, made by WhisperX, to ytt subtitles. JSON subtitle output of WhisperX is used.

## Usage
The input is always a directory. It will convert all subtitles in that directory. The ytt files will be saved in that same directory

### Standard convert
```python subtitle_json-2-ytt.py --subtitledir <path to directory with subtitles>```

### Single word convert
Single words will be shown, instead of complete sentences. Usually known from short form videos. ytt files have the additional _words tag in the filename.

```python subtitle_json-2-ytt.py --subtitledir <path to directory with subtitles> --words```
