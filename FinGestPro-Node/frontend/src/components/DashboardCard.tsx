
import * as React from "react";
import { cn } from "@/lib/utils";

interface DashboardCardProps {
  children: React.ReactNode;
  className?: string;
  delay?: number;
}

export function DashboardCard({ children, className, delay = 0 }: DashboardCardProps) {
  return (
    <div 
      className={cn(
        "rounded-lg border bg-card text-card-foreground shadow-sm p-5 animate-on-load card-hover",
        className
      )}
      style={{ '--delay': `${delay}ms` } as React.CSSProperties}
    >
      {children}
    </div>
  );
}

export function DashboardCardHeader({ 
  children, 
  className 
}: { 
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("flex items-center justify-between mb-4", className)}>
      {children}
    </div>
  );
}

export function DashboardCardTitle({ 
  children, 
  className 
}: { 
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <h3 className={cn("font-medium text-sm text-muted-foreground", className)}>
      {children}
    </h3>
  );
}

export function DashboardCardContent({ 
  children, 
  className 
}: { 
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("", className)}>
      {children}
    </div>
  );
}

export function DashboardCardFooter({ 
  children, 
  className 
}: { 
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("flex items-center pt-4 mt-auto", className)}>
      {children}
    </div>
  );
}
