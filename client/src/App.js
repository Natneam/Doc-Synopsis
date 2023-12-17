import "./App.css";
import React, { useState, useEffect } from "react";
import ChatBox from "./components/chatBox";
import { Toaster } from "react-hot-toast";

function App() {
  return (
    <div>
      <ChatBox />
      <Toaster position="bottom-right" reverseOrder={false} />
    </div>
  );
}

export default App;
