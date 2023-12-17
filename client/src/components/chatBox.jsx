import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperclip, faPaperPlane, faSpinner } from "@fortawesome/free-solid-svg-icons";
import SERVER_URL from "../config"

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState("");
  const [selectedFileName, setSelectedFileName] = useState("");
  const [summarizeLoading, setSummarizeLoading] = useState(false);
  const [sendMessageLoading, setSendMessageLoading] = useState(false);

  const summarizeDoc = async () => {
    if (summarizeLoading || sendMessageLoading) return;
    setSummarizeLoading(true);
    try {
      const response = await fetch(
        `${SERVER_URL}/summarize/${selectedFileName !== "" ? selectedFileName : "text_segments.csv"}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (response.ok) {
        const result = await response.json();
        setMessages((prevMessages) => [
          ...prevMessages,
          { message: result["summary"], isUser: false },
        ]);
        setSummarizeLoading(false);
      } else {
        console.error('Failed to summarize document');
        setSummarizeLoading(false);
      }
    } catch (error) {
      console.error('An error occurred during document summarization:', error);
    }
  };

  const sendMessage = async () => {
    if (summarizeLoading || sendMessageLoading || messageInput === "") return;

    if (messageInput.trim()) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { message: messageInput, isUser: true },
      ]);
      setMessageInput("");
    }

    setSendMessageLoading(true);

    // request to backend
    try {
      const response = await fetch(`${SERVER_URL}/answer/${selectedFileName !== "" ? selectedFileName : "text_segments.csv"}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: messageInput }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log(result["answer"]);
        setMessages((prevMessages) => [
          ...prevMessages,
          { message: result["answer"], isUser: false },
        ]);
        setSendMessageLoading(false);
      } else {
        console.log("Message sending failed");
        setSendMessageLoading(false);
      }
    } catch (error) {
      console.error("Error sending request:", error);
    }
  };

  const renderMessage = (message, isUser, index) => (
    <div className={`message ${isUser ? "user" : "bot"}`} key={index}>{message}</div>
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
      if (response.ok) {
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
            renderMessage(message.message, message.isUser, index)
          )}
        </div>
        <div className="info-wrapper">
          <div className="file-name-indicator">{selectedFileName === "" ? "Text_segments.csv has been pre-uploaded. To update or change it, please upload a new file." : selectedFileName}</div>
          <button className="summarize-button" onClick={summarizeDoc}>
            {summarizeLoading ? "Summarizing..." : "Summarize"}
          </button>
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
            {sendMessageLoading ? <FontAwesomeIcon icon={faSpinner} /> : <FontAwesomeIcon icon={faPaperPlane} />}
          </button>
        </div>
      </div>
    </>
  );
};

export default ChatBox;
