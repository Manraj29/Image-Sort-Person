import face_recognition
import os
import shutil
import cv2
import streamlit as st

st.set_page_config(page_title="Image Sorter", page_icon="📷", layout="centered", initial_sidebar_state="auto")
st.title("Image Sorter 📷")
st.write("This app will help you sort your images by copying them to a separate folder.")
st.error("Instructions \n\n1. Select multiple Images from any folder \n2. Enter your name then click on the Open Camera button to open the webcam.\n3. Press q to quit & press enter to save the image.\n 4. After saving the image, The sorted images will be stored in the images folder with your name as a folder.")
st.write("Please upload multiple images of jpg, jpeg, png format only.")
# upload multiple images of jpg, jpeg, png
uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)


name = st.text_input("Enter your name: ")

# save the images in the images folder
for uploaded_file in uploaded_files:
    if not os.path.exists("images"):
        os.makedirs("images")
    with open(os.path.join("images", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

if not uploaded_files:
    st.warning("Please upload images to continue.")

img_name = ""

if name:
    st.write("Hello", name)
    if st.button("Open Camera"):
        st.write("the webcam will open in 5 seconds, press q to quit & press enter to save the image")
        cv2.waitKey(2000)
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("Capturing Image")
        model = cv2.CascadeClassifier(r"haarcascade_frontalface_default.xml")
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            faces = model.detectMultiScale(frame)
            for x,y,width,height in faces:
                frame = cv2.rectangle(frame, (x,y), (x+width, y+height), (0,255,255), 2)
            cv2.imshow("Capturing Image", frame)
            k = cv2.waitKey(1)
            # if q is pressed then exit
            if k%256 == 113:
                print("Escape hit, closing...")
                print("Thanks for using!")
                break
            elif k%256 == 13:
                img_name = "{}.png".format(name)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                break

        user_img = face_recognition.load_image_file(img_name)
        user_face_encoding = face_recognition.face_encodings(user_img)[0]
        print(user_face_encoding)


        target_folder = "images"
        known_face_encodings = [user_face_encoding]

        matched_images = []

        for filename in os.listdir(target_folder):
            # Check if file is an image
            if filename.endswith((".jpg", ".png", ".jpeg")):
                image_path = os.path.join(target_folder, filename)
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)

                for face_encoding in face_encodings:
                    match = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    if match[0]:
                        matched_images.append(image_path)
                        break

        # Print or process matched images
        st.write("There are", len(matched_images), "images that match your face.")
        print("Matched images:", matched_images)

        # copy_images = st.text_input("Do you want to copy all your images to a separate folder? (y/n): ")
        # copy_images = input("Do you want to copy all your images to a separate folder? (y/n): ")
        # copy_images = st.radio("Do you want to copy all your images to a separate folder? (y/n): ", ("y", "n"))
        copy_images = "y"
        # if st.button("Sort Images"):
        st.write("Sorting images...")
        
        if copy_images.lower() in ("y"):
            # source_folder = os.getcwd()
            source_folder = "images"
            destination_folder = os.path.join(source_folder, name)
            os.makedirs(destination_folder, exist_ok=True)

            # Loop through matched images list
            for matched_image_path in matched_images:
                shutil.copy2(matched_image_path, os.path.join(destination_folder, os.path.basename(matched_image_path)))

            print("Images copied successfully!")
            st.success("Images copied successfully!")
            st.success("Thanks for using!")
            st.error("The images are stored in the folder named " + name)
            # display the images from the new folder
            for filename in os.listdir(destination_folder):
                st.image(os.path.join(destination_folder, filename), use_column_width=True)
                st.info(filename)

        else:
            print("hope you got all the names of the images you are in!")
            st.write("Hope you got all the names of the images you are in!")
            st.write("Thanks for using!")