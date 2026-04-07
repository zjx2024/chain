// 图谱节点类型
export interface GraphNode {
  id: string;
  name: string;
  category: string;
  symbolSize: number;
  value?: number;
  x?: number;
  y?: number;
}

// 图谱连接类型
export interface GraphLink {
  source: string;
  target: string;
  value: number;
}

// 图谱数据结构
export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
  categories: { name: string }[];
} 
