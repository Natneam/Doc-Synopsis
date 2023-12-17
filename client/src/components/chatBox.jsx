import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperclip, faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import SERVER_URL from "../config"

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState("");
  const [selectedFileName, setSelectedFileName] = useState("");

  const sendMessage = () => {
    if (messageInput.trim()) {
      setMessages([...messages, { message: messageInput, isUser: true }]);
      setMessageInput("");
    }
  };

  const renderMessage = (message, isUser) => (
    <div className={`message ${isUser ? "user" : "bot"}`}>{message}</div>
  );

  const handleChange = async (event) => {
    const newFileName = event.target.files[0]?.name || "text_segments.csv";

    const formData = new FormData();
    formData.append("file", event.target.files[0]);

    try {
      const response = await fetch(`${SERVER_URL}/upload/${newFileName}`, {
        method: "POST",
        body: formData,
      });

      // Handle the response as needed
      const result = await response.json();
      if (result.success) {
        setSelectedFileName(newFileName);
        console.log("File uploaded successfully");
      } else {
        console.log("File upload failed");
      }
    } catch (error) {
      console.error("Error sending request:", error);
    }
  };

  return (
    <>
      <div className="title">
        ByteGenie FullStack Developer Test <span>By Natneam</span>
      </div>
      <div className="chat-box">
        <div className="message-list">
          {messages.map((message, index) =>
            renderMessage(message.message, message.isUser)
          )}
        </div>
        <div className="info-wrapper">
          <div className="file-name-indicator">{selectedFileName === "" ? "Text_segments.csv has been pre-uploaded. To update or change it, please upload a new file." : selectedFileName}</div>
          <button className="summarize-button">Summarize</button>
        </div>
        <div className="chat-input">
          <div className="file-upload-icon">
            <label htmlFor="file-input">
              <FontAwesomeIcon
                icon={faPaperclip}
                fontSize="25px"
                className="file-icon"
              />
            </label>
            <input
              type="file"
              accept=".pdf, .csv"
              className="hidden-input"
              id="file-input"
              onChange={handleChange}
            />
          </div>
          <input
            type="text"
            placeholder="Enter your question here..."
            value={messageInput}
            onChange={(e) => setMessageInput(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
          />
          <button onClick={sendMessage}>
            <FontAwesomeIcon icon={faPaperPlane} />
          </button>
        </div>
      </div>
    </>
  );
};

export default ChatBox;
