export const metricData = [
  { 
    title: "Receita Total", 
    value: "R$ 45.231,89", 
    icon: "DollarSign", // We'll use icon names instead of components for better portability
    change: { value: 12.5, type: "increase" as const }
  },
  { 
    title: "Assinaturas Ativas", 
    value: "2.420", 
    icon: "CreditCard",
    change: { value: 8.2, type: "increase" as const }
  },
  { 
    title: "Produtos Vendidos", 
    value: "12.543", 
    icon: "ShoppingCart",
    change: { value: 3.1, type: "decrease" as const }
  },
  { 
    title: "Clientes Novos", 
    value: "482", 
    icon: "Users",
    change: { value: 14.3, type: "increase" as const }
  }
];

export const revenueChartData = [
  { name: "Jan", value: 12400 },
  { name: "Fev", value: 15600 },
  { name: "Mar", value: 18200 },
  { name: "Abr", value: 17100 },
  { name: "Mai", value: 21300 },
  { name: "Jun", value: 25400 },
  { name: "Jul", value: 24500 },
  { name: "Ago", value: 28100 },
  { name: "Set", value: 31200 },
  { name: "Out", value: 34500 },
  { name: "Nov", value: 37800 },
  { name: "Dez", value: 45200 }
];

export const categoryData = [
  { name: "Eletrônicos", value: 35 },
  { name: "Vestuário", value: 25 },
  { name: "Alimentos", value: 20 },
  { name: "Beleza", value: 15 },
  { name: "Outros", value: 5 }
];

export const salesData = [
  { name: "Seg", value: 420 },
  { name: "Ter", value: 380 },
  { name: "Qua", value: 450 },
  { name: "Qui", value: 520 },
  { name: "Sex", value: 580 },
  { name: "Sáb", value: 620 },
  { name: "Dom", value: 320 }
];

export const recentTransactionsData = [
  { 
    id: "#TR-0192", 
    customer: "João Silva", 
    email: "joao.silva@example.com",
    amount: "R$ 345,00", 
    status: "Completo", 
    date: "12 abr, 2023" 
  },
  { 
    id: "#TR-0191", 
    customer: "Maria Souza", 
    email: "maria.s@example.com",
    amount: "R$ 789,50", 
    status: "Processando", 
    date: "11 abr, 2023" 
  },
  { 
    id: "#TR-0190", 
    customer: "Carlos Mendes", 
    email: "carlos.m@example.com",
    amount: "R$ 129,99", 
    status: "Completo", 
    date: "10 abr, 2023" 
  },
  { 
    id: "#TR-0189", 
    customer: "Ana Oliveira", 
    email: "ana.o@example.com",
    amount: "R$ 459,00", 
    status: "Cancelado", 
    date: "09 abr, 2023" 
  },
  { 
    id: "#TR-0188", 
    customer: "Roberto Santos", 
    email: "r.santos@example.com",
    amount: "R$ 779,90", 
    status: "Completo", 
    date: "08 abr, 2023" 
  }
];

export const inventoryItems = [
  { name: "Smartphone X Pro", stock: 245, category: "Eletrônicos", progress: 70 },
  { name: "Notebook Ultra", stock: 52, category: "Eletrônicos", progress: 20 },
  { name: "Camiseta Premium", stock: 310, category: "Vestuário", progress: 85 },
  { name: "Fones de Ouvido Sem Fio", stock: 127, category: "Eletrônicos", progress: 60 },
  { name: "Tênis Esportivo", stock: 89, category: "Calçados", progress: 40 }
];

export const transactionColumns = [
  { title: "ID", key: "id" },
  { title: "Cliente", key: "customer" },
  { title: "Valor", key: "amount" },
  { title: "Status", key: "status" },
  { title: "Data", key: "date" }
];
