import win32com.client 


#start outlook application 
outlook = win32com.client.Dispatch('outlook.application')

#create outlook email object 
mail = outlook.CreateItem(0)

# List of recipients of the emial in a list
to_recipients = ["andrew.macmaster@fiserv.com", "kirtana.ganesh@fiserv.com", "manan.patel@fiserv.com"]
cc_recipients = ["carla.moseleyholmes@fiserv.com"]

# Set recipients
mail.To = ";".join(to_recipients)
mail.CC = ";".join(cc_recipients)

mail.Subject = "Hello, this is a test"

# Set HTML body
mail.HTMLBody = "<h3>This is the body of the email</h3>"

# Set plain text body (optional)
mail.Body = "Your payments was submitted. Manan your debt is now 1000 USD, please pay before christmas!"

# Send the email
mail.Send()

