
import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import TransactionsTab from './TransactionsTab';
import InventoryTab from './InventoryTab';

const DataTabs = () => {
  return (
    <Tabs defaultValue="transactions">
      <TabsList className="mb-4">
        <TabsTrigger value="transactions">Transações Recentes</TabsTrigger>
        <TabsTrigger value="inventory">Estoque</TabsTrigger>
      </TabsList>
      <TabsContent value="transactions">
        <TransactionsTab />
      </TabsContent>
      <TabsContent value="inventory">
        <InventoryTab />
      </TabsContent>
    </Tabs>
  );
};

export default DataTabs;
