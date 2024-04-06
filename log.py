from chatPDF import connection, ask_question

SourceId = -1

# Run the connection function
while True:
    SourceId = connection()
    if SourceId != -1 :
        break

# Chat with the bot
format = input("Enter the format: ")
log = input("Enter the log: ")
answer = ask_question(SourceId, format, log)

print(answer)


# Write to csv file

