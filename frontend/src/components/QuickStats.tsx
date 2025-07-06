import React from 'react';
import { TrendingUp, Users, Package, Star } from 'lucide-react';

const QuickStats: React.FC = () => {
  const stats = [
    {
      icon: Users,
      value: '50K+',
      label: 'Active Users',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      icon: Package,
      value: '100K+',
      label: 'Products Listed',
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-50'
    },
    {
      icon: TrendingUp,
      value: '25K+',
      label: 'Successful Sales',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    },
    {
      icon: Star,
      value: '4.9',
      label: 'Average Rating',
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50'
    }
  ];

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Trusted by Thousands</h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Join our growing community of buyers and sellers
        </p>
      </div>
      
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div
            key={index}
            className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1"
          >
            <div className={`inline-flex p-3 rounded-xl ${stat.bgColor} mb-4`}>
              <stat.icon className={`h-6 w-6 ${stat.color}`} />
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">
              {stat.value}
            </div>
            <div className="text-gray-600 font-medium">
              {stat.label}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default QuickStats;