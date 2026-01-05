import { useState, useEffect } from 'react';
import api from '../../services/api';

interface Group {
  id: number;
  name: string;
  description: string;
  is_private: boolean;
  created_by_username: string;
  member_count: number;
  thread_count: number;
}

function GroupsList() {
  const [groups, setGroups] = useState<Group[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchGroups();
  }, []);

  const fetchGroups = async () => {
    try {
      const response = await api.get('/groups/');
      setGroups(response.data.results || response.data);  
    } catch (err) {
      if (err.response?.status === 401) {

        window.location.href = '/login';
      } else {
        setError('Failed to load groups');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleJoinGroup = async (groupId: number) => {
    try {
      fetchGroups();
      
    } catch (err) {
      if (err.response?.data?.error) {
        alert(err.response.data.error);  
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading groups...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-red-600">{error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Groups</h1>
          {/* TODO: Add "Create Group" button */}
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {groups.map((group) => (
            <div key={group.id} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="flex items-start justify-between mb-2">
                <h3 className="text-xl font-semibold">{group.name}</h3>
                {group.is_private && (
                  <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded">
                    Private
                  </span>
                )}
              </div>
              
              <p className="text-gray-600 mb-4">{group.description || 'No description'}</p>
              
              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <span>{group.member_count} members</span>
                <span>{group.thread_count} threads</span>
              </div>
              
              <div className="flex gap-2">
                <button
                  onClick={() => window.location.href = `/groups/${group.id}`}
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
                >
                  View
                </button>
                {!group.is_private && (
                  <button
                    onClick={() => handleJoinGroup(group.id)}
                    className="flex-1 bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700"
                  >
                    Join
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
        
        {groups.length === 0 && (
          <div className="text-center text-gray-500 mt-12">
            <p className="text-xl">No groups available</p>
            <p className="mt-2">Create one to get started!</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default GroupsList;