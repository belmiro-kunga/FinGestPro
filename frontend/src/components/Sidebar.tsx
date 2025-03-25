
import React, { useState } from 'react';
import { cn } from '@/lib/utils';
import { 
  CreditCard, Users, Package, ShoppingCart, BarChart, Calendar, 
  FileText, User, DollarSign, Settings, ChevronLeft, Menu
} from 'lucide-react';
import { Button } from '@/components/ui/button';

type SidebarItemType = {
  name: string;
  icon: React.ElementType;
  path: string;
};

const sidebarItems: SidebarItemType[] = [
  { name: 'Gestão de Assinaturas', icon: CreditCard, path: '/assinaturas' },
  { name: 'Autenticação e Usuários', icon: User, path: '/usuarios' },
  { name: 'Gestão de Clientes', icon: Users, path: '/clientes' },
  { name: 'Controle de Inventário', icon: Package, path: '/inventario' },
  { name: 'Sistema de Faturamento', icon: FileText, path: '/faturamento' },
  { name: 'Gestão de Produtos', icon: ShoppingCart, path: '/produtos' },
  { name: 'Relatórios', icon: BarChart, path: '/relatorios' },
  { name: 'Sistema de Reservas', icon: Calendar, path: '/reservas' },
  { name: 'Recursos Humanos', icon: Users, path: '/rh' },
  { name: 'Ponto de Venda (POS)', icon: DollarSign, path: '/pos' },
];

type SidebarProps = {
  isMobile?: boolean;
  onCloseMobile?: () => void;
  className?: string;
};

export function Sidebar({ isMobile, onCloseMobile, className }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false);
  const [active, setActive] = useState('/');

  const toggleCollapse = () => {
    if (!isMobile) {
      setCollapsed(!collapsed);
    }
  };

  const handleItemClick = (path: string) => {
    setActive(path);
    if (isMobile && onCloseMobile) {
      onCloseMobile();
    }
  };

  return (
    <aside
      className={cn(
        'flex flex-col',
        collapsed ? 'w-[80px]' : 'w-[260px]',
        isMobile ? 'w-full' : 'h-screen sticky top-0 left-0',
        'bg-sidebar text-sidebar-foreground transition-all duration-300',
        className
      )}
    >
      <div className="flex items-center justify-between px-4 h-16 border-b border-sidebar-border">
        <div className={cn("flex items-center font-semibold text-xl", 
          collapsed && !isMobile && "opacity-0")}>
          {!collapsed && "BusinessDash"}
        </div>
        
        {isMobile ? (
          <Button variant="ghost" size="icon" onClick={onCloseMobile}>
            <ChevronLeft className="h-5 w-5" />
          </Button>
        ) : (
          <Button variant="ghost" size="icon" onClick={toggleCollapse}>
            <ChevronLeft className={cn("h-5 w-5 transition-transform", 
              collapsed && "rotate-180")} />
          </Button>
        )}
      </div>

      <nav className="flex-1 overflow-y-auto hide-scrollbar py-4">
        <ul className="space-y-1 px-2">
          {sidebarItems.map((item) => (
            <li key={item.path}>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  handleItemClick(item.path);
                }}
                className={cn(
                  "menu-link",
                  active === item.path ? "menu-link-active" : "menu-link-inactive",
                  collapsed && !isMobile && "justify-center px-2"
                )}
              >
                <item.icon className="h-5 w-5 flex-shrink-0" />
                {(!collapsed || isMobile) && <span>{item.name}</span>}
              </a>
            </li>
          ))}
        </ul>
      </nav>

      <div className="p-3 border-t border-sidebar-border">
        <a
          href="#"
          className={cn(
            "menu-link menu-link-inactive",
            collapsed && !isMobile && "justify-center px-2"
          )}
        >
          <Settings className="h-5 w-5 flex-shrink-0" />
          {(!collapsed || isMobile) && <span>Configurações</span>}
        </a>
      </div>
    </aside>
  );
}
