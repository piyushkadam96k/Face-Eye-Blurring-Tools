import cv2
import mediapipe as mp
import os

mp_face_mesh = mp.solutions.face_mesh

def blur_eyes_only(source):
    cap = cv2.VideoCapture(source)
    is_webcam = source == 0
    if not cap.isOpened():
        return

    if not is_webcam:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out_path = source.rsplit('.', 1)[0] + '_eyes_blurred.mp4'
        out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

    # Use FaceMesh for precise eye landmarks
    with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=10,
        refine_landmarks=True,        # Gives iris landmarks — crucial for eyes
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if is_webcam:
                frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                h, w = frame.shape[:2]
                for face_landmarks in results.multi_face_landmarks:
                    # Left eye (landmarks 468–473 for iris, but we blur full eye area)
                    left_eye_pts = [33, 7, 163, 144, 145, 153, 154, 155, 133, 130, 159, 158, 157, 173]
                    # Right eye
                    right_eye_pts = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385]

                    for eye_indices in [left_eye_pts, right_eye_pts]:
                        pts = []
                        for i in eye_indices:
                            lm = face_landmarks.landmark[i]
                            pts.append([int(lm.x * w), int(lm.y * h)])
                        
                        if len(pts) > 3:
                            x_coords = [p[0] for p in pts]
                            y_coords = [p[1] for p in pts]
                            x1, x2 = max(0, min(x_coords) - 12), min(w, max(x_coords) + 12)
                            y1, y2 = max(0, min(y_coords) - 12), min(h, max(y_coords) + 12)
                            
                            if x2 > x1 + 20 and y2 > y1 + 10:
                                eye_region = frame[y1:y2, x1:x2]
                                blurred = cv2.GaussianBlur(eye_region, (71, 71), 30)
                                frame[y1:y2, x1:x2] = blurred

            if is_webcam:
                cv2.imshow('Eyes Only Blur - Press Q', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                out.write(frame)
                cv2.imshow('Blurring Eyes...', cv2.resize(frame, (854, 480)))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    cap.release()
    if not is_webcam:
        out.release()
    cv2.destroyAllWindows()


# One-time choice → then runs silently
if __name__ == "__main__":
    choice = input("Webcam (w) or Video (v)? → ").strip().lower()
    if choice == 'w':
        blur_eyes_only(0)
    elif choice == 'v':
        path = input("Video path → ").strip().strip('"\'')
        if os.path.isfile(path):
            blur_eyes_only(path)