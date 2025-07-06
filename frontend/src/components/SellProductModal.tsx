import React, { useState } from 'react';
import { X, Upload, Plus, Trash2, DollarSign, Package, MapPin, FileText, Camera, AlertCircle } from 'lucide-react';
import { categories } from '../data/mockData';
import { useAuth } from '../context/AuthContext';
import { productService, CreateProductData } from '../services/productService';
import { notificationStorage } from '../utils/storage';

interface SellProductModalProps {
  isOpen: boolean;
  onClose: () => void;
  onProductCreated: () => void;
}

interface ProductFormData {
  title: string;
  description: string;
  price: string;
  category: string;
  subcategory: string;
  condition: 'new' | 'used' | 'refurbished';
  location: string;
  images: File[];
  imagePreviewUrls: string[];
}

const SellProductModal: React.FC<SellProductModalProps> = ({ isOpen, onClose, onProductCreated }) => {
  const { user } = useAuth();
  const [currentStep, setCurrentStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState<ProductFormData>({
    title: '',
    description: '',
    price: '',
    category: '',
    subcategory: '',
    condition: 'new',
    location: '',
    images: [],
    imagePreviewUrls: []
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  if (!isOpen) return null;

  const selectedCategory = categories.find(cat => cat.name === formData.category);

  const handleInputChange = (field: keyof ProductFormData, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    
    if (formData.images.length + files.length > 8) {
      setErrors(prev => ({ ...prev, images: 'Maximum 8 images allowed' }));
      return;
    }

    const validFiles = files.filter(file => {
      const isValidType = file.type.startsWith('image/');
      const isValidSize = file.size <= 10 * 1024 * 1024; // 10MB
      return isValidType && isValidSize;
    });

    if (validFiles.length !== files.length) {
      setErrors(prev => ({ ...prev, images: 'Some files were invalid (only images under 10MB allowed)' }));
    }

    // Create preview URLs for immediate display
    const newImageUrls: string[] = [];
    for (const file of validFiles) {
      const previewUrl = URL.createObjectURL(file);
      newImageUrls.push(previewUrl);
    }

    setFormData(prev => ({
      ...prev,
      images: [...prev.images, ...validFiles],
      imagePreviewUrls: [...prev.imagePreviewUrls, ...newImageUrls]
    }));

    setErrors(prev => ({ ...prev, images: '' }));
  };

  const removeImage = (index: number) => {
    URL.revokeObjectURL(formData.imagePreviewUrls[index]);
    setFormData(prev => ({
      ...prev,
      images: prev.images.filter((_, i) => i !== index),
      imagePreviewUrls: prev.imagePreviewUrls.filter((_, i) => i !== index)
    }));
  };

  const validateStep = (step: number): boolean => {
    const newErrors: Record<string, string> = {};

    if (step === 1) {
      if (!formData.title.trim()) newErrors.title = 'Title is required';
      if (!formData.description.trim()) newErrors.description = 'Description is required';
      if (formData.description.length < 20) newErrors.description = 'Description must be at least 20 characters';
    }

    if (step === 2) {
      if (!formData.category) newErrors.category = 'Category is required';
      if (!formData.price) newErrors.price = 'Price is required';
      if (parseFloat(formData.price) <= 0) newErrors.price = 'Price must be greater than 0';
    }

    if (step === 3) {
      if (formData.images.length === 0) newErrors.images = 'At least one image is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const nextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, 4));
    }
  };

  const prevStep = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
  };

  const handleSubmit = async () => {
    if (!validateStep(currentStep) || !user) return;

    setIsSubmitting(true);

    try {
      const productData: CreateProductData = {
        title: formData.title,
        description: formData.description,
        price: parseFloat(formData.price),
        category: formData.category,
        subcategory: formData.subcategory || undefined,
        condition: formData.condition,
        location: formData.location || undefined,
        images: formData.images,
      };

      const newProduct = await productService.createProduct(productData);

      // Create notification for successful listing
      const notification = {
        id: Date.now().toString(),
        type: 'listing_created',
        title: 'Product Listed Successfully!',
        message: `Your product "${formData.title}" has been listed and is now live.`,
        timestamp: new Date().toISOString(),
        isRead: false,
        productId: newProduct.id
      };

      notificationStorage.save(notification);

      onProductCreated();
      onClose();
      
      // Reset form
      setFormData({
        title: '',
        description: '',
        price: '',
        category: '',
        subcategory: '',
        condition: 'new',
        location: '',
        images: [],
        imagePreviewUrls: []
      });
      setCurrentStep(1);
    } catch (error) {
      console.error('Error creating listing:', error);
      setErrors({ submit: error instanceof Error ? error.message : 'Failed to create listing. Please try again.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <FileText className="h-12 w-12 text-blue-600 mx-auto mb-3" />
              <h3 className="text-xl font-semibold text-gray-900">Product Details</h3>
              <p className="text-gray-600">Tell us about your product</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Product Title *
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                className={`w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.title ? 'border-red-300' : 'border-gray-300'
                }`}
                placeholder="e.g., iPhone 15 Pro Max - Space Black"
                maxLength={100}
              />
              {errors.title && <p className="text-red-500 text-sm mt-1">{errors.title}</p>}
              <p className="text-gray-500 text-sm mt-1">{formData.title.length}/100 characters</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description *
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                rows={5}
                className={`w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none ${
                  errors.description ? 'border-red-300' : 'border-gray-300'
                }`}
                placeholder="Describe your product in detail. Include condition, features, and any important information buyers should know..."
                maxLength={1000}
              />
              {errors.description && <p className="text-red-500 text-sm mt-1">{errors.description}</p>}
              <p className="text-gray-500 text-sm mt-1">{formData.description.length}/1000 characters</p>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <Package className="h-12 w-12 text-blue-600 mx-auto mb-3" />
              <h3 className="text-xl font-semibold text-gray-900">Category & Pricing</h3>
              <p className="text-gray-600">Categorize and price your product</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Category *
                </label>
                <select
                  value={formData.category}
                  onChange={(e) => handleInputChange('category', e.target.value)}
                  className={`w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                    errors.category ? 'border-red-300' : 'border-gray-300'
                  }`}
                >
                  <option value="">Select category</option>
                  {categories.map(category => (
                    <option key={category.id} value={category.name}>
                      {category.name}
                    </option>
                  ))}
                </select>
                {errors.category && <p className="text-red-500 text-sm mt-1">{errors.category}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Subcategory
                </label>
                <select
                  value={formData.subcategory}
                  onChange={(e) => handleInputChange('subcategory', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={!selectedCategory}
                >
                  <option value="">Select subcategory</option>
                  {selectedCategory?.subcategories?.map(sub => (
                    <option key={sub} value={sub}>{sub}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Price *
                </label>
                <div className="relative">
                  <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                  <input
                    type="number"
                    value={formData.price}
                    onChange={(e) => handleInputChange('price', e.target.value)}
                    className={`w-full pl-10 pr-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                      errors.price ? 'border-red-300' : 'border-gray-300'
                    }`}
                    placeholder="0.00"
                    min="0"
                    step="0.01"
                  />
                </div>
                {errors.price && <p className="text-red-500 text-sm mt-1">{errors.price}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Condition *
                </label>
                <select
                  value={formData.condition}
                  onChange={(e) => handleInputChange('condition', e.target.value as any)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="new">New</option>
                  <option value="used">Used</option>
                  <option value="refurbished">Refurbished</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Location
              </label>
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => handleInputChange('location', e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="City, State"
                />
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <Camera className="h-12 w-12 text-blue-600 mx-auto mb-3" />
              <h3 className="text-xl font-semibold text-gray-900">Product Images</h3>
              <p className="text-gray-600">Add photos to showcase your product</p>
            </div>

            <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-400 transition-colors">
              <input
                type="file"
                multiple
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
                id="image-upload"
              />
              <label htmlFor="image-upload" className="cursor-pointer">
                <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-lg font-medium text-gray-700 mb-2">
                  Click to upload images
                </p>
                <p className="text-gray-500">
                  Upload up to 8 images (max 10MB each)
                </p>
                <p className="text-sm text-gray-400 mt-2">
                  Supported formats: JPG, PNG, WebP
                </p>
              </label>
            </div>

            {errors.images && (
              <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-lg">
                <AlertCircle className="h-5 w-5" />
                <span className="text-sm">{errors.images}</span>
              </div>
            )}

            {formData.imagePreviewUrls.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-3">
                  Uploaded Images ({formData.imagePreviewUrls.length}/8)
                </h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {formData.imagePreviewUrls.map((url, index) => (
                    <div key={index} className="relative group">
                      <img
                        src={url}
                        alt={`Preview ${index + 1}`}
                        className="w-full h-24 object-cover rounded-lg border border-gray-200"
                      />
                      <button
                        onClick={() => removeImage(index)}
                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                      {index === 0 && (
                        <div className="absolute bottom-1 left-1 bg-blue-600 text-white text-xs px-2 py-1 rounded">
                          Main
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <Package className="h-12 w-12 text-green-600 mx-auto mb-3" />
              <h3 className="text-xl font-semibold text-gray-900">Review & Publish</h3>
              <p className="text-gray-600">Review your listing before publishing</p>
            </div>

            <div className="bg-gray-50 rounded-xl p-6 space-y-4">
              <div className="flex items-start space-x-4">
                {formData.imagePreviewUrls[0] && (
                  <img
                    src={formData.imagePreviewUrls[0]}
                    alt="Main product"
                    className="w-20 h-20 object-cover rounded-lg"
                  />
                )}
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-900 text-lg">{formData.title}</h4>
                  <p className="text-2xl font-bold text-green-600">${formData.price}</p>
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mt-2">
                    <span>{formData.category}</span>
                    <span>•</span>
                    <span className="capitalize">{formData.condition}</span>
                    {formData.location && (
                      <>
                        <span>•</span>
                        <span>{formData.location}</span>
                      </>
                    )}
                  </div>
                </div>
              </div>

              <div>
                <h5 className="font-medium text-gray-900 mb-2">Description</h5>
                <p className="text-gray-700 text-sm">{formData.description}</p>
              </div>

              <div>
                <h5 className="font-medium text-gray-900 mb-2">Images</h5>
                <p className="text-gray-600 text-sm">{formData.imagePreviewUrls.length} images uploaded</p>
              </div>
            </div>

            {errors.submit && (
              <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-lg">
                <AlertCircle className="h-5 w-5" />
                <span className="text-sm">{errors.submit}</span>
              </div>
            )}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white/95 backdrop-blur-sm border-b border-gray-100 p-6 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Sell Your Product</h2>
            <p className="text-gray-600">Step {currentStep} of 4</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="h-6 w-6 text-gray-500" />
          </button>
        </div>

        {/* Progress Bar */}
        <div className="px-6 py-4">
          <div className="flex items-center space-x-2">
            {[1, 2, 3, 4].map((step) => (
              <div
                key={step}
                className={`flex-1 h-2 rounded-full transition-colors ${
                  step <= currentStep ? 'bg-blue-600' : 'bg-gray-200'
                }`}
              />
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {renderStep()}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-white border-t border-gray-100 p-6 flex justify-between">
          <button
            onClick={prevStep}
            disabled={currentStep === 1}
            className="px-6 py-3 border border-gray-300 text-gray-700 rounded-xl font-medium hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>

          {currentStep < 4 ? (
            <button
              onClick={nextStep}
              className="px-6 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-colors"
            >
              Next
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="px-6 py-3 bg-green-600 text-white rounded-xl font-medium hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              {isSubmitting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Publishing...</span>
                </>
              ) : (
                <span>Publish Listing</span>
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default SellProductModal;