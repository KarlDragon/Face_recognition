import os
import cv2
import time
import threading
from .Client import Client

class FaceRecognition:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.warning_count = 1
        self.recognition = False
        self.x_border = self.y_border = 1e6
        self.x1_border = self.y1_border = 0
        self.face_cascade = cv2.CascadeClassifier(r'C:\C++\Homeworks\project\Module_File\Model\haarcascade_frontalface_alt.xml')
        self.nose_cascade = cv2.CascadeClassifier(r'C:\C++\Homeworks\project\Module_File\Model\haarcascade_mcs_nose.xml')
        self.current_folder_path = None  
        self.set_camera_properties(1, 1)

    def set_camera_properties(self, width, height):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def create_folder(self, path):
        os.makedirs(path, exist_ok=True)

    def put_text_on_frame(self, frame, text, count=0):
        text = f"{text}!"
        font = cv2.FONT_HERSHEY_SIMPLEX
        position = (50, 50 + 10 * count)
        font_scale = 1
        font_thickness = 2
        font_color = (0, 0, 255)
        cv2.putText(frame, text, position, font, font_scale, font_color, font_thickness)

    def take_photos(self, frame, timestamp, folder_path):
        file_path = os.path.join(folder_path, f"{timestamp}.jpg")
        cv2.imwrite(file_path, frame)

    def run_face_recognition(self, path, IP, port):
        try:
            client = Client()
            client.connect_server(IP, port)
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                size = frame.shape

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                           flags=cv2.CASCADE_SCALE_IMAGE)
                noses = self.nose_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10),
                                                           flags=cv2.CASCADE_SCALE_IMAGE)

                if len(faces) > 0:
                    self.recognition = True
                    first_face = faces[0]
                else:
                    first_face = None
                    self.put_text_on_frame(frame, 'Can not recognize face', 1)

                if len(noses) > 0:
                    first_nose = noses[0]
                else:
                    first_nose = None

                if first_face is not None and first_nose is not None:
                    x_face, y_face, w_face, h_face = first_face
                    x1_face = x_face + w_face
                    y1_face = y_face + h_face
                    xmd_face = round(x_face + w_face / 2)

                    x_nose, y_nose, w_nose, h_nose = first_nose
                    xmd_nose, ymd_nose = x_nose + w_nose // 2, y_nose + h_nose // 2

                    self.x_border = round(min((size[1] - w_face) / 2 + 5, self.x_border))
                    self.y_border = round(min((size[0] - h_face) / 2 + 5, self.y_border))
                    self.x1_border = round(max((size[1] + w_face) / 2 + 5, self.x1_border))
                    self.y1_border = round(max((size[0] + h_face) / 2 + 5, self.y1_border))

                    if not (self.x_border < x_face and self.y_border < y_face and
                            self.x1_border > x1_face and self.y1_border > y1_face):

                        cv2.rectangle(frame, (self.x_border, self.y_border), (self.x1_border, self.y1_border),
                                      (0, 0, 255), 1)
                        cv2.rectangle(frame, (x_nose, y_nose), (x_nose + w_nose, y_nose + h_nose), (255, 0, 0), 1)
                        cv2.rectangle(frame, (x_face, y_face), (x1_face, y1_face), (0, 255, 0), 1)

                        self.put_text_on_frame(frame, 'Please move your face into frame!', 1)
                        
                if self.recognition:
                    distance = abs(xmd_face - xmd_nose)

                    if distance > 4 or first_face is None:
                        self.put_text_on_frame(frame, 'Warning!!', 3)

                        time_now = time.strftime("(%d-%m-%Y) (%H-%M-%S)", time.localtime())

                        if not self.current_folder_path:
                            self.current_folder_path = os.path.join(path, f'Warning_{self.warning_count}')
                            self.create_folder(self.current_folder_path)

                            if os.path.exists(os.path.join(path, f'Warning_{self.warning_count - 1}')):
                                send_thread = threading.Thread(target=client.send_images, args=(os.path.join(path, f'Warning_{self.warning_count - 1}'),f'Warning_{self.warning_count - 1}'),)
        
                                send_thread.start()

                            self.warning_count += 1

                        self.take_photos(frame, time_now, self.current_folder_path)

                    else:
                        # Prepare for the next folder
                        self.current_folder_path = None  # Reset to None
                        
                cv2.imshow("F",frame)

                
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    if self.warning_count >1:
                        send_thread = threading.Thread(target=client.send_images, args=(os.path.join(path, f'Warning_{self.warning_count - 1}'),f'Warning_{self.warning_count - 1}'),)
                        send_thread.start()
                        break
        
            # Release the video capture object
            self.cap.release()

            # Closes all the frames
            cv2.destroyAllWindows()

            client.disconnect_server()  # Corrected method name

        except Exception as e:
            print(f"Error when trying to open camera: {e}")
            input("Press any key to quit")
            exit()

