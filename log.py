from chatPDF import connection, ask_log_parser
import csv
import re
import ast

SourceId = -1


class Log():

    def __init__(self, format, name):
        self.name = name    
        self.format = format
        self.header_items= re.findall(r'<(.*?)>', self.format)
        self.header_items.append("templete")

    # Connect to the chatPDF API
    def connection(self):
        while True:
            SourceId = connection()
            if SourceId != -1:
                self.SourceId = SourceId
                break
        print("Source ID:", SourceId)

    # Chat with the bot
    def ask_question(self, log):
        while True:
            answer = ask_log_parser(self.SourceId, self.format, log)
            try:
                answer = ast.literal_eval(answer)
                return answer
            except ValueError as e:
                continue

    # Write the title of csv file
    def write_csv_title(self):
        with open(self.name+'.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.header_items)

    # Write the data of csv file
    def write_csv_content(self, log):
        while True:
            answer = self.ask_question(log)
            print("answer is:", answer)
            # oepn the csv file and write the structured log data
            with open(self.name+'.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                templete = answer[0]
                row_data = []

                for header_item in self.header_items:
                    if header_item in answer[1]:
                        output = ""
                        for i, item in enumerate(answer[1][header_item]):
                            if i < len(answer[1][header_item]) - 1:
                                output += item + ", "
                            else:
                                output += item
                        row_data.append(output)
                    else :
                        row_data.append(" ")
                # add the templete to the row data
                row_data.append(templete)
                # write the row data to the csv file
                writer.writerow(row_data)

            # if the data is wrong, continue to ask the question
            # Using the GPT API as a supervisor to verify if the data is correct.
            break

        print("CSV 文件已創建。")
    
print("Enter the name of log message:")
Logname = input()
print("Enter the format of log message:")   
Logformat = input()   

log = Log(Logformat, Logname)
log.connection()
print("Enter the log message:")
log_message = input()
log.write_csv_title()
log.write_csv_content(log_message)

