import cv2
import mediapipe as mp
import os

mp_face_detection = mp.solutions.face_detection

def fast_blur(source):
    cap = cv2.VideoCapture(source)
    is_webcam = source == 0
    if not cap.isOpened():
        return

    if not is_webcam:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out_path = source.rsplit('.', 1)[0] + '_blurred.mp4'
        out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as detector:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if is_webcam:
                frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = detector.process(rgb)

            if results.detections:
                ih, iw = frame.shape[:2]
                for d in results.detections:
                    b = d.location_data.relative_bounding_box
                    x1 = max(0, int(b.xmin * iw))
                    y1 = max(0, int(b.ymin * ih))
                    x2 = min(iw, int((b.xmin + b.width) * iw))
                    y2 = min(ih, int((b.ymin + b.height) * ih))
                    if x2 > x1 and y2 > y1:
                        face = frame[y1:y2, x1:x2]
                        frame[y1:y2, x1:x2] = cv2.GaussianBlur(face, (99,99), 40)

            if is_webcam:
                cv2.imshow('Face Blur - Press Q to Quit', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                out.write(frame)
                cv2.imshow('Blurring... Press Q to Stop', cv2.resize(frame, (854, 480)))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    cap.release()
    if not is_webcam:
        out.release()
    cv2.destroyAllWindows()

# ——— Ask once, then run silently & fast ———
if __name__ == "__main__":
    choice = input("Webcam (w) or Video file (v)? → ").strip().lower()
    
    if choice == 'w':
        fast_blur(0)
    elif choice == 'v':
        path = input("Drag & drop video or type path → ").strip().strip('"\'')
        if os.path.exists(path):
            fast_blur(path)
        else:
            print("File not found.")
    else:
        print("Invalid.")