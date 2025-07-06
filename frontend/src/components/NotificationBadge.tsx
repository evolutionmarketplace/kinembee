import React, { useState, useEffect } from 'react';
import { Bell } from 'lucide-react';
import { notificationStorage } from '../utils/storage';

interface NotificationBadgeProps {
  onClick: () => void;
}

const NotificationBadge: React.FC<NotificationBadgeProps> = ({ onClick }) => {
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const updateUnreadCount = () => {
      const count = notificationStorage.getUnreadCount();
      setUnreadCount(count);
    };

    // Initial load
    updateUnreadCount();

    // Listen for storage changes
    window.addEventListener('storage', updateUnreadCount);
    
    // Check for updates periodically
    const interval = setInterval(updateUnreadCount, 1000);

    return () => {
      window.removeEventListener('storage', updateUnreadCount);
      clearInterval(interval);
    };
  }, []);

  return (
    <button
      onClick={onClick}
      className="relative p-2 text-gray-600 hover:text-blue-600 transition-colors"
    >
      <Bell className="h-5 w-5" />
      {unreadCount > 0 && (
        <span className="absolute -top-1 -right-1 h-5 w-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center font-medium">
          {unreadCount > 9 ? '9+' : unreadCount}
        </span>
      )}
    </button>
  );
};

export default NotificationBadge;