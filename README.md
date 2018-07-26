# Chatbot 

This project is a collection of chatbots that are meant to be run in chatscript or ghost. Albot is the basic chatscript bot. AlbotEmo is meant to be run with the ChatScript_Client to control the Einstein robot from the Einstein repository. AlbotGhost and STEMbot are meant to be run in ghost but are still under development. 

## Chatscript Installation

In the Linux terminal, run the following: 

```
git clone https://github.com/bwilcox-1234/ChatScript
cd ChatScript
cd BINARIES
chmod a+x ./LinuxChatScript64
cd .. 
./BINARIES/LinuxChatScript64 local
``` 
This should run the chatscript demo bot, Harry.


## Running Albot in ChatScript 

```
git clone https://github.com/aro-ai-robots/Chatbot.git
``` 

Copy the Albot directory from Chatbot and paste it in ChatScript/RAWDATA. 

Additionally, copy filesAlbot.txt and paste it in ChatScript/RAWDATA. 

To run Albot: 

```
cd ChatScript
./BINARIES/LinuxChatScript64 local
``` 

Enter your username and then enter the command - :build Albot 

If you want to reset the conversation, use the command - :reset 

If you want to quit the converstaion, use the command - :quit 


## Running Albot with the Einstein robot head

Copy the Albot directory from Chatbot and paste it in ChatScript/RAWDATA. 

Additionally, copy filesAlbot.txt and paste it in ChatScript/RAWDATA. 

Make sure to build AlbotEmo: 

```
cd ChatScript
./BINARIES/LinuxChatScript64 local
```

Enter your username and then enter the command - :build AlbotEmo

Then, exit through the command - :quit and start the ChatScript server:

```
./BINARIES/LinuxChatScript64
```

On the raspberryPi that runs the Einstein, run the following commands:

```
cd Vision
python Main.py
```

On your laptop, open up a new termial and run the following commands.

```
cd Chatbot/ChatScriptClient
python3 AlbotClient.py
```

Enter the IP address from the raspberry pi and start talking to Albot Einstein
