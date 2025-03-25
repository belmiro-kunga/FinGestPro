
import React from 'react';
import { MetricCard } from '../MetricCard';
import { metricData } from '@/data/dashboardData';
import { CreditCard, DollarSign, ShoppingCart, Users } from 'lucide-react';

// Map to convert string icon names to actual components
const iconMap = {
  DollarSign: <DollarSign className="h-6 w-6 text-primary" />,
  CreditCard: <CreditCard className="h-6 w-6 text-primary" />,
  ShoppingCart: <ShoppingCart className="h-6 w-6 text-primary" />,
  Users: <Users className="h-6 w-6 text-primary" />
};

const MetricsGrid = () => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {metricData.map((metric, i) => (
        <MetricCard
          key={metric.title}
          title={metric.title}
          value={metric.value}
          icon={iconMap[metric.icon as keyof typeof iconMap]}
          change={metric.change}
          delay={i * 100}
        />
      ))}
    </div>
  );
};

export default MetricsGrid;
