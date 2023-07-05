# Face Recognition API

This is a Flask-based API that performs face recognition on a video file using the `face_recognition` library. The API accepts an image file and a video file, and it compares the faces detected in the video with the known face in the image to find a match.

## Installation

To run this API, follow these steps:

1. Install the required dependencies by running the following command:

   ```bash
   pip install flask opencv-python-headless face_recognition
   ```

2. Save the provided code into a Python file, e.g., `face_recognition_api.py`.

3. Execute the Python file to start the API server:

   ```bash
   python face_recognition_api.py
   ```

   The API server will run on `http://localhost:2000`.

## API Endpoints

### Face Recognition

**Endpoint**: `/face-recognition`

**Method**: `POST`

**Parameters**:
- `image`: The image file containing the known face. (Type: File)
- `video`: The video file to perform face recognition on. (Type: File)

**Example**:

```python
import requests

image_file = open('known_face.png', 'rb')
video_file = open('video.mp4', 'rb')

files = {'image': image_file, 'video': video_file}
response = requests.post('http://localhost:2000/face-recognition', files=files)

print(response.json())
```

**Response**:

The API responds with a JSON object containing the result of the face recognition process:

- If a match is found:
  - `"message"`: "Match found"
  - `"max_percentage_match"`: The maximum percentage match found in the video.
  - `"frame_at_which_max_percentage_match_was_found"`: The frame number where the maximum percentage match was found.
  - `"number_of_frames_where_a_match_was_found"`: The total number of frames in the video where a match was found.
  - `"average_match_percentage"`: The average percentage match across all frames where a match was found.

- If no match is found:
  - `"message"`: "No match"

## Limitations

- The API currently only supports one known face. If there are multiple known faces in the image, it will only consider the first face detected.
- The API uses a tolerance of 0.50 for comparing face encodings. You may need to adjust this value based on your specific use case to achieve better results.

## Conclusion

The Face Recognition API provides a simple way to perform face recognition on a video file. By sending an image file containing the known face and a video file for analysis, the API will identify and provide information about any matches found in the video.
