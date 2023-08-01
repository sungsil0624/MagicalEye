import cv2
import os
import concurrent.futures

def save_frames_as_images(video_path, output_folder, frame_interval=1):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Unable to open the video file '{video_path}'.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_interval_frames = int(fps * frame_interval)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0
    success = True

    while success:
        success, frame = cap.read()

        if frame_count % frame_interval_frames != 0:
            frame_count += 1
            continue

        if success:
            frame_filename = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(video_path))[0]}_frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_paths = [
        "test1.mp4",
        "test2.mp4",
        "test3.mp4",
        "test4.mp4",
        "test5.mp4"
    ]
    output_folder = "output_frames"
    frame_interval_seconds = 1

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(save_frames_as_images, path, output_folder, frame_interval_seconds) for path in
                   video_paths]

        concurrent.futures.wait(futures)
    # 변환 성공시
    print("All videos processed successfully.")