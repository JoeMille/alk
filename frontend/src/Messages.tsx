import { useState, useEffect } from 'react';
import axios from 'axios';

interface Message {
  id: number;
  text: string;
  author: string;
  created_at: string;
}

function Messages() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [newText, setNewText] = useState('');
  const [newAuthor, setNewAuthor] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/messages/');
      setMessages(response.data);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await axios.post('http://localhost:8000/api/messages/', {
        text: newText,
        author: newAuthor,
      });
      
      setNewText('');
      setNewAuthor('');
      
      fetchMessages();
    } catch (error) {
      console.error('Error creating message:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">ALkemy Messages</h1>
        
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Post a Message</h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Author
              </label>
              <input
                type="text"
                value={newAuthor}
                onChange={(e) => setNewAuthor(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Message
              </label>
              <textarea
                value={newText}
                onChange={(e) => setNewText(e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
            >
              {loading ? 'Posting...' : 'Post Message'}
            </button>
          </form>
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Messages</h2>
          {messages.length === 0 ? (
            <p className="text-gray-500">No messages yet. Be the first to post!</p>
          ) : (
            messages.map((message) => (
              <div key={message.id} className="bg-white rounded-lg shadow p-4">
                <div className="flex justify-between items-start mb-2">
                  <span className="font-semibold text-gray-900">{message.author}</span>
                  <span className="text-sm text-gray-500">
                    {new Date(message.created_at).toLocaleString()}
                  </span>
                </div>
                <p className="text-gray-700">{message.text}</p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default Messages;