# colabelsite
I have used following packages and these are required to run the code

1. django
2. djangorestframework
3. slackclient
4. slackeventsapi

instalation commands for above packages are below : 
1. pip3 install django
2. pip3 install djangorestframework
3. pip install slackclient
4. pip3 install slackeventsapi

How to Run the code ? 

 Step 1 :  Create a slack App and bot user and update autentication values :
 
 in settings.py we need to update following variables : 
        [SLACK_CLIENT_ID
        SLACK_CLIENT_SECRET
        SLACK_VERIFICATION_TOKEN
        SLACK_BOT_USER_TOKEN
        CSV_FILE_PATH]
 
        a.  Go to URL : https://api.slack.com/apps
        b. select your app 
        c. In App Setting page : Go to [Basic Information] section and set 
                    SLACK_CLIENT_ID =[Client ID]
                    SLACK_CLIENT_SECRET=[Client Secret] 
                    SLACK_VERIFICATION_TOKEN=[Verification Token]
        d. Create a new Bot User using [Bot Users] section                     
        
        e. Go to [OAuth & Permissions] section and copy [Bot User OAuth Access Token] value in [SLACK_BOT_USER_TOKEN]
                    SLACK_BOT_USER_TOKEN=[Bot User OAuth Access Token]   
  
        f. Update path of CSV file [CSV_FILE_PATH]. This is optional step as i have checked in DB 
           with preloaded CSV file. Plaese norte in CSV file i have add headeer with name  [Data]. The 
           csv file i have used can be found in [codechallange] folder. 


Step 2 : Run [ngrok http 8000] and note server ID generated. e.g. It will show some URL like [http://55fdbe22.ngrok.io ]
we need to update this URL in allowed [ALLOWED_HOSTS] variable in [settings.py]. Example : ALLOWED_HOSTS = ['55fdbe22.ngrok.io','127.0.0.1']


Step 3 : Run the server using [manage.py runserver] command. If you have not setup enviornment variable and attached py file to [python.exe] then
 you might need to run command like  [python manage.py runserver]
 

Step 4 : Subscribe to Slac event via [Event Subscriptions] section from your App setting page. In this section we need to do following 
    a. Enable Events : True 
    b. Request URL : [URL of nghook]/codechallenge/ . If we take  Step no 2 example then it will be [http://55fdbe22.ngrok.io/codechallenge/]
    c. [Subscribe to bot events] -> [message.channels] and [message.im]
    d. [Subscribe to workspace events] -> [message.channels]
    

Step 5: Enable [Interactive Components]    section from your App setting page. In this section we need to do following
    a. Interactivity : True
    b. Request URL : Same as Step 4.b
    c. Options Load URL( optional) : Same as Step 4.b
    
Step 6: Enable [Incoming Webhooks]    section from your App setting page. In this section we need to do following
    a. Activate Incoming Webhooks : True
    b. Save URL for sending messages. URL fot my work boook is[https://hooks.slack.com/services/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] 
    c. Sample Payload : {
    "attachments": [
        {
            "fallback": "any text",
            "text": "daisy",
            "image_url": "https://images.wagwalkingweb.com/media/articles/cat/daisy-poisoning-1/daisy-poisoning-1.jpg"
            
        }
    ]
}
     
     
Step 7.  Save your changes and deploy the application. 

Usage : 

1. You can use HTTP POST message using POSTMAN to send Label Information : 
Sample :  URL: https://hooks.slack.com/services/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
Payload : In below payload, "text" field contain actual label and image_url contain Image URL.  
{
    "attachments": [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "text": "daisy",
            "image_url": "https://images.wagwalkingweb.com/media/articles/cat/daisy-poisoning-1/daisy-poisoning-1.jpg"
            
        }
    ]
}


2. In the Actual Workboook https://app.slack.com/client/ . type "next". System will show you image and drop down to select label.


Test Cases can be run using : [manage.py test ./codechallenge/]  ( Given the time i would have written few more.            