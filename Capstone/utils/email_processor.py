import win32com.client
import pythoncom


def send_email(email_recipients, email_subject, email_html='', email_body=''):
#start outlook application 
    pythoncom.CoInitialize()

    try:
        outlook = win32com.client.Dispatch('outlook.application')

        #create outlook email object 
        mail = outlook.CreateItem(0)

        # Set recipients
        mail.To = ";".join(email_recipients)

        mail.Subject = email_subject

        # Set HTML body
        mail.HTMLBody = email_html

        # Set plain text body (optional)
        mail.Body = email_body

        # Send the email
        mail.Send()
    finally:
        pythoncom.CoUninitialize()


def compose_email(email_recipient, email_type, **kwargs):
    emails = [email_recipient.email]
    if email_type == 'payment_success':
        subject = 'Payment Successful!'
        body = f'Your payment of {email_recipient.unit.rent} was successful!'

        send_email(emails, subject, email_body=body)

    elif email_type == 'landlord_receipt':
        subject = "You've received a rent payment!"
        body = f'You have received a payment on the unit at {kwargs["tenant"].unit.address} has received a payment to the amount of {kwargs["tenant"].unit.rent}. The amount has been transferred to your account.'

        send_email(emails, subject, email_body=body)
    
    elif email_type == 'rent_reminder':
        subject = "You have an upcoming rent payment!"
        body = f'You have an upcoming rent payment of {email_recipient.unit.rent} due on {kwargs["due_date"]}. Be sure to pay your balance before the due date to avoid incurring penalties.'

        send_email(emails, subject, email_body=body)