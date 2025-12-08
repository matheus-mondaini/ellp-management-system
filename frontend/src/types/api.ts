export type LoginRequest = {
  email: string;
  password: string;
};

export type TokenPair = {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
};

export type UserRole = "admin" | "professor" | "tutor" | "aluno";

export type AuthenticatedUser = {
  id: string;
  email: string;
  role: UserRole;
  nome_completo: string;
  ativo: boolean;
  ultimo_login: string | null;
};

export type DashboardMetrics = {
  oficinas_ativas: number;
  oficinas_planejadas: number;
  oficinas_concluidas: number;
  total_inscricoes: number;
  inscritos_concluidos: number;
  certificados_emitidos: number;
  presenca_media_geral: number;
  ultima_atualizacao: string;
};

export type Tema = {
  id: string;
  nome: string;
  descricao: string | null;
  ativo: boolean;
};

export type OficinaStatus =
  | "planejada"
  | "inscricoes_abertas"
  | "em_andamento"
  | "concluida"
  | "cancelada";

export type Oficina = {
  id: string;
  titulo: string;
  descricao: string | null;
  objetivo: string | null;
  carga_horaria: number;
  capacidade_maxima: number;
  numero_aulas: number | null;
  data_inicio: string;
  data_fim: string;
  dias_semana: string | null;
  horario: string | null;
  local: string;
  status: OficinaStatus;
  professor_id: string;
  temas: Tema[];
  total_inscritos: number;
  vagas_disponiveis: number;
  total_concluintes: number;
  lotada: boolean;
  created_at: string;
  updated_at: string;
};

export type CertificadoTipo = "conclusao_aluno" | "participacao_tutor";

export type Certificado = {
  id: string;
  tipo: CertificadoTipo;
  inscricao_id: string | null;
  tutor_id: string | null;
  oficina_id: string;
  hash_validacao: string;
  codigo_verificacao: string;
  arquivo_pdf_url: string | null;
  arquivo_pdf_nome: string | null;
  data_emissao: string;
  carga_horaria_certificada: number | null;
  percentual_presenca_certificado: number | null;
  revogado: boolean;
};

export type CertificadoValidacao = {
  hash_validacao: string;
  codigo_verificacao: string;
  tipo: CertificadoTipo;
  valido: boolean;
  participante_nome: string;
  participante_tipo: string;
  oficina_id: string;
  oficina_titulo: string;
  data_emissao: string;
  carga_horaria_certificada: number | null;
  percentual_presenca_certificado: number | null;
  revogado: boolean;
  motivo_revogacao: string | null;
  arquivo_pdf_url: string | null;
  arquivo_pdf_nome: string | null;
};

export type UserSummary = {
  id: string;
  email: string;
  role: UserRole;
  nome_completo: string;
  ativo: boolean;
};

export type CreateOficinaPayload = {
  titulo: string;
  descricao?: string | null;
  objetivo?: string | null;
  carga_horaria: number;
  capacidade_maxima: number;
  numero_aulas?: number | null;
  data_inicio: string;
  data_fim: string;
  local: string;
  dias_semana?: string | null;
  horario?: string | null;
  status?: OficinaStatus;
  professor_id: string;
  tema_ids?: string[];
};
