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
        a.  Go to URL : https://api.slack.com/apps
        b. select your app 
        c. In App Setting page : Go to [Basic Information] section and set 
                    SLACK_CLIENT_ID =[Client ID]
                    SLACK_CLIENT_SECRET=[Client Secret] 
                    SLACK_VERIFICATION_TOKEN=[Verification Token]
        d. Create a new Bot User using []                     
                    SLACK_BOT_USER_TOKEN=[]  
  
