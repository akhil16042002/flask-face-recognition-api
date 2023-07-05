from flask import Flask, request, jsonify
import face_recognition
import cv2
import numpy as np
import os
import uuid
import tempfile
import shutil

app = Flask(__name__)

@app.route('/face-recognition', methods=['POST'])
def face_recognition_api():
    # Get the uploaded image and video files from the request
    image_file = request.files['image']
    video_file = request.files['video']
    
    # Create a temporary directory to store the files
    temp_dir = tempfile.mkdtemp()

    # Generate unique filenames for the image and video files
    image_filename = str(uuid.uuid4()) + '.png'
    video_filename = str(uuid.uuid4()) + '.mp4'

    # Save the image and video files to the temporary directory
    image_path = os.path.join(temp_dir, image_filename)
    video_path = os.path.join(temp_dir, video_filename)
    image_file.save(image_path)
    video_file.save(video_path)

    # Load the known image and get the encoding
    known_image = face_recognition.load_image_file(image_path)
    known_face_encoding = face_recognition.face_encodings(known_image)[0]

    # Load the video for face detection
    video_capture = cv2.VideoCapture(video_path)

    # Load variables to get details from each frame from the video
    frame_count = 0
    match_found = False

    max_match_percent = 0
    frame_frequency = 0
    sum_match_percent = 0

    while video_capture.isOpened():
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Bail out when the video file ends
        if not ret:
            video_capture.release()
            break

        frame_count += 1
    	# Check one frame out of every  five
        if frame_count % 5 == 0:
 
            # Convert BGR2RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for face_encoding in face_encodings:
                # See if the face is a match for the known face
                match = face_recognition.compare_faces([known_face_encoding], face_encoding, tolerance=0.50)

                if match[0]:
                    match_percent = (1 - face_recognition.face_distance([known_face_encoding], face_encoding)[0]) * 100
                    # Find max percentage match and number of matches
                    frame_frequency += 1
                    sum_match_percent += match_percent 
                    if match_percent > max_match_percent: 
                        max_match_percent = match_percent
                        max_frame_count = frame_count

                    match_found = True

    if match_found:
        response = {
            "message": "Match found",
            "max_percentage_match": max_match_percent,
            "frame_at_which_max_percentage_match_was_found": max_frame_count,
            "number_of_frames_where_a_match_was_found": frame_frequency,
            "average_match_percentage": sum_match_percent / frame_frequency
        }
    else:
        response = {
            "message": "No match"
        }
        
    # Delete the temporary directory and its contents
    shutil.rmtree(temp_dir)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug = True, port = 2000)
