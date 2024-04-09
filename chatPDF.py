import requests

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
        return SourceId
    else:
        return False
    
# Ask the bot for the log parser
def ask_log_parser(SourceId, LogFormat, LogMessage):    
    question =  (
        "the format of the log message is the format of the log message is " + 
        LogFormat + 
        "You will be provided with a log message delimited by backticks. " + 
        "Please extract the log template and dynamic variables from this log message."  +
        "for example for log message : 2015-10-18 18:01:51,963 INFO [main] org.mortbay.log: jetty-6.1.26" +
        "you should output a list : ['<*> <*> <*> <*> <*> <*>: jetty-6.1.26',{ (name in the first <> of log format ex time): [\"2015-10-18\"], (name in the second <> in log format): [\"18:01:51,963\"], (name in the third <> of log format): [\"INFO\"], (name in the forth <> of log format): [\"rdd_2_2\",\"0\"]...}]" +
        "(importment:the output should just a list without any description beside the list。"  +
        "\"()\" in the json represents a variable, so do not output (name in the first <> of log format ex time) or variable with bracelet..." +
        "<*> represent the place for dynamic variable)" +
        "Log message: " + 
        LogMessage
    )
    return ask_question(SourceId, question)

# Ask the bot for the more details
def reaskQuestion(Source, question):
    ask_question(Source, question)

# Chat with the bot
def ask_question(SourceId, question):
    while(True):
        if SourceId == -1:
            return False

        headers = {
            # Provide for testing purposes
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
            answer = response.json()['content']
            return answer





