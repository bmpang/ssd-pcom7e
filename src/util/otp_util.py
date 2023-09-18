from secrets import randbelow

# from smtplib import SMTP


# This function creates a 6 character string of digits, 0-10, to use as an otp
def generate_otp():
    otp = str(randbelow(10))

    for i in range(5):
        otp += str(randbelow(10))

    return otp


# This function sends an email containing a temporary OTP to the user's registed account
def send_email(email, subject, message):
    print(message)

    # It requires usage of an api key for a valid gmail account, so we have commented out
    # the email functionality and stub it by directly printing the message body


#   # Create a SMTP connection.
#   connection = SMTP('smtp.gmail.com', 587)
#   connection.ehlo()
#   # Start a TLS connection.
#   connection.starttls()
#   connection.ehlo()
#   # Login to the account.
#   connection.login('BLANK', 'BLANK')
#   # Send the email.
#   connection.sendmail('BLANK', email,
#                      'Subject: {0}\n\n{1}'.format(subject, message))
#   # Close the connection.
#   connection.close()


# Create and return an otp to validate against user input. Send that otp to the user's email.
def send_otp_to_email(email):
    otp = generate_otp()

    # Send the OTP to the email address.
    send_email(email, "OTP Password", "Your OTP is: {0}".format(otp))

    # Return the OTP.
    return otp
