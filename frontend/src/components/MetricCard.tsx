
import * as React from "react";
import { cn } from "@/lib/utils";
import { DashboardCard, DashboardCardContent, DashboardCardTitle } from "./DashboardCard";
import { ArrowDown, ArrowUp } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  change?: {
    value: number;
    type: "increase" | "decrease";
  };
  className?: string;
  delay?: number;
}

export function MetricCard({ 
  title, 
  value, 
  icon, 
  change, 
  className, 
  delay = 0 
}: MetricCardProps) {
  return (
    <DashboardCard className={cn("", className)} delay={delay}>
      <DashboardCardTitle>{title}</DashboardCardTitle>
      <DashboardCardContent className="flex justify-between items-start mt-2">
        <div className="flex flex-col">
          <span className="text-2xl font-semibold">{value}</span>
          {change && (
            <div className="flex items-center mt-1 text-xs">
              <span 
                className={cn(
                  "flex items-center font-medium",
                  change.type === "increase" ? "text-green-600" : "text-red-600"
                )}
              >
                {change.type === "increase" ? (
                  <ArrowUp className="h-3 w-3 mr-1" />
                ) : (
                  <ArrowDown className="h-3 w-3 mr-1" />
                )}
                {Math.abs(change.value)}%
              </span>
              <span className="text-muted-foreground ml-1">últimos 30 dias</span>
            </div>
          )}
        </div>
        <div className="p-2 rounded-full bg-primary/10">
          {icon}
        </div>
      </DashboardCardContent>
    </DashboardCard>
  );
}
