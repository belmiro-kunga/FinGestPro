
import React from 'react';
import { DataTable } from '../DataTable';
import { transactionColumns } from '@/data/dashboardData';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

// Custom render functions that were previously inline
const renderCustomer = (value: string, record: any) => (
  <div className="flex items-center gap-2">
    <Avatar className="h-8 w-8">
      <AvatarImage src={`https://api.dicebear.com/7.x/initials/svg?seed=${record.customer}`} alt={value} />
      <AvatarFallback>{value.charAt(0)}</AvatarFallback>
    </Avatar>
    <div className="flex flex-col">
      <span className="font-medium">{value}</span>
      <span className="text-xs text-muted-foreground">{record.email}</span>
    </div>
  </div>
);

const renderStatus = (value: string) => (
  <div className={`px-2 py-1 rounded-full text-xs font-medium inline-block ${
    value === "Completo" ? "bg-green-100 text-green-800" :
    value === "Processando" ? "bg-blue-100 text-blue-800" :
    "bg-red-100 text-red-800"
  }`}>
    {value}
  </div>
);

// Process columns to include render functions
const processedColumns = transactionColumns.map(column => {
  if (column.key === 'customer') {
    return {
      ...column,
      render: renderCustomer
    };
  }
  if (column.key === 'status') {
    return {
      ...column,
      render: renderStatus
    };
  }
  return column;
});

const TransactionsTab = () => {
  return (
    <DataTable
      title="Transações Recentes"
      columns={processedColumns}
      data={recentTransactionsData}
      delay={300}
    />
  );
};

// Import the data separately
import { recentTransactionsData } from '@/data/dashboardData';

export default TransactionsTab;
