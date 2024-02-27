# Safety-Helmet-For-Mining-Workers-using-IoT-and-Machine-Learning

This project was developed to help increase the safety of workers specifically in Mining Industry.
This invoilable skull cap is equipped with Various IoT sensors to sense any kind of danger.
This project is a innovation based on my "Women safety device" project.

Machine learning is implemented for prediction of temperature in mines for entered date and time.

Component list:
1. Arduino NANO
2. SIM800L (GSM)
3. NEO6M (GPSM)
4. Smoke sensor (MQ2)
5. Pulse sensor
6. Vibration sensor
7. Temperature and humidity sensor (DHT11)

IoT working:
When the worker feels he is in danger, he can choose to click the panic button which triggers the "Manual Mechanism" and sends the help message with live location to the manager's phone.
Or
If any sensor senses danger (for ex: if smoke sensor detects any harmful gas or fire) the "Automatic Mechanism" is triggered and message will be sent automatically without having to click the panic button.

Machine learning working:
When device is connected to PC and "Upload data" button is clicked in the Python tkinter gui created for this project, the temperature data will be recorded and stored in a csv file locally which will be used for training the model later.
When "Predict temperature" is clicked in the gui, we will have to enter date and time for which the model will predict the temperature.

Decision tree is used in this model.
