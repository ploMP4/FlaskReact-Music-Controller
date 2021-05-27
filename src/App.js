import React, { useEffect, useState } from "react";
import HomePage from "./components/HomePage";
import CreateRoomPage from "./components/CreateRoomPage";
import RoomJoinPage from "./components/RoomJoinPage";
import Room from "./components/Room";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";

function App() {
  const [roomCode, setRoomCode] = useState(null);

  useEffect(() => {
    const isInRoom = async () => {
      const res = await fetch("/api/user-in-room");
      const data = await res.json();

      if(res.ok) {
        setRoomCode(data.code);
      } 
    };

    isInRoom();
  });

  const clearRoomCode = () => {
    setRoomCode(null);
  }

  return (
    <Router>
      <Switch>
        <Route
          exact
          path="/"
          render={() => {
            return roomCode ? (
              <Redirect to={`/room/${roomCode}`} />
            ) : (
              <HomePage />
            );
          }}
        />
        <Route path="/create" component={CreateRoomPage} />
        <Route path="/join" component={RoomJoinPage} />
        <Route path="/room/:roomCode" render={() => <Room leaveRoomCallback={clearRoomCode}/>}/>
      </Switch>
    </Router>
  );
}

export default App;
