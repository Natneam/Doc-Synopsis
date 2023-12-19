import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperclip, faPaperPlane, faSpinner } from "@fortawesome/free-solid-svg-icons";
import SERVER_URL from "../config"
import toast from "react-hot-toast";
import botImg from "../assets/bot.png";

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
        toast.error("Summarization failed. Please try again.");
        setSummarizeLoading(false);
      }
    } catch (error) {
      toast.error("Summarization failed. Please try again.");
      setSummarizeLoading(false);
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
        toast.error("Answering failed. Please try again.");
        setSendMessageLoading(false);
      }
    } catch (error) {
      toast.error("Answering failed. Please try again.");
      setSendMessageLoading(false);
    }
  };

  const renderMessage = (message, isUser, index) => (
    <div className={`message ${isUser ? "user" : "bot"}`} key={index}>
      {message.split('\n\n').map((line, lineIndex) => (
        <React.Fragment key={lineIndex}>
          {line}
          {lineIndex !== message.split('\n\n').length - 1 && <br />}
          <br />
        </React.Fragment>
      ))}
    </div>
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
        toast.success("File uploaded successfully.");
      } else {
        toast.error("File upload failed. Please try again.");
      }
    } catch (error) {
      toast.error("File upload failed. Please try again.");
    }
  };

  return (
    <>
      <div className="title">
        ByteGenie FullStack Developer Test <span>By Natneam</span>
      </div>
      <div className="chat-box">
        <div className="message-list">
          {messages.length === 0 && (<div className="no-conversation"><img src={botImg} alt="No messages available" className="bot-img"/>Hello! I am ByteGenie. I can answer your questions about the uploaded document. Please upload a document and ask me a question.</div>)}
          {messages.length > 0 && messages.map((message, index) =>
            renderMessage(message.message, message.isUser, index)
          )}
        </div>
        <div className="info-wrapper">
          <div className="file-name-indicator">{selectedFileName === "" ? "Text_segments.csv has been pre-uploaded. To update or change it, please upload a new file." : selectedFileName}</div>
          <button className="summarize-button" onClick={summarizeDoc}>
            {summarizeLoading ? <FontAwesomeIcon icon={faSpinner} className="spinner" /> : "Summarize"}
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
            {sendMessageLoading ? <FontAwesomeIcon icon={faSpinner} className="spinner" /> : <FontAwesomeIcon icon={faPaperPlane} />}
          </button>
        </div>
      </div>
    </>
  );
};

export default ChatBox;
