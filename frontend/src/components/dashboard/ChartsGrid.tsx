
import React from 'react';
import { ChartCard } from '../ChartCard';
import { revenueChartData, categoryData } from '@/data/dashboardData';

const ChartsGrid = () => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <ChartCard
        title="Receita Mensal"
        type="line"
        data={revenueChartData}
        className="lg:col-span-2"
        delay={100}
      />
      <ChartCard
        title="Vendas por Categoria"
        type="pie"
        data={categoryData}
        delay={200}
      />
    </div>
  );
};

export default ChartsGrid;
