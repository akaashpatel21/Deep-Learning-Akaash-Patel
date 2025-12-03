import cv2

def find_available_cameras():
    """
    Scans for and lists available camera devices and their indices.
    """
    print("Searching for available cameras...")
    index = 0
    available_cameras = []
    
    # Scan indices 0 through 9
    while index < 10:
        # Try to open the camera at the current index
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            # If successful, it's a valid camera
            camera_name = f"Camera Index: {index}"
            available_cameras.append((index, camera_name))
            # Release the camera so it can be used by other applications
            cap.release()
        index += 1
        
    if not available_cameras:
        print("\nNo cameras found. Please ensure your webcam is connected and drivers are installed.")
    else:
        print("\nFound the following cameras:")
        for idx, name in available_cameras:
            print(f"- {name}")
        print("\nNote: Your iPhone (Continuity Camera) and built-in FaceTime HD Camera will be listed here.")
        print("Try using the index that is NOT your iPhone in your app.py file.")

if __name__ == "__main__":
    find_available_cameras()
