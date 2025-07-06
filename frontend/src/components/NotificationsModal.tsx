import React, { useState, useEffect } from 'react';
import { Bell, X, Check, CheckCheck, Trash2, Package, DollarSign, Star, MessageCircle, AlertCircle, TrendingUp } from 'lucide-react';
import { notificationStorage } from '../utils/storage';

interface Notification {
  id: string;
  type: 'listing_created' | 'listing_approved' | 'listing_rejected' | 'message' | 'sale' | 'review' | 'system';
  title: string;
  message: string;
  timestamp: string;
  isRead: boolean;
  productId?: string;
  actionUrl?: string;
}

interface NotificationsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const NotificationsModal: React.FC<NotificationsModalProps> = ({ isOpen, onClose }) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [filter, setFilter] = useState<'all' | 'unread' | 'listings' | 'messages'>('all');

  useEffect(() => {
    if (isOpen) {
      loadNotifications();
    }
  }, [isOpen]);

  useEffect(() => {
    const handleStorageChange = () => {
      if (isOpen) {
        loadNotifications();
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [isOpen]);

  const loadNotifications = () => {
    const stored = notificationStorage.getAll();
    setNotifications(stored);
  };

  const markAsRead = (id: string) => {
    notificationStorage.markAsRead(id);
    loadNotifications();
  };

  const markAllAsRead = () => {
    notificationStorage.markAllAsRead();
    loadNotifications();
  };

  const deleteNotification = (id: string) => {
    notificationStorage.remove(id);
    loadNotifications();
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'listing_created':
      case 'listing_approved':
        return <Package className="h-5 w-5 text-green-600" />;
      case 'listing_rejected':
        return <AlertCircle className="h-5 w-5 text-red-600" />;
      case 'message':
        return <MessageCircle className="h-5 w-5 text-blue-600" />;
      case 'sale':
        return <DollarSign className="h-5 w-5 text-green-600" />;
      case 'review':
        return <Star className="h-5 w-5 text-yellow-600" />;
      case 'system':
        return <TrendingUp className="h-5 w-5 text-purple-600" />;
      default:
        return <Bell className="h-5 w-5 text-gray-600" />;
    }
  };

  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'listing_created':
      case 'listing_approved':
      case 'sale':
        return 'bg-green-50 border-green-200';
      case 'listing_rejected':
        return 'bg-red-50 border-red-200';
      case 'message':
        return 'bg-blue-50 border-blue-200';
      case 'review':
        return 'bg-yellow-50 border-yellow-200';
      case 'system':
        return 'bg-purple-50 border-purple-200';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInMinutes = Math.floor((now.getTime() - time.getTime()) / (1000 * 60));

    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    if (diffInMinutes < 10080) return `${Math.floor(diffInMinutes / 1440)}d ago`;
    return time.toLocaleDateString();
  };

  const filteredNotifications = notifications.filter(notif => {
    switch (filter) {
      case 'unread':
        return !notif.isRead;
      case 'listings':
        return ['listing_created', 'listing_approved', 'listing_rejected'].includes(notif.type);
      case 'messages':
        return notif.type === 'message';
      default:
        return true;
    }
  });

  const unreadCount = notifications.filter(n => !n.isRead).length;

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="sticky top-0 bg-white/95 backdrop-blur-sm border-b border-gray-100 p-6 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Bell className="h-6 w-6 text-blue-600" />
            <div>
              <h2 className="text-xl font-bold text-gray-900">Notifications</h2>
              {unreadCount > 0 && (
                <p className="text-sm text-gray-600">{unreadCount} unread</p>
              )}
            </div>
          </div>
          <div className="flex items-center space-x-2">
            {unreadCount > 0 && (
              <button
                onClick={markAllAsRead}
                className="flex items-center space-x-1 text-blue-600 hover:text-blue-700 text-sm font-medium"
              >
                <CheckCheck className="h-4 w-4" />
                <span>Mark all read</span>
              </button>
            )}
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <X className="h-5 w-5 text-gray-500" />
            </button>
          </div>
        </div>

        {/* Filter Tabs */}
        <div className="px-6 py-4 border-b border-gray-100">
          <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
            {[
              { key: 'all', label: 'All' },
              { key: 'unread', label: 'Unread' },
              { key: 'listings', label: 'Listings' },
              { key: 'messages', label: 'Messages' }
            ].map(tab => (
              <button
                key={tab.key}
                onClick={() => setFilter(tab.key as any)}
                className={`flex-1 px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                  filter === tab.key
                    ? 'bg-white text-blue-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {tab.label}
                {tab.key === 'unread' && unreadCount > 0 && (
                  <span className="ml-2 bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
                    {unreadCount}
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Notifications List */}
        <div className="overflow-y-auto max-h-96">
          {filteredNotifications.length > 0 ? (
            <div className="divide-y divide-gray-100">
              {filteredNotifications.map(notification => (
                <div
                  key={notification.id}
                  className={`p-4 hover:bg-gray-50 transition-colors relative ${
                    !notification.isRead ? 'bg-blue-50/30' : ''
                  }`}
                >
                  <div className="flex items-start space-x-3">
                    <div className={`p-2 rounded-lg border ${getNotificationColor(notification.type)}`}>
                      {getNotificationIcon(notification.type)}
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className={`font-medium ${!notification.isRead ? 'text-gray-900' : 'text-gray-700'}`}>
                            {notification.title}
                          </h4>
                          <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                            {notification.message}
                          </p>
                          <p className="text-xs text-gray-500 mt-2">
                            {formatTimestamp(notification.timestamp)}
                          </p>
                        </div>
                        
                        <div className="flex items-center space-x-2 ml-4">
                          {!notification.isRead && (
                            <button
                              onClick={() => markAsRead(notification.id)}
                              className="p-1 text-blue-600 hover:text-blue-700 transition-colors"
                              title="Mark as read"
                            >
                              <Check className="h-4 w-4" />
                            </button>
                          )}
                          <button
                            onClick={() => deleteNotification(notification.id)}
                            className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                            title="Delete notification"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                      
                      {!notification.isRead && (
                        <div className="absolute left-2 top-1/2 transform -translate-y-1/2 w-2 h-2 bg-blue-600 rounded-full"></div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <Bell className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No notifications</h3>
              <p className="text-gray-500">
                {filter === 'all' 
                  ? "You're all caught up! No notifications to show."
                  : `No ${filter} notifications to show.`
                }
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        {filteredNotifications.length > 0 && (
          <div className="border-t border-gray-100 p-4 text-center">
            <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
              View All Notifications
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default NotificationsModal;