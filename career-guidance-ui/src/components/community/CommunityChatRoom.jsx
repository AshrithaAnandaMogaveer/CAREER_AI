import React, { useState, useEffect, useRef } from 'react';
import { X, Send, Image as ImageIcon, Smile, Users, Info } from 'lucide-react';
import { getStoredToken, getStoredUser } from '../../services/authService';

const CommunityChatRoom = ({ community, onClose }) => {
  const token = getStoredToken();
  const currentUser = getStoredUser();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [showMembers, setShowMembers] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchMessages();
    fetchMembers();
    // Poll for new messages every 5 seconds
    const interval = setInterval(fetchMessages, 5000);
    return () => clearInterval(interval);
  }, [community.id]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchMessages = async () => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/community/${community.id}/messages`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const data = await response.json();
      if (data.success) {
        setMessages(data.messages || []);
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMembers = async () => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/community/${community.id}/members`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const data = await response.json();
      if (data.success) {
        setMembers(data.members || []);
      }
    } catch (error) {
      console.error('Error fetching members:', error);
    }
  };

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        alert('Image size should be less than 5MB');
        return;
      }
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!newMessage.trim() && !selectedImage) return;

    setSending(true);
    try {
      const formData = new FormData();
      formData.append('community_id', community.id);
      formData.append('content', newMessage.trim());
      
      if (selectedImage) {
        formData.append('image', selectedImage);
      }

      const response = await fetch(
        'http://localhost:5000/api/community/message/send',
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        }
      );

      const data = await response.json();
      if (data.success) {
        setNewMessage('');
        removeImage();
        fetchMessages();
      } else {
        alert(data.message || 'Failed to send message');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Failed to send message. Please try again.');
    } finally {
      setSending(false);
    }
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';
    // Append 'Z' so the browser treats the backend UTC string as UTC,
    // then converts to the user's local timezone automatically.
    const raw = timestamp.endsWith('Z') ? timestamp : timestamp + 'Z';
    const date = new Date(raw);
    if (isNaN(date)) return '';

    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    const timeStr = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    if (diffDays >= 1) return date.toLocaleDateString() + ' ' + timeStr;
    return timeStr;
  };

  const isMyMessage = (message) => {
    return message.user_id === currentUser?.id;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div className="bg-surface rounded-lg w-full max-w-6xl h-[90vh] flex flex-col border border-gray-700">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
              {community.name.charAt(0).toUpperCase()}
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">{community.name}</h2>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowMembers(!showMembers)}
              className="p-2 text-gray-400 hover:text-white hover:bg-dark rounded-lg transition"
              title="View members"
            >
              <Users size={20} />
            </button>
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-white hover:bg-dark rounded-lg transition"
            >
              <X size={24} />
            </button>
          </div>
        </div>

        <div className="flex flex-1 overflow-hidden">
          {/* Messages Area */}
          <div className="flex-1 flex flex-col">
            {/* Messages List */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {loading ? (
                <div className="text-center py-8 text-gray-400">Loading messages...</div>
              ) : messages.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-gray-400 mb-2">No messages yet</p>
                  <p className="text-sm text-gray-500">Be the first to start the conversation!</p>
                </div>
              ) : (
                messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${isMyMessage(message) ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-[70%] ${isMyMessage(message) ? 'items-end' : 'items-start'} flex flex-col`}>
                      {!isMyMessage(message) && (
                        <div className="flex items-center gap-2 mb-1">
                          <div className="w-6 h-6 bg-gradient-to-br from-teal-500 to-purple-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
                            {message.user_name?.charAt(0).toUpperCase() || 'U'}
                          </div>
                          <span className="text-xs text-gray-400">{message.user_name}</span>
                        </div>
                      )}
                      <div
                        className={`rounded-lg p-3 ${
                          isMyMessage(message)
                            ? 'bg-teal-500 text-white'
                            : 'bg-dark text-gray-200'
                        }`}
                      >
                        {message.image_url && (
                          <img
                            src={`http://localhost:5000${message.image_url}`}
                            alt="Shared"
                            className="rounded-lg mb-2 max-w-full h-auto max-h-64 object-cover"
                            onError={(e) => { e.target.style.display = 'none'; }}
                          />
                        )}
                        {message.content && (
                          <p className="whitespace-pre-wrap break-words">{message.content}</p>
                        )}
                      </div>
                      <span className="text-xs text-gray-500 mt-1">
                        {formatTimestamp(message.created_at)}
                      </span>
                    </div>
                  </div>
                ))
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Image Preview */}
            {imagePreview && (
              <div className="px-4 pb-2">
                <div className="relative inline-block">
                  <img
                    src={imagePreview}
                    alt="Preview"
                    className="h-20 w-20 object-cover rounded-lg border border-gray-600"
                  />
                  <button
                    onClick={removeImage}
                    className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
                  >
                    <X size={14} />
                  </button>
                </div>
              </div>
            )}

            {/* Message Input */}
            <form onSubmit={handleSendMessage} className="p-4 border-t border-gray-700">
              <div className="flex items-end gap-2">
                <input
                  type="file"
                  ref={fileInputRef}
                  accept="image/*"
                  onChange={handleImageSelect}
                  className="hidden"
                />
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="p-3 text-gray-400 hover:text-teal-400 hover:bg-dark rounded-lg transition"
                  title="Attach image"
                >
                  <ImageIcon size={20} />
                </button>
                <div className="flex-1 relative">
                  <textarea
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSendMessage(e);
                      }
                    }}
                    placeholder="Type your message... (Shift+Enter for new line)"
                    className="w-full px-4 py-3 bg-white border border-gray-600 rounded-lg text-gray-900 placeholder-gray-500 focus:border-teal-500 focus:outline-none resize-none"
                    rows="2"
                  />
                </div>
                <button
                  type="submit"
                  disabled={sending || (!newMessage.trim() && !selectedImage)}
                  className="p-3 bg-teal-500 text-white rounded-lg hover:bg-teal-600 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send size={20} />
                </button>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Press Enter to send • Shift+Enter for new line • Max image size: 5MB
              </p>
            </form>
          </div>

          {/* Members Sidebar */}
          {showMembers && (
            <div className="w-64 border-l border-gray-700 p-4 overflow-y-auto">
              <h3 className="text-lg font-bold text-white mb-4">Members ({members.length})</h3>
              <div className="space-y-2">
                {members.map((member) => (
                  <div
                    key={member.user_id}
                    className="flex items-center gap-3 p-2 rounded-lg hover:bg-dark transition"
                  >
                    <div className="w-8 h-8 bg-gradient-to-br from-teal-500 to-purple-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                      {member.user_name?.charAt(0).toUpperCase() || 'U'}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-white truncate">{member.user_name}</p>
                      <p className="text-xs text-gray-500 capitalize">{member.role?.toLowerCase()}</p>
                    </div>
                    {member.role === 'ADMIN' && (
                      <span className="px-2 py-0.5 bg-yellow-500/20 text-yellow-400 text-xs rounded">
                        Admin
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CommunityChatRoom;
