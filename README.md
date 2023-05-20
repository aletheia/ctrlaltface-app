# CtrlAltFace App

## Description
CtrlAltFace is an application designed to use the DLIB face recognition library for bunker access in the CtrlAltMuseum. This application merges the power of face recognition technology with the uniqueness of museum experiences, enhancing security while creating an immersive visitor journey.

## Installation
1. Clone this repository to your local machine using `https://github.com/aletheia/ctrlaltface-app.git`.
2. Navigate to the project directory.
3. Install the required dependencies with `pip install requirements.txt`.
4. Start the application with `python app/main.py`.

## Usage
Once the app is running, you can register faces for bunker access by providing photos into the 'faces' folder. These will be used by the DLIB face recognition to allow or deny access. 

When a visitor approaches the bunker, the app will attempt to recognize the face. If the face is recognized and has been granted access, the bunker will open because a REST call to the shelly device is sent.. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 

## License
This project is licensed under the MIT License - see the LICENSE file for more details.

## References

<https://sefiks.com/2020/07/11/face-recognition-with-dlib-in-python/>

<https://www.youtube.com/watch?v=bvCE4EmrUOI>

<https://pyimagesearch.com/2021/04/19/face-detection-with-dlib-hog-and-cnn/>
