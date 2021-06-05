import React from "react";
import {
  Grid,
  Typography,
  Card,
  IconButton,
  LinearProgress,
} from "@material-ui/core";
import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import SkipNextIcon from "@material-ui/icons/SkipNext";
import PauseIcon from "@material-ui/icons/Pause";

const MediaPlayer = ({ image_url, title, artist, is_playing, time, duration, votes, votes_required }) => {
  const songProgress = (time / duration) * 100;

  const playSong = async () => {
    const requestOptions = {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'}
    }

    fetch("/spotify/play", requestOptions);
  }

  const pauseSong = async () => {
    const requestOptions = {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'}
    }

    fetch("/spotify/pause", requestOptions);
  }

  const skipSong = async () => {
    const requestOptions = {
      method: "POST",
      headers: {'Content-Type': 'application/json'}
    }

    fetch("/spotify/skip", requestOptions);
  }

  return (
    <Card>
      <Grid container alignItems="center">
        <Grid item align="center" xs={12} sm={4}>
          <img src={image_url} height="100%" width="100%" alt=""/>
        </Grid>
        <Grid item align="center" xs={12} sm={8}>
            <Typography component="h5" variant="h5">
                {title}
            </Typography>
            <Typography color="textSecondary" variant="subtitle1">
                {artist}
            </Typography>
            <div>
                <IconButton onClick={() => {is_playing ? pauseSong() : playSong()}}>
                    {is_playing ? <PauseIcon /> : <PlayArrowIcon />}
                </IconButton>
                <IconButton onClick={skipSong}>
                    <SkipNextIcon /> {votes} / {votes_required}
                </IconButton>
            </div>
        </Grid>
      </Grid>
      <LinearProgress variant="determinate" value={songProgress} />
    </Card>
  );
};

export default MediaPlayer;
