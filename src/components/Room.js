import React, { useState, useEffect } from "react";
import { useHistory, useRouteMatch } from "react-router-dom";
import { Grid, Button, Typography } from "@material-ui/core";
import Settings from "./Settings";
import MediaPlayer from "./MediaPlayer";

const Room = ({ leaveRoomCallback }) => {
  const [guestCanPause, setGuestCanPause] = useState(true);
  const [votesToSkip, setVotesToSkip] = useState(2);
  const [isHost, setIsHost] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [song, setSong] = useState({});
  // const [isSpotifyAuthenticated, setSpotifyAuthenticated] = useState(false);
  const history = useHistory();
  const match = useRouteMatch();
  const roomCode = match.params.roomCode;

  useEffect(() => {
    const interval = setInterval(() => getCurrentSong(), 1000);
    return () => clearInterval(interval);
  }, [song]);

  const getRoomDetails = async () => {
    const res = await fetch(`/api/get-room?code=${roomCode}`);
    if (!res.ok) {
      leaveRoomCallback();
      history.push("/");
    }

    const data = await res.json();

    setVotesToSkip(data.votes_to_skip);
    setGuestCanPause(data.guest_can_pause);
    setIsHost(data.is_host);
    if (isHost) {
      authenticateSpotify();
    }
  };

  const leaveButtonPressed = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };

    await fetch("/api/leave-room", requestOptions);

    leaveRoomCallback();
    history.push("/");
  };

  const authenticateSpotify = async () => {
    const res = await fetch("/spotify/is-authenticated");
    const data = await res.json();

    // setSpotifyAuthenticated(data.status);
    if (!data.status) {
      const res = await fetch("/spotify/get-auth-url");
      const data = await res.json();

      window.location.replace(data.url);
    }
  };

  const renderSettingsButton = () => {
    return (
      <Grid item xs={12}>
        <Button
          variant="contained"
          color="primary"
          onClick={() => setShowSettings(true)}
        >
          Settings
        </Button>
      </Grid>
    );
  };

  const getCurrentSong = async () => {
    const res = await fetch("/spotify/current-song");
    if (!res.ok) {
      return {};
    } else {
      const data = await res.json();
      setSong(data);
    }
  };

  getRoomDetails();

  if (showSettings) {
    return (
      <Settings
        votesToSkip={votesToSkip}
        guestCanPause={guestCanPause}
        roomCode={roomCode}
        setShowSettings={setShowSettings}
      />
    );
  } else {
    return (
      <Grid container spacing={1} align="center">
        <Grid item xs={12}>
          <Typography variant="h4" component="h4">
            Code: {roomCode}
          </Typography>
        </Grid>
        <MediaPlayer {...song} />
        {isHost && renderSettingsButton()}
        <Grid item xs={12}>
          <Button
            color="secondary"
            variant="contained"
            onClick={leaveButtonPressed}
          >
            Leave Room
          </Button>
        </Grid>
      </Grid>
    );
  }
};

export default Room;
