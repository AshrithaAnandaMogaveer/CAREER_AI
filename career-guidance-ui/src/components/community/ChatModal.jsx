import React, { useState, useEffect, useRef } from 'react';
import { getStoredToken, getStoredUser } from '../../services/authService';

const ChatModal = ({ profile, onClose }) => {
  const token = getStoredToken();
  const user = getStoredUser();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [fetchingMessages, setFetchingMessages] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (profile?.id) {
      setMessages([]); // clear previous conversation when switching users
      fetchMessages();
    }
  }, [profile?.id]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchMessages = async () => {
    if (!profile?.id) return;
    setFetchingMessages(true);
    try {
      const response = await fetch(
        `http://localhost:5000/api/community/messages/user/${profile.id}`,
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      const data = await response.json();
      if (data.success) {
        setMessages(data.messages || []);
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    } finally {
      setFetchingMessages(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || sending) return;

    setSending(true);
    try {
      const response = await fetch('http://localhost:5000/api/community/messages', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ recipient_id: profile.id, content: newMessage })
      });

      const data = await response.json();
      if (data.success) {
        setNewMessage('');
        await fetchMessages(); // re-fetch full history to keep everything in sync
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div className="bg-surface rounded-lg max-w-2xl w-full h-[600px] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
              {profile.name?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div>
              <h3 className="text-white font-semibold">{profile.name}</h3>
              <p className="text-gray-400 text-sm">{profile.domain || 'Professional'}</p>
            </div>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white text-2xl">×</button>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {fetchingMessages ? (
            <div className="text-center py-12">
              <p className="text-gray-400">Loading conversation...</p>
            </div>
          ) : messages.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-400">No messages yet</p>
              <p className="text-gray-500 text-sm mt-1">Start the conversation!</p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.is_own ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] rounded-lg p-3 ${
                    message.is_own ? 'bg-teal-500 text-white' : 'bg-dark text-gray-300'
                  }`}
                >
                  {!message.is_own && (
                    <p className="text-xs text-gray-400 mb-1">{message.sender_name}</p>
                  )}
                  <p className="break-words">{message.content}</p>
                  <p className={`text-xs mt-1 ${message.is_own ? 'text-teal-100' : 'text-gray-500'}`}>
                    {new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <form onSubmit={handleSendMessage} className="p-4 border-t border-gray-700">
          <div className="flex gap-2">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 px-4 py-2 bg-white border border-gray-600 rounded-lg text-gray-900 focus:border-teal-500 focus:outline-none"
              disabled={sending}
            />
            <button
              type="submit"
              disabled={sending || !newMessage.trim()}
              className="px-6 py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600 transition disabled:opacity-50"
            >
              {sending ? '...' : 'Send'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatModal;
