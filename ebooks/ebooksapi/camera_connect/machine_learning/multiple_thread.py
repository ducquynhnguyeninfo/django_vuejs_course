import time
import cv2
import multiprocessing as mp

ip_address="10.86.7.123"
username="admin"
password="123456aA"
def read_frames(output_queue, event):
    # video_path = 'path_to_video_file.mp4'
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(f'rtsp://{username}:{password}@{ip_address}/1')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        output_queue.put(frame)  # Gửi frame tới luồng xử lý
        # event.set()  

    cap.release()
    output_queue.put(None)  # Gửi None để đánh dấu kết thúc luồng

def process_frames(input_queue, event):
    while True:
        #event.wait()
        frame = input_queue.get()  # Nhận frame từ luồng đọc
        # event.clear()  # Xóa cờ

        if frame is None:
            break

        # Xử lý frame: vẽ một hình tròn màu đỏ
        circle_color = (0, 0, 255)
        circle_center = (250, 250)
        circle_radius = 120

        time.sleep(0.5)
        while not input_queue.empty():
            input_queue.get()
            
        cv2.circle(frame, circle_center, circle_radius, circle_color, -1)

        # Hiển thị frame
        cv2.imshow('Processed Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    event_queue = mp.Queue()
    event = mp.Event()

    #output_queue = mp.Queue()

    # Tạo và khởi chạy luồng đọc
    reader_process = mp.Process(target=read_frames, args=(event_queue, event))
    reader_process.start()

    # Tạo và khởi chạy luồng xử lý
    processor_process = mp.Process(target=process_frames, args=(event_queue, event))
    processor_process.start()

    reader_process.join()
    processor_process.join()
