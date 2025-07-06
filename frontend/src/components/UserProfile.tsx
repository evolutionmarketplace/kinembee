import React, { useState } from 'react';
import { User, Mail, Phone, MapPin, Calendar, Star, Package, Edit3, X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { mockProducts } from '../data/mockData';

interface UserProfileProps {
  isOpen: boolean;
  onClose: () => void;
  onSellClick: () => void; // Add this prop
}

const UserProfile: React.FC<UserProfileProps> = ({ isOpen, onClose, onSellClick }) => {
  const { user, updateUser } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({
    name: user?.name || '',
    contactNumber: user?.contactNumber || '',
    email: user?.email || ''
  });

  if (!isOpen || !user) return null;

  const userProducts = mockProducts.filter(product => product.sellerId === user.id);

  const handleSaveEdit = () => {
    updateUser(editData);
    setIsEditing(false);
  };

  const handleSellClick = () => {
    onSellClick();
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-100">
          <h2 className="text-2xl font-bold text-gray-900">My Profile</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors p-1"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        <div className="p-6">
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Profile Info */}
            <div className="lg:col-span-1">
              <div className="bg-gradient-to-br from-blue-50 to-emerald-50 rounded-xl p-6">
                {/* Avatar */}
                <div className="text-center mb-6">
                  {user.avatar ? (
                    <img 
                      src={user.avatar} 
                      alt={user.name}
                      className="h-24 w-24 rounded-full object-cover mx-auto mb-4 border-4 border-white shadow-lg"
                    />
                  ) : (
                    <div className="h-24 w-24 bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4 border-4 border-white shadow-lg">
                      {user.name.charAt(0).toUpperCase()}
                    </div>
                  )}
                  
                  <div className="flex items-center justify-center space-x-2">
                    <h3 className="text-xl font-bold text-gray-900">{user.name}</h3>
                    {user.isVerified && (
                      <div className="h-6 w-6 bg-green-500 rounded-full flex items-center justify-center">
                        <svg className="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                    )}
                  </div>
                  
                  {user.isAdmin && (
                    <div className="inline-flex items-center px-2 py-1 bg-purple-100 text-purple-800 text-xs font-medium rounded-full mt-2">
                      Admin
                    </div>
                  )}
                </div>

                {/* Profile Details */}
                <div className="space-y-4">
                  {isEditing ? (
                    <div className="space-y-3">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                        <input
                          type="text"
                          value={editData.name}
                          onChange={(e) => setEditData({...editData, name: e.target.value})}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                        <input
                          type="tel"
                          value={editData.contactNumber}
                          onChange={(e) => setEditData({...editData, contactNumber: e.target.value})}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={handleSaveEdit}
                          className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
                        >
                          Save
                        </button>
                        <button
                          onClick={() => setIsEditing(false)}
                          className="flex-1 bg-gray-200 text-gray-800 py-2 px-4 rounded-lg hover:bg-gray-300 transition-colors"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <>
                      <div className="flex items-center space-x-3 text-gray-600">
                        <Mail className="h-5 w-5" />
                        <span>{user.email}</span>
                      </div>
                      
                      {user.contactNumber && (
                        <div className="flex items-center space-x-3 text-gray-600">
                          <Phone className="h-5 w-5" />
                          <span>{user.contactNumber}</span>
                        </div>
                      )}
                      
                      <div className="flex items-center space-x-3 text-gray-600">
                        <Calendar className="h-5 w-5" />
                        <span>Joined {new Date(user.createdAt).toLocaleDateString()}</span>
                      </div>
                      
                      <button
                        onClick={() => setIsEditing(true)}
                        className="w-full flex items-center justify-center space-x-2 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        <Edit3 className="h-4 w-4" />
                        <span>Edit Profile</span>
                      </button>
                    </>
                  )}
                </div>

                {/* Stats */}
                <div className="grid grid-cols-2 gap-4 mt-6 pt-6 border-t border-gray-200">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">{userProducts.length}</div>
                    <div className="text-sm text-gray-500">Listings</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">4.8</div>
                    <div className="text-sm text-gray-500 flex items-center justify-center">
                      <Star className="h-3 w-3 text-yellow-400 mr-1" />
                      Rating
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* My Listings */}
            <div className="lg:col-span-2">
              <div className="flex items-center justify-between mb-6">
                <h4 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
                  <Package className="h-5 w-5" />
                  <span>My Listings ({userProducts.length})</span>
                </h4>
                <button 
                  onClick={handleSellClick}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
                >
                  Add New Listing
                </button>
              </div>

              {userProducts.length > 0 ? (
                <div className="space-y-4">
                  {userProducts.map(product => (
                    <div key={product.id} className="bg-gray-50 rounded-xl p-4 border border-gray-200">
                      <div className="flex items-center space-x-4">
                        <img
                          src={product.images[0]}
                          alt={product.title}
                          className="h-16 w-16 rounded-lg object-cover"
                        />
                        <div className="flex-1">
                          <h5 className="font-semibold text-gray-900">{product.title}</h5>
                          <p className="text-sm text-gray-500 line-clamp-1">{product.description}</p>
                          <div className="flex items-center justify-between mt-2">
                            <span className="text-lg font-bold text-blue-600">
                              ${product.price.toLocaleString()}
                            </span>
                            <div className="flex items-center space-x-4 text-sm text-gray-500">
                              <span>{product.views} views</span>
                              <span>{product.likes} likes</span>
                            </div>
                          </div>
                        </div>
                        <div className="flex flex-col space-y-2">
                          <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                            Edit
                          </button>
                          <button className="text-red-600 hover:text-red-700 text-sm font-medium">
                            Delete
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <div className="h-24 w-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Package className="h-12 w-12 text-gray-400" />
                  </div>
                  <h5 className="text-lg font-medium text-gray-900 mb-2">No listings yet</h5>
                  <p className="text-gray-500 mb-4">Start selling by creating your first listing</p>
                  <button 
                    onClick={handleSellClick}
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
                  >
                    Create First Listing
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;