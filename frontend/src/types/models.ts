export interface Project {
  id: number;
  name: string;
  description: string;
  owner: number;
  members: number[];
  created_at: string;
  progress_percentage: number;
}

export interface Asset {
  id: number;
  name: string;
  description: string;
  asset_type: '3D' | '2D' | 'AUDIO' | 'VFX' | 'OTHER';
  project: number;
  owner: number;
  tags: string;
  created_at: string;
  updated_at: string;
}

export interface AssetVersion {
  id: number;
  asset: number;
  version_number: number;
  file_path: string;
  note: string;
  created_at: string;
  created_by: number;
}

export interface Bug {
  id: number;
  title: string;
  description: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  status: 'TRIAGE' | 'IN_PROGRESS' | 'BLOCKED' | 'RESOLVED';
  project: number;
  reporter: number;
  assignee: number | null;
  created_at: string;
  updated_at: string;
}
