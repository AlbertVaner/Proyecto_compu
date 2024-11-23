import cv2
import mediapipe as mp
import serial
import time

# Inicializar MediaPipe Hands y OpenCV
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Captura de video
cap = cv2.VideoCapture(0)

baud_rate = 9600
arduino_port = "COM5"
timeout = 1

command_sent = {'control': False, 'control2': False, 'control3': False, 'control4': False, 'control5': False}  # Diccionario para rastrear el estado de cada control
last_command_time = 0  

command_delay = 0.5

try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=timeout)
    print(f"Conectado a {arduino_port}")
    time.sleep(2)
except Exception as e:
    print(f"Error al conectar con Arduino: {e}")

try:
    while True:
        
        ret, frame = cap.read()

        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        
        results = hands.process(rgb_frame)

        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                
                p1 = p2 = Pm = Mm = pa = pa1 = Pme = Pme1 = Ppul = PpulM = 0

                for id, landmark in enumerate(hand_landmarks.landmark):
                    if id == 5:
                        p1 = landmark.y
                    if id == 8:
                        p2 = landmark.y
                    if id == 12:
                        Pm = landmark.y
                    if id == 9:
                        Mm = landmark.y
                    if id == 16:
                        pa = landmark.y
                    if id == 13:
                        pa1 = landmark.y
                    if id == 20:
                        Pme = landmark.y
                    if id == 17:
                        Pme1 = landmark.y
                    if id == 4:
                        Ppul = landmark.y
                    if id == 1:
                        PpulM = landmark.y

                
                control = p1 - p2
                control2 = Mm - Pm
                control3 = pa1 - pa
                control4 = Pme1 - Pme
                Control5 = PpulM - Ppul

                
                current_time = time.time()
                if current_time - last_command_time < command_delay:
                    continue  

                

                # Control 1
                if control < 0.03 and not command_sent['control']:
                    print("Condición de control1 cumplida, enviando '1'...")
                    arduino.write(b'1')  # Enviar un '1' al Arduino
                    command_sent['control'] = True  # Marcar que ya se envió el comando
                    last_command_time = current_time

                elif control >= 0.07:
                    if command_sent['control']:
                        print("Control1 > 0.05, enviando '0'...")
                        arduino.write(b"0")  # Enviar un '0' al Arduino
                        command_sent['control'] = False  # Reiniciar el estado
                        last_command_time = current_time

                # Control 2
                if control2 < 0.03 and not command_sent['control2']:
                    print("Condición de control2 cumplida, enviando '2'...")
                    arduino.write(b'2')  # Enviar un '2' al Arduino
                    command_sent['control2'] = True
                    last_command_time = current_time

                elif control2 >= 0.07:
                    if command_sent['control2']:
                        print("Control2 > 0.05, enviando '0'...")
                        arduino.write(b"0")
                        command_sent['control2'] = False
                        last_command_time = current_time

                # Control 3
                if control3 < 0.03 and not command_sent['control3']:
                    print("Condición de control3 cumplida, enviando '3'...")
                    arduino.write(b'3')  # Enviar un '3' al Arduino
                    command_sent['control3'] = True
                    last_command_time = current_time

                elif control3 >= 0.07:
                    if command_sent['control3']:
                        print("Control3 > 0.05, enviando '0'...")
                        arduino.write(b"0")
                        command_sent['control3'] = False
                        last_command_time = current_time

                # Control 4
                if control4 < 0.03 and not command_sent['control4']:
                    print("Condición de control4 cumplida, enviando '4'...")
                    arduino.write(b'4')  
                    command_sent['control4'] = True
                    last_command_time = current_time

                elif control4 >= 0.07:
                    if command_sent['control4']:
                        print("Control4 > 0.05, enviando '0'...")
                        arduino.write(b"0")
                        command_sent['control4'] = False
                        last_command_time = current_time

                # Control 5
                if Control5 < 0.03 and not command_sent['control5']:
                    print("Condición de control5 cumplida, enviando '5'...")
                    arduino.write(b'5')  #
                    command_sent['control5'] = True
                    last_command_time = current_time

                elif Control5 >= 0.07:
                    if command_sent['control5']:
                        print("Control5 > 0.05, enviando '0'...")
                        arduino.write(b"0")
                        command_sent['control5'] = False
                        last_command_time = current_time

       
        cv2.imshow("Hand Tracking", frame)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    
    cap.release()
    arduino.close()
    cv2.destroyAllWindows()
    print("Conexión cerrada")
