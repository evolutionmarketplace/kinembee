import React from 'react';
import * as LucideIcons from 'lucide-react';
import { Category } from '../types';

interface CategoryCardProps {
  category: Category;
  onCategoryClick: (category: Category) => void;
}

const CategoryCard: React.FC<CategoryCardProps> = ({ category, onCategoryClick }) => {
  // Get the icon component dynamically
  const IconComponent = (LucideIcons as any)[category.icon] || LucideIcons.Package;

  return (
    <div
      onClick={() => onCategoryClick(category)}
      className="bg-white rounded-xl p-6 shadow-sm hover:shadow-lg transition-all duration-300 cursor-pointer group border border-gray-100 hover:border-blue-200 transform hover:-translate-y-1"
    >
      <div className="flex flex-col items-center space-y-3">
        <div className="p-4 bg-gradient-to-br from-blue-50 to-emerald-50 rounded-full group-hover:from-blue-100 group-hover:to-emerald-100 transition-colors">
          <IconComponent className="h-8 w-8 text-blue-600 group-hover:text-blue-700 transition-colors" />
        </div>
        
        <div className="text-center">
          <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
            {category.name}
          </h3>
          <p className="text-sm text-gray-500 mt-1">
            {category.type === 'goods' ? 'Products' : 'Services'}
          </p>
        </div>
        
        {category.subcategories && (
          <div className="flex flex-wrap justify-center gap-1 mt-2">
            {category.subcategories.slice(0, 3).map((sub, index) => (
              <span
                key={index}
                className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full"
              >
                {sub}
              </span>
            ))}
            {category.subcategories.length > 3 && (
              <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full">
                +{category.subcategories.length - 3}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default CategoryCard;