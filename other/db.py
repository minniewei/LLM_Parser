import param
from other.test import load_db

# Define the class cbfs (Conversational Bot with File Support)
class cbfs(param.Parameterized):

    chat_history = param.List([])
    answer = param.String("")
    db_query  = param.String("")
    db_response = param.List([])
    
    def __init__(self,  **params):
        super(cbfs, self).__init__( **params)
    
    def call_load_db(self):
        self.qa = load_db()
        self.clr_history()
        return 

    def convchain(self, query):

        # ERROR: The following line is causing an error in the app
        if not query:
            return 
        
        result = self.qa.invoke({"question": query, "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        self.db_query = result["generated_question"]
        self.db_response = result["source_documents"]
        self.answer = result['answer']

        print(result['answer'])

        return 
    
    def get_sources(self):
        if not self.db_response:
            return 
        print(self.db_response)
        return

    def clr_history(self):
        self.chat_history = []
        return 

my_cbfs = cbfs()
my_cbfs.call_load_db()
while True:
    word = input("Enter a question: ")
    if word == "exit":
        break
    my_cbfs.convchain(word)

    
