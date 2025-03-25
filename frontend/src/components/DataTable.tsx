
import * as React from "react";
import { cn } from "@/lib/utils";
import { 
  DashboardCard, 
  DashboardCardContent, 
  DashboardCardHeader, 
  DashboardCardTitle 
} from "./DashboardCard";
import { Button } from "@/components/ui/button";
import { ChevronDown, Download, Plus } from "lucide-react";

interface DataTableProps {
  title: string;
  columns: Array<{
    title: string;
    key: string;
    render?: (value: any, record: any) => React.ReactNode;
  }>;
  data: any[];
  className?: string;
  delay?: number;
}

export function DataTable({ 
  title, 
  columns, 
  data, 
  className, 
  delay = 0 
}: DataTableProps) {
  return (
    <DashboardCard className={cn("", className)} delay={delay}>
      <DashboardCardHeader>
        <DashboardCardTitle>{title}</DashboardCardTitle>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" className="h-8">
            <Download className="h-3.5 w-3.5 mr-1" />
            Exportar
          </Button>
          <Button size="sm" className="h-8">
            <Plus className="h-3.5 w-3.5 mr-1" />
            Adicionar
          </Button>
        </div>
      </DashboardCardHeader>
      <DashboardCardContent>
        <div className="rounded-md border">
          <div className="w-full overflow-auto">
            <table className="w-full caption-bottom text-sm">
              <thead className="[&_tr]:border-b">
                <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                  {columns.map((column, i) => (
                    <th 
                      key={column.key} 
                      className="h-10 px-4 text-left align-middle font-medium text-muted-foreground"
                    >
                      <div className="flex items-center justify-between">
                        {column.title}
                        {i === 0 && (
                          <ChevronDown className="h-4 w-4 text-muted-foreground ml-2" />
                        )}
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="[&_tr:last-child]:border-0">
                {data.map((record, i) => (
                  <tr 
                    key={i} 
                    className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
                  >
                    {columns.map((column) => (
                      <td 
                        key={`${i}-${column.key}`} 
                        className="p-4 align-middle"
                      >
                        {column.render 
                          ? column.render(record[column.key], record) 
                          : record[column.key]}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </DashboardCardContent>
    </DashboardCard>
  );
}
