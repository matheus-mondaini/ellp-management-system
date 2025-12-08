import { randomUUID } from "crypto";

import {
  type AuthenticatedUser,
  type Certificado,
  type CertificadoValidacao,
  type CreateOficinaPayload,
  type DashboardMetrics,
  type Oficina,
  type Tema,
  type TokenPair,
  type UserSummary,
} from "@/types/api";

const MOCK_STORAGE_BASE = "https://storage.ellp.dev/certificados";

// ---------------------------
// Types & state definition
// ---------------------------
type MockUserRecord = AuthenticatedUser & { password: string };

type MockCertificadoRecord = {
  certificado: Certificado;
  validacao: CertificadoValidacao;
};

type MockState = {
  dashboard: DashboardMetrics;
  temas: Tema[];
  oficinas: Oficina[];
  users: MockUserRecord[];
  certificados: MockCertificadoRecord[];
};

let accessTokenMap = new Map<string, string>();
let refreshTokenMap = new Map<string, string>();

const buildDashboard = (): DashboardMetrics => ({
  oficinas_ativas: 3,
  oficinas_planejadas: 1,
  oficinas_concluidas: 2,
  total_inscricoes: 86,
  inscritos_concluidos: 42,
  certificados_emitidos: 58,
  presenca_media_geral: 87.5,
  ultima_atualizacao: new Date().toISOString(),
});

const buildTemas = (): Tema[] => [
  {
    id: randomUUID(),
    nome: "Robótica com LEGO",
    descricao: "Montagem e lógica com kits LEGO Education",
    ativo: true,
  },
  {
    id: randomUUID(),
    nome: "Scratch Básico",
    descricao: "Algoritmos com blocos para crianças",
    ativo: true,
  },
  {
    id: randomUUID(),
    nome: "Arduino Lúdico",
    descricao: "Circuitos simples para oficinas itinerantes",
    ativo: true,
  },
];

const buildUsers = (): MockUserRecord[] => {
  const baseDate = new Date().toISOString();
  return [
    {
      id: randomUUID(),
      email: "admin@ellp.test",
      role: "admin",
      nome_completo: "Administrador Geral",
      ativo: true,
      ultimo_login: baseDate,
      password: "admin12345",
    },
    {
      id: randomUUID(),
      email: "prof@ellp.test",
      role: "professor",
      nome_completo: "Prof. Helena Souza",
      ativo: true,
      ultimo_login: baseDate,
      password: "prof12345",
    },
    {
      id: randomUUID(),
      email: "tutor@ellp.test",
      role: "tutor",
      nome_completo: "Tutor Rafael Lima",
      ativo: true,
      ultimo_login: baseDate,
      password: "tutor12345",
    },
    {
      id: randomUUID(),
      email: "aluno@ellp.test",
      role: "aluno",
      nome_completo: "Ana Clara",
      ativo: true,
      ultimo_login: baseDate,
      password: "aluno12345",
    },
  ];
};

const buildOficinas = (temas: Tema[], users: MockUserRecord[]): Oficina[] => {
  const professorId = users.find((user) => user.role === "professor")?.id ?? users[0].id;
  const now = new Date();
  const makeOficina = (overrides: Partial<Oficina>): Oficina => ({
    id: randomUUID(),
    titulo: "Robótica Criativa",
    descricao: "Oficina prática com LEGO", 
    objetivo: "Estimular lógica e colaboração",
    carga_horaria: 16,
    capacidade_maxima: 20,
    numero_aulas: 4,
    data_inicio: now.toISOString(),
    data_fim: new Date(now.getTime() + 1000 * 60 * 60 * 24 * 30).toISOString(),
    dias_semana: "Sábados",
    horario: "09h às 11h",
    local: "UTFPR Cornélio",
    status: "em_andamento",
    professor_id: professorId,
    temas: [temas[0]],
    total_inscritos: 18,
    vagas_disponiveis: 2,
    total_concluintes: 10,
    lotada: false,
    created_at: now.toISOString(),
    updated_at: now.toISOString(),
    ...overrides,
  });

  return [
    makeOficina({ titulo: "Robótica Criativa", status: "em_andamento" }),
    makeOficina({
      titulo: "Primeiros passos no Scratch",
      status: "inscricoes_abertas",
      descricao: "Fluxos animados",
      vagas_disponiveis: 8,
      total_inscritos: 12,
      temas: [temas[1]],
    }),
    makeOficina({
      titulo: "Arduino Lúdico para tutores",
      status: "planejada",
      total_inscritos: 0,
      vagas_disponiveis: 20,
      temas: [temas[2]],
    }),
  ];
};

const buildCertificados = (oficinas: Oficina[]): MockCertificadoRecord[] => {
  const [oficina] = oficinas;
  const certificadoId = randomUUID();
  const hash = `ellp-hash-${certificadoId.slice(0, 8)}`;
  const pdfUrl = `${MOCK_STORAGE_BASE}/${certificadoId}.pdf`;
  return [
    {
      certificado: {
        id: certificadoId,
        tipo: "conclusao_aluno",
        inscricao_id: randomUUID(),
        tutor_id: null,
        oficina_id: oficina.id,
        hash_validacao: hash,
        codigo_verificacao: "ELLPPW-12345",
        arquivo_pdf_url: pdfUrl,
        arquivo_pdf_nome: `certificado-${certificadoId}.pdf`,
        data_emissao: new Date().toISOString(),
        carga_horaria_certificada: oficina.carga_horaria,
        percentual_presenca_certificado: 92.5,
        revogado: false,
      },
      validacao: {
        hash_validacao: hash,
        codigo_verificacao: "ELLPPW-12345",
        tipo: "conclusao_aluno",
        valido: true,
        participante_nome: "Ana Clara Souza",
        participante_tipo: "aluno",
        oficina_id: oficina.id,
        oficina_titulo: oficina.titulo,
        data_emissao: new Date().toISOString(),
        carga_horaria_certificada: oficina.carga_horaria,
        percentual_presenca_certificado: 92.5,
        revogado: false,
        motivo_revogacao: null,
        arquivo_pdf_url: pdfUrl,
        arquivo_pdf_nome: `certificado-${certificadoId}.pdf`,
      },
    },
  ];
};

const buildInitialState = (): MockState => {
  const temas = buildTemas();
  const users = buildUsers();
  const oficinas = buildOficinas(temas, users);
  const dashboard = buildDashboard();
  const certificados = buildCertificados(oficinas);
  return { dashboard, temas, users, oficinas, certificados };
};

let state: MockState = buildInitialState();

// ---------------------------
// Helpers
// ---------------------------
export function resetMockState() {
  state = buildInitialState();
  accessTokenMap = new Map();
  refreshTokenMap = new Map();
}

export function listMockTemas(): Tema[] {
  return state.temas;
}

export function listMockUsers(): UserSummary[] {
  return state.users.map(({ password: _password, ...user }) => ({
    id: user.id,
    email: user.email,
    role: user.role,
    nome_completo: user.nome_completo,
    ativo: user.ativo,
  }));
}

export function getDashboardMetrics(): DashboardMetrics {
  return state.dashboard;
}

export function listMockOficinas(): Oficina[] {
  return state.oficinas;
}

export function createMockOficina(payload: CreateOficinaPayload): Oficina {
  const now = new Date().toISOString();
  const temas = payload.tema_ids?.map((id) => state.temas.find((tema) => tema.id === id)).filter(Boolean) as Tema[];
  const totalInscritos = Math.min(payload.capacidade_maxima, Math.max(payload.capacidade_maxima - 3, 0));
  const vagasDisponiveis = Math.max(payload.capacidade_maxima - totalInscritos, 0);

  const oficina: Oficina = {
    id: randomUUID(),
    titulo: payload.titulo,
    descricao: payload.descricao ?? null,
    objetivo: payload.objetivo ?? null,
    carga_horaria: payload.carga_horaria,
    capacidade_maxima: payload.capacidade_maxima,
    numero_aulas: payload.numero_aulas ?? null,
    data_inicio: payload.data_inicio,
    data_fim: payload.data_fim,
    dias_semana: payload.dias_semana ?? null,
    horario: payload.horario ?? null,
    local: payload.local,
    status: payload.status ?? "planejada",
    professor_id: payload.professor_id,
    temas: temas ?? [],
    total_inscritos: totalInscritos,
    vagas_disponiveis: vagasDisponiveis,
    total_concluintes: 0,
    lotada: vagasDisponiveis === 0,
    created_at: now,
    updated_at: now,
  };

  state.oficinas = [oficina, ...state.oficinas];
  state.dashboard.oficinas_planejadas += 1;
  return oficina;
}

export function listMockCertificados(): Certificado[] {
  return state.certificados.map((record) => record.certificado);
}

export function getMockCertificadoById(id: string): Certificado | undefined {
  return state.certificados.find((record) => record.certificado.id === id)?.certificado;
}

export function getMockCertificadoValidation(hash: string): CertificadoValidacao | undefined {
  return state.certificados.find((record) => record.certificado.hash_validacao === hash)?.validacao;
}

export function authenticateMockUser(
  email: string,
  password: string,
): { tokens: TokenPair; user: AuthenticatedUser } | null {
  const found = state.users.find((user) => user.email === email && user.password === password);
  if (!found) {
    return null;
  }

  const accessToken = `mock-access-${randomUUID()}`;
  const refreshToken = `mock-refresh-${randomUUID()}`;
  accessTokenMap.set(accessToken, found.id);
  refreshTokenMap.set(refreshToken, found.id);

  const tokens: TokenPair = {
    access_token: accessToken,
    refresh_token: refreshToken,
    token_type: "bearer",
    expires_in: 3600,
  };

  const { password: _password, ...user } = found;
  return { tokens, user };
}

export function getUserFromToken(token: string): AuthenticatedUser | null {
  const userId = accessTokenMap.get(token);
  if (!userId) {
    return null;
  }
  const user = state.users.find((candidate) => candidate.id === userId);
  if (!user) {
    return null;
  }
  const { password: _pwd, ...safeUser } = user;
  return safeUser;
}

export function refreshMockToken(refreshToken: string): TokenPair | null {
  const userId = refreshTokenMap.get(refreshToken);
  if (!userId) {
    return null;
  }
  const accessToken = `mock-access-${randomUUID()}`;
  const newRefreshToken = `mock-refresh-${randomUUID()}`;
  accessTokenMap.set(accessToken, userId);
  refreshTokenMap.set(newRefreshToken, userId);
  return {
    access_token: accessToken,
    refresh_token: newRefreshToken,
    token_type: "bearer",
    expires_in: 3600,
  };
}
