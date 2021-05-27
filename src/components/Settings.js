import React from "react";
import { Grid, Button } from "@material-ui/core";
import CreateRoomPage from "./CreateRoomPage";

const Settings = ({ votesToSkip, guestCanPause, roomCode, setShowSettings }) => {
  return (
    <Grid container spacing={1} align="center">
      <Grid item xs={12}>
        <CreateRoomPage
          update={true}
          _votesToSkip={votesToSkip}
          _guestCanPause={guestCanPause}
          roomCode={roomCode}
        />
      </Grid>
      <Grid item xs={12}>
        <Button
          variant="contained"
          color="secondary"
          onClick={() => setShowSettings(false)}
        >
          Close
        </Button>
      </Grid>
    </Grid>
  );
};

export default Settings;
