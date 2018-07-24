# Simple chat client to communicate with chat script server
from optparse import OptionParser
import socket
import sys
import speech_recognition as sr
import time
import os

#creating voice recognizer and microphone
recognizer = sr.Recognizer()

#use sr.Microphone.list_microphone_names() to find the device index
#if device_index arg is omitted, it will use the default microphone
microphone = sr.Microphone()

#When the code runs, it will ask for the IP address of the server you want to connect to.
ip_address = input("Enter the IP address of the server: ")

# starting socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ip_address, 4000)
sock.connect(server_address)

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def sendAndReceiveChatScript(msgToSend, server='127.0.0.1', port=1024, timeout=10):
    try:
        # Connect, send, receive and close socket. Connections are not persistent
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)  # timeout in secs
        s.connect((server, port))
        s.sendall(msgToSend)
        msg = ''
        while True:
            chunk = s.recv(1024)
            if chunk == b'':
                break
            msg = msg + chunk.decode("utf-8")
        s.close()
        return msg
    except:
        return None


if __name__ == '__main__':
    server = "127.0.0.1"
    port = 1024
    botname = ""

    # Setup the command line arguments.
    optp = OptionParser()

    # user name to login to chat script as
    optp.add_option("-u", dest="user", help="user id, required")
    # botname
    optp.add_option("-b", dest="botname", help="which bot to talk to, if not specified, will use default bot")
    # server
    optp.add_option("-s", dest="server", help="chat server host name (default is " + str(server) + ")")
    # port
    optp.add_option("-p", dest="port", help="chat server listen port (default is " + str(port) + ")")

    opts, args = optp.parse_args()

    if opts.user is None:
        optp.print_help()
        sys.exit(1)
    user = opts.user

    if opts.botname is not None:
        botname = opts.botname

    if opts.server is not None:
        server = opts.server

    if opts.port is not None:
        port = int(opts.port)

    intro = "Hi " + user + ", I am Albot Einstein. "
    print(intro)
    os.system('echo %s | festival --tts' % intro) 

    while True:
        response = recognize_speech_from_mic(recognizer,microphone)
        s = response["transcription"]
        #s = input("[" + user + "]" + ">: ").lower().strip()
        if not response["success"]:
            print("I didn't catch that. What did you say?\n")
        if response["error"]:
            print("ERROR: {}".format(response["error"]))

        # Ensure empty strings are padded with atleast one space before sending to the
        # server, as per the required protocol
        if s == "":
            s = " "
        # Send this to the server and print the response
        # Put in null terminations as required
        msg = u'%s\u0000%s\u0000%s\u0000' % (user, botname, s)
        msg = msg.encode('ascii')
        botResp = sendAndReceiveChatScript(msg, server=server, port=port)
        
        if botResp is None:
            print("Error communicating with Chat Server")
            break  # Stop on any error
        else:
            try:
                print("You said: {}".format(s))
                print("[Albot]: " + botResp)
                sock.send('6'.encode())
                botResp = botResp.replace("'", "")
                os.system('echo %s | festival --tts' % botResp)
                sock.send('7'.encode())
            except:
                botResp = "I cannot understand. Try speaking more clearly."
                print("[Albot]: " + botResp)
                sock.send('6'.encode())
                os.system('echo %s | festival --tts' % botResp) 
                sock.send('7'.encode())
