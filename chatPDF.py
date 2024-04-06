import requests
import re

# Connect to the chatPDF API
def connection ():

    # Set the source ID
    SourceId = -1

    # Get the file
    files = [
        ('file', ('file', open('Log_Paser_Concept.pdf', 'rb'), 'application/octet-stream'))
    ]

    # Set the headers
    headers = {
        'x-api-key': 'sec_A2KRWUa7gi4RER6agfHD8WxTnxV7FMFM',
    }

    # Upload the file
    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

    if response.status_code == 200:
        SourceId = response.json()['sourceId']
        print('Source ID:', response.json()['sourceId'])
        return SourceId
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
    
# Chat with the bot
def ask_question(SourceId, LogFormat, LogMessage):

    while(True):

        question =  (
            "the format of the log message is the format of the log message is " + 
            LogFormat + 
            "You will be provided with a log message delimited by backticks. " + 
            "Please extract the log template and dynamic variables from this log message."  +
            "for example for log message :  17/08/22 15:51:24 DEBUG BlockManager Putting block rdd_2_2 with replication took 0" +
            "you should output a list : ['<> <> <> Putting block <> with replication took <>',{ (name in the first <> of log format ex time): [17/08/22], (name in the second <> in log format): [15:51:24], (name in the third <> of log format): [BlockManager], (name in the forth <> of log format): [rdd_2_2,0]...}]" +
            "(importment:the output should just a list without any description beside the list)" +
            "Log message: " + 
            LogMessage
        )

        if SourceId == -1:
            print('Error: Source ID is not set')
            break

        headers = {
            'x-api-key': 'sec_A2KRWUa7gi4RER6agfHD8WxTnxV7FMFM',
            "Content-Type": "application/json",
        }

        data = {
            'sourceId': SourceId,
            'messages': [
                {
                    'role': "user",
                    'content': question,
                }
            ]
        }

        response = requests.post(
            'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

        if response.status_code == 200:
            print('Result:', response.json()['content'])
            answer = response.json()['content']
            return answer

        else:
            print('Status:', response.status_code)
            print('Error:', response.text)



