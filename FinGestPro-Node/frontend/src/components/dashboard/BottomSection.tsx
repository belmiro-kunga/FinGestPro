
import React from 'react';
import { ChartCard } from '../ChartCard';
import { salesData, recentTransactionsData } from '@/data/dashboardData';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import {
  DashboardCard,
  DashboardCardContent,
  DashboardCardHeader,
  DashboardCardTitle
} from '../DashboardCard';

const BottomSection = () => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <ChartCard
        title="Vendas Diárias"
        type="bar"
        data={salesData}
        delay={400}
      />
      
      <DashboardCard delay={500}>
        <DashboardCardHeader>
          <DashboardCardTitle>Clientes Recentes</DashboardCardTitle>
        </DashboardCardHeader>
        <DashboardCardContent>
          <div className="space-y-6">
            {recentTransactionsData.slice(0, 4).map((customer) => (
              <div key={customer.id} className="flex justify-between items-center">
                <div className="flex items-center gap-3">
                  <Avatar>
                    <AvatarImage src={`https://api.dicebear.com/7.x/initials/svg?seed=${customer.customer}`} />
                    <AvatarFallback>{customer.customer.charAt(0)}</AvatarFallback>
                  </Avatar>
                  <div>
                    <div className="font-medium">{customer.customer}</div>
                    <div className="text-xs text-muted-foreground">{customer.email}</div>
                  </div>
                </div>
                <Button variant="ghost" size="sm">Ver Detalhes</Button>
              </div>
            ))}
          </div>
        </DashboardCardContent>
      </DashboardCard>
    </div>
  );
};

export default BottomSection;
