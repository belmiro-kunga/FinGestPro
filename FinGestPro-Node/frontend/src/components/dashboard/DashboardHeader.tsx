
import React from 'react';
import { Button } from "@/components/ui/button";
import { ChevronDown } from 'lucide-react';

const DashboardHeader = () => {
  return (
    <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <h1 className="text-2xl font-semibold">Visão Geral</h1>
        <p className="text-muted-foreground">Bem-vindo de volta, Belmiro!</p>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="outline">
          Últimos 30 dias
          <ChevronDown className="ml-2 h-4 w-4" />
        </Button>
        <Button>Gerar Relatório</Button>
      </div>
    </div>
  );
};

export default DashboardHeader;
