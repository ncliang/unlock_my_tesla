# unlock_my_tesla
Script to be used in AWS lambda to unlock Tesla with an [AWS IoT Button](https://aws.amazon.com/iotbutton/).
Based on the idea of [tesla-unlock-lambda](https://bitbucket.org/mikeortman/tesla-unlock-lambda/), but rewritten in Python and improved with double-click feature.

### Features
* Click to unlock
* Double-click to pop-frunk
* Works even if vehicle is in deep-sleep

### How to use
1. Create AWS Lambda function. Choose the Python 3.7 runtim.
2. Upload a zip file containing both unlock_my_tesla.py and myTesla.py
3. Set the handler to be "unlock_my_tesla.lambda_handler"
4. Add environment variables TESLA_EMAIL and TESLA_PASS.
5. Configure AWS IoT button to call this Lambda function. I used the AWS IoT Button Dev app for this.
