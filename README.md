
# Test Portal using Face Recognition

This project is an online test portal that utilizes face recognition technology to authenticate users and provide a secure testing environment. The system identifies and verifies the test takers' faces to ensure the authenticity of the participants.


## Features

- Face recognition-based user authentication
- Secure test environment
- User registration and management
- Test creation and management
- Test-taking functionality
- Scoring and result generation

## Technologies Used

- Python
- Django (Python web framework)
- OpenCV (Open Source Computer Vision Library)
- CNN (Machine learning algorithm)
- HTML, CSS, JavaScript (Front-end development)

## Screenshots

![Login Page](https://github.com/akanksha2911/FiyePr/blob/master/ss/login.png?raw=true)

![Face Recognition Page](https://github.com/akanksha2911/FiyePr/blob/master/ss/live%20stream.png?raw=true)

![Login Failed Alert](https://github.com/akanksha2911/FiyePr/blob/master/ss/alert_login.png?raw=true)

![Home Page](https://github.com/akanksha2911/FiyePr/blob/master/ss/home%20page%20.png?raw=true)

![Quiz Instructions](https://github.com/akanksha2911/FiyePr/blob/master/ss/quiz%20alert.png?raw=true)

![Quiz Questions](https://github.com/akanksha2911/FiyePr/blob/master/ss/quiz%20page.png?raw=true)
## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/akanksha2911/FiyePr.git

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

3. Change the path of files as relative path is not specified.

3. Set up the database:

   Create your own dataset using generate.py for each face. The    generate.py will create folder of all faces which will be used for training the model. Update the ResultsMap.pkl and classifier_model.h5 file based on your trained dataset.

4. Run the application:

   ```bash
   cd Quiz2
   python manage.py runserver

5. Access the application in your browser at http://127.0.0.1:8000/.


## Usage Steps

1. Log in using your credentials.
3. The system will use face recognition to verify your identity.
3. Create a new test or select an existing one.
4. Start the test and follow the instructions.
5. Submit the test, and your score will be displayed.
6. Being a superuser you can even add quiz, questions.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

