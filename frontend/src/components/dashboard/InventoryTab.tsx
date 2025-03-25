
import React from 'react';
import { inventoryItems } from '@/data/dashboardData';
import { Package } from 'lucide-react';
import { Progress } from '@/components/ui/progress';
import {
  DashboardCard,
  DashboardCardContent,
  DashboardCardHeader,
  DashboardCardTitle
} from '../DashboardCard';

const InventoryTab = () => {
  return (
    <DashboardCard delay={300}>
      <DashboardCardHeader>
        <DashboardCardTitle>Status do Inventário</DashboardCardTitle>
      </DashboardCardHeader>
      <DashboardCardContent>
        <div className="space-y-5">
          {inventoryItems.map((item) => (
            <div key={item.name} className="space-y-2">
              <div className="flex justify-between items-center">
                <div>
                  <div className="font-medium">{item.name}</div>
                  <div className="text-xs text-muted-foreground flex items-center">
                    <Package className="h-3 w-3 mr-1" />
                    {item.stock} unidades | {item.category}
                  </div>
                </div>
                <div className="text-sm font-medium">{item.progress}%</div>
              </div>
              <Progress value={item.progress} className="h-2" />
            </div>
          ))}
        </div>
      </DashboardCardContent>
    </DashboardCard>
  );
};

export default InventoryTab;
