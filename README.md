# FlaskReact-Music-Controller

------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Purpose and Usage

***This app let's you make rooms that your friends can join using the room code an be able to control the music that is playing. You can give them permission to play and pause the song and they can also vote to skip the song if enough votes are collected the song gets skipped. This app is meant to be used in something like a house party or a roadtrip since you can't hear the music from your browser.***

>*Note that some features might not work if you don't use an account with spotify premium*

------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Local Installation 

### Install the requierements 
### Make sure pip and npm are installed on your computer

*Windows:*

#### ```pip install -r requirements.txt```
#### ```npm install```

*Mac && Linux:* 

#### ```pip3 install -r requirements.txt```
#### ```npm install```

### Create the spotify application on the spotify developer dashboard
#### Then create a .env file inside of the /api folder with your variables *(use .env.exaple as a guide)*
#### Add 127.0.0.1:*{PORT}* to allowed hosts on the spotify app settings in the developer dashboard

### Finally Run The Backend with

#### ```npm run api```

### Then Run the Frontend with

#### ```npm start```

------------------------------------------------------------------------------------------------------------------------------------------------------------------
