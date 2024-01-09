import win32com.client
import pandas as pd
from datetime import datetime, timedelta


def do_get_accounts():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    return [acc.DisplayName for acc in outlook.Accounts]

def do_read_emails(account):
    # Connect to Outlook and access shared mailbox
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    #inbox = outlook.Folders("soporteglobalcva@gruposantander.com").Folders("Inbox")
    #inbox = outlook.Folders("soporteglobalcva@gruposantander.com").GetDefaultFolder("6")
    #inbox = outlook.Folders(account).Folders("Inbox")

    # get the account object
    for account_name in outlook.Accounts:
        if account in account_name.DisplayName:
            account_obj = account_name
            break

    # get the default inbox folder for the account
    inbox = account_obj.DeliveryStore.GetDefaultFolder(6)

    # Get all emails in the inbox folder
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)

    # The way the datetime is formatted DOES matter; You can't add seconds here.
    num_days = 1
    lastDayDateTime = datetime.now() - timedelta(days=int(num_days))
    messages = messages.Restrict("[ReceivedTime] >= '" + lastDayDateTime.strftime('%m/%d/%Y %H:%M %p') + "'")

    # Create an empty list to hold email information
    emails = []

    # Loop through all emails and retrieve information
    i = 1
    for message in messages:
        print(i)
        if message.Class == 43:


            email_info = {
                "Received": message.ReceivedTime.strftime('%y-%m-%d %H:%M'),
                "Sent On": message.Senton.strftime('%y-%m-%d %H:%M'),
                "Subject": message.Subject,
                "Sender Type": message.SenderEmailType,
                "Company": message.Sender.GetExchangeUser().CompanyName if message.SenderEmailType == "EX" else "",
                "Dept": message.Sender.GetExchangeUser().Department if message.SenderEmailType == "EX" else "",
                "Alias": message.Sender.GetExchangeUser().Alias if message.SenderEmailType == "EX" else "",
                "From": message.Sender.GetExchangeUser().Name if message.SenderEmailType == "EX" else message.SenderName,
                "From Address": message.Sender.GetExchangeUser().PrimarySmtpAddress if message.SenderEmailType == "EX" else message.SenderEmailAddress,
                "To": message.To,
                "Category": message.Categories,
                "Priority": message.Importance,
                "Read Status": message.UnRead,
                "Reply": message.MessageClass == "IPM.Note.Reply",
                "Num Attachments": sum(1 for attachment in message.Attachments if attachment.FileName.lower().endswith(('.dat', '.xlsx', '.zip'))),
                "Email ID": message.EntryID,
                "Conversation ID": message.ConversationID
            }
            emails.append(email_info)
        i = i + 1
    # Create a pandas dataframe from the email information list
    df = pd.DataFrame(emails)

    print(emails)
    # Print the dataframe
    return df



