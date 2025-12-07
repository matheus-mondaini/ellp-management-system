-- ============================================
-- ELLP Management System - Database Schema v2
-- Abordagem Híbrida: users + especialização
-- ============================================

-- ========== CORE: Autenticação e Pessoas ==========

-- Tabela de usuários (autenticação e controle de acesso)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'professor', 'tutor', 'aluno')),
    ativo BOOLEAN DEFAULT true,
    ultimo_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Tabela de pessoas (dados comuns)
CREATE TABLE pessoas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    nome_completo VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    data_nascimento DATE,
    foto_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_pessoas_user ON pessoas(user_id);
CREATE INDEX idx_pessoas_nome ON pessoas(nome_completo);

-- ========== ESPECIALIZAÇÃO: Alunos ==========

CREATE TABLE alunos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pessoa_id UUID UNIQUE NOT NULL REFERENCES pessoas(id) ON DELETE CASCADE,
    
    -- Dados pessoais
    endereco_rua VARCHAR(255),
    endereco_numero VARCHAR(10),
    endereco_complemento VARCHAR(100),
    endereco_bairro VARCHAR(100),
    endereco_cidade VARCHAR(100),
    endereco_uf CHAR(2),
    endereco_cep VARCHAR(10),
    
    -- Dados escolares
    escola VARCHAR(255),
    serie VARCHAR(50),
    turno VARCHAR(20) CHECK (turno IN ('Manhã', 'Tarde', 'Integral', 'Noite') OR turno IS NULL),
    
    -- Dados do responsável (obrigatório)
    responsavel_nome VARCHAR(255) NOT NULL,
    responsavel_cpf VARCHAR(14),
    responsavel_email VARCHAR(255),
    responsavel_telefone VARCHAR(20) NOT NULL,
    responsavel_parentesco VARCHAR(50),
    responsavel_profissao VARCHAR(100),
    
    -- Observações
    observacoes TEXT,
    necessidades_especiais TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alunos_pessoa ON alunos(pessoa_id);
CREATE INDEX idx_alunos_escola ON alunos(escola);

-- ========== ESPECIALIZAÇÃO: Tutores ==========

CREATE TABLE tutores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pessoa_id UUID UNIQUE NOT NULL REFERENCES pessoas(id) ON DELETE CASCADE,
    
    -- Dados acadêmicos (se aluno da faculdade)
    faculdade VARCHAR(255),
    curso VARCHAR(255),
    semestre INTEGER,
    ra VARCHAR(50),
    email_educacional VARCHAR(255),
    
    -- Dados profissionais (se voluntário externo)
    profissao VARCHAR(255),
    empresa VARCHAR(255),
    linkedin VARCHAR(255),
    
    -- Controle de voluntariado
    tipo_vinculo VARCHAR(50) CHECK (tipo_vinculo IN ('Aluno UTFPR', 'Voluntário Externo', 'Outro')),
    data_inicio_voluntariado DATE,
    data_fim_voluntariado DATE,
    status_voluntariado VARCHAR(50) DEFAULT 'Ativo' CHECK (status_voluntariado IN ('Ativo', 'Inativo', 'Afastado')),
    
    -- Controle de carga horária
    carga_horaria_maxima_semanal INTEGER DEFAULT 20,
    carga_horaria_atual DECIMAL(5,2) DEFAULT 0.00,
    
    -- Observações
    areas_interesse TEXT,  -- Ex: "Scratch, Python, Robótica"
    observacoes TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tutores_pessoa ON tutores(pessoa_id);
CREATE INDEX idx_tutores_faculdade ON tutores(faculdade);
CREATE INDEX idx_tutores_status ON tutores(status_voluntariado);

-- ========== ESPECIALIZAÇÃO: Professores ==========

CREATE TABLE professores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pessoa_id UUID UNIQUE NOT NULL REFERENCES pessoas(id) ON DELETE CASCADE,
    
    -- Dados institucionais
    faculdade VARCHAR(255) NOT NULL,
    departamento VARCHAR(255),
    titulacao VARCHAR(100) CHECK (titulacao IN ('Graduação', 'Especialização', 'Mestrado', 'Doutorado', 'Pós-Doutorado')),
    email_institucional VARCHAR(255),
    segundo_email VARCHAR(255),
    
    -- Papel no ELLP
    coordenador BOOLEAN DEFAULT false,
    area_atuacao VARCHAR(255),  -- Ex: "Lógica de Programação", "Robótica Educacional"
    
    -- Observações
    observacoes TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_professores_pessoa ON professores(pessoa_id);
CREATE INDEX idx_professores_coordenador ON professores(coordenador);

-- ========== OFICINAS E TEMAS ==========

CREATE TABLE temas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL UNIQUE,
    descricao TEXT,
    cor_hex VARCHAR(7),  -- Ex: "#FF5733" para UI
    icone VARCHAR(50),   -- Nome do ícone (lucide-react)
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_temas_ativo ON temas(ativo);

CREATE TABLE oficinas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    objetivo TEXT,  -- Objetivo pedagógico
    
    -- Configurações
    carga_horaria INTEGER NOT NULL,  -- Horas totais
    capacidade_maxima INTEGER NOT NULL,
    numero_aulas INTEGER,  -- Quantas aulas/sessões terá
    
    -- Período
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    
    -- Local e horário
    local VARCHAR(255),
    dias_semana VARCHAR(100),  -- Ex: "Segunda, Quarta, Sexta"
    horario VARCHAR(50),       -- Ex: "14:00-16:00"
    
    -- Status
    status VARCHAR(50) DEFAULT 'planejada' CHECK (status IN ('planejada', 'inscricoes_abertas', 'em_andamento', 'concluida', 'cancelada')),
    
    -- Relações
    professor_id UUID REFERENCES professores(id) ON DELETE SET NULL,
    
    -- Contadores (desnormalizado para performance)
    total_inscritos INTEGER DEFAULT 0,
    total_concluintes INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Validações
    CONSTRAINT chk_datas CHECK (data_fim >= data_inicio),
    CONSTRAINT chk_capacidade CHECK (capacidade_maxima > 0)
);

CREATE INDEX idx_oficinas_status ON oficinas(status);
CREATE INDEX idx_oficinas_professor ON oficinas(professor_id);
CREATE INDEX idx_oficinas_datas ON oficinas(data_inicio, data_fim);

-- Relacionamento N:N entre oficinas e temas
CREATE TABLE oficina_temas (
    oficina_id UUID REFERENCES oficinas(id) ON DELETE CASCADE,
    tema_id UUID REFERENCES temas(id) ON DELETE CASCADE,
    PRIMARY KEY (oficina_id, tema_id)
);

-- Relacionamento N:N entre oficinas e tutores
CREATE TABLE oficina_tutores (
    oficina_id UUID REFERENCES oficinas(id) ON DELETE CASCADE,
    tutor_id UUID REFERENCES tutores(id) ON DELETE CASCADE,
    carga_horaria_oficina DECIMAL(5,2),  -- Horas dedicadas a esta oficina específica
    PRIMARY KEY (oficina_id, tutor_id)
);

CREATE INDEX idx_oficina_tutores_tutor ON oficina_tutores(tutor_id);

-- ========== INSCRIÇÕES E PRESENÇA ==========

CREATE TABLE inscricoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aluno_id UUID NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    oficina_id UUID NOT NULL REFERENCES oficinas(id) ON DELETE CASCADE,
    
    -- Controle
    data_inscricao TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'inscrito' CHECK (status IN ('inscrito', 'em_andamento', 'concluido', 'abandonou', 'cancelado')),
    
    -- Métricas (calculadas automaticamente)
    percentual_presenca DECIMAL(5,2) DEFAULT 0.00,
    total_aulas_previstas INTEGER DEFAULT 0,
    total_presencas INTEGER DEFAULT 0,
    total_faltas INTEGER DEFAULT 0,
    
    -- Certificado
    apto_certificado BOOLEAN DEFAULT false,  -- Calculado: presença >= 75% E status = concluido
    data_conclusao TIMESTAMP,
    
    -- Observações
    observacoes TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Garantir que aluno não se inscreva 2x na mesma oficina
    UNIQUE (aluno_id, oficina_id)
);

CREATE INDEX idx_inscricoes_aluno ON inscricoes(aluno_id);
CREATE INDEX idx_inscricoes_oficina ON inscricoes(oficina_id);
CREATE INDEX idx_inscricoes_status ON inscricoes(status);
CREATE INDEX idx_inscricoes_apto ON inscricoes(apto_certificado);

CREATE TABLE presencas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    inscricao_id UUID NOT NULL REFERENCES inscricoes(id) ON DELETE CASCADE,
    
    -- Data da aula/sessão
    data_aula DATE NOT NULL,
    numero_aula INTEGER,  -- 1, 2, 3, etc.
    
    -- Presença
    presente BOOLEAN NOT NULL,
    justificativa TEXT,  -- Se faltou, pode ter justificativa
    
    -- Observações do tutor
    observacao_tutor TEXT,
    registrado_por UUID REFERENCES users(id),  -- Quem registrou a presença
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Garantir que não haja duplicatas
    UNIQUE (inscricao_id, data_aula)
);

CREATE INDEX idx_presencas_inscricao ON presencas(inscricao_id);
CREATE INDEX idx_presencas_data ON presencas(data_aula);

-- ========== CERTIFICADOS ==========

CREATE TABLE certificados (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Pode ser certificado de aluno OU tutor (mutuamente exclusivos)
    inscricao_id UUID REFERENCES inscricoes(id) ON DELETE SET NULL,
    tutor_id UUID REFERENCES tutores(id) ON DELETE SET NULL,
    oficina_id UUID NOT NULL REFERENCES oficinas(id) ON DELETE SET NULL,
    
    -- Tipo
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('conclusao_aluno', 'participacao_tutor')),
    
    -- Validação
    hash_validacao VARCHAR(255) UNIQUE NOT NULL,
    codigo_verificacao VARCHAR(20) UNIQUE NOT NULL,  -- Código curto para validação (ex: ABC123XYZ)
    
    -- Arquivo
    arquivo_pdf_url TEXT,
    arquivo_pdf_nome VARCHAR(255),
    
    -- Datas
    data_emissao TIMESTAMP DEFAULT NOW(),
    valido_ate TIMESTAMP,  -- Pode ter validade (opcional)
    
    -- Métricas (duplicadas do momento da emissão para histórico)
    carga_horaria_certificada INTEGER,
    percentual_presenca_certificado DECIMAL(5,2),
    
    -- Controle
    revogado BOOLEAN DEFAULT false,
    data_revogacao TIMESTAMP,
    motivo_revogacao TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Garantir que inscricao_id OU tutor_id esteja preenchido (não ambos)
    CONSTRAINT chk_certificado_tipo CHECK (
        (tipo = 'conclusao_aluno' AND inscricao_id IS NOT NULL AND tutor_id IS NULL) OR
        (tipo = 'participacao_tutor' AND tutor_id IS NOT NULL AND inscricao_id IS NULL)
    )
);

CREATE INDEX idx_certificados_hash ON certificados(hash_validacao);
CREATE INDEX idx_certificados_codigo ON certificados(codigo_verificacao);
CREATE INDEX idx_certificados_inscricao ON certificados(inscricao_id);
CREATE INDEX idx_certificados_tutor ON certificados(tutor_id);
CREATE INDEX idx_certificados_tipo ON certificados(tipo);

-- ========== AUDITORIA ==========

CREATE TABLE auditoria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Quem fez a ação
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    user_email VARCHAR(255),  -- Duplicado para histórico
    user_role VARCHAR(50),
    
    -- O que foi feito
    acao VARCHAR(255) NOT NULL,  -- Ex: "CREATE", "UPDATE", "DELETE"
    entidade VARCHAR(100) NOT NULL,  -- Ex: "oficinas", "inscricoes", "certificados"
    entidade_id UUID,
    
    -- Detalhes (JSON)
    detalhes JSONB,
    
    -- Metadados
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_auditoria_user ON auditoria(user_id);
CREATE INDEX idx_auditoria_entidade ON auditoria(entidade, entidade_id);
CREATE INDEX idx_auditoria_created ON auditoria(created_at DESC);
CREATE INDEX idx_auditoria_acao ON auditoria(acao);

-- ========== VIEWS ==========

-- View: Tutores completos (facilita queries)
CREATE VIEW v_tutores_completos AS
SELECT 
    u.id as user_id,
    u.email,
    u.ativo,
    p.id as pessoa_id,
    p.nome_completo,
    p.telefone,
    p.data_nascimento,
    t.id as tutor_id,
    t.faculdade,
    t.curso,
    t.semestre,
    t.ra,
    t.email_educacional,
    t.tipo_vinculo,
    t.status_voluntariado,
    t.carga_horaria_maxima_semanal,
    t.carga_horaria_atual,
    t.data_inicio_voluntariado,
    t.data_fim_voluntariado
FROM users u
JOIN pessoas p ON u.id = p.user_id
JOIN tutores t ON p.id = t.pessoa_id;

-- View: Alunos completos
CREATE VIEW v_alunos_completos AS
SELECT 
    u.id as user_id,
    u.email,
    u.ativo,
    p.id as pessoa_id,
    p.nome_completo,
    p.telefone,
    p.data_nascimento,
    a.id as aluno_id,
    a.escola,
    a.serie,
    a.responsavel_nome,
    a.responsavel_email,
    a.responsavel_telefone,
    a.responsavel_parentesco,
    CONCAT(a.endereco_rua, ', ', a.endereco_numero, ' - ', a.endereco_bairro) as endereco_completo,
    a.endereco_cidade,
    a.endereco_uf
FROM users u
JOIN pessoas p ON u.id = p.user_id
JOIN alunos a ON p.id = a.pessoa_id;

-- View: Professores completos
CREATE VIEW v_professores_completos AS
SELECT 
    u.id as user_id,
    u.email,
    u.ativo,
    p.id as pessoa_id,
    p.nome_completo,
    p.telefone,
    prof.id as professor_id,
    prof.faculdade,
    prof.departamento,
    prof.titulacao,
    prof.email_institucional,
    prof.coordenador
FROM users u
JOIN pessoas p ON u.id = p.user_id
JOIN professores prof ON p.id = prof.pessoa_id;

-- View: Dashboard - Métricas gerais
CREATE VIEW v_dashboard_metricas AS
SELECT
    (SELECT COUNT(*) FROM oficinas WHERE status = 'em_andamento') as oficinas_ativas,
    (SELECT COUNT(*) FROM oficinas WHERE status = 'planejada') as oficinas_planejadas,
    (SELECT COUNT(*) FROM inscricoes WHERE status IN ('inscrito', 'em_andamento')) as inscricoes_ativas,
    (SELECT COUNT(*) FROM inscricoes WHERE status = 'concluido') as alunos_concluintes,
    (SELECT COUNT(*) FROM certificados WHERE tipo = 'conclusao_aluno' AND revogado = false) as certificados_alunos,
    (SELECT COUNT(*) FROM certificados WHERE tipo = 'participacao_tutor' AND revogado = false) as certificados_tutores,
    (SELECT AVG(percentual_presenca) FROM inscricoes WHERE status IN ('em_andamento', 'concluido')) as presenca_media_geral,
    (SELECT COUNT(*) FROM tutores WHERE status_voluntariado = 'Ativo') as tutores_ativos,
    (SELECT COUNT(*) FROM alunos) as total_alunos;

-- ========== FUNÇÕES E TRIGGERS ==========

-- Função: Atualizar percentual de presença automaticamente
CREATE OR REPLACE FUNCTION atualizar_percentual_presenca()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE inscricoes
    SET 
        percentual_presenca = (
            SELECT 
                CASE 
                    WHEN COUNT(*) = 0 THEN 0
                    ELSE (COUNT(*) FILTER (WHERE presente = true) * 100.0 / COUNT(*))
                END
            FROM presencas
            WHERE inscricao_id = NEW.inscricao_id
        ),
        total_presencas = (
            SELECT COUNT(*) FILTER (WHERE presente = true)
            FROM presencas
            WHERE inscricao_id = NEW.inscricao_id
        ),
        total_faltas = (
            SELECT COUNT(*) FILTER (WHERE presente = false)
            FROM presencas
            WHERE inscricao_id = NEW.inscricao_id
        )
    WHERE id = NEW.inscricao_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_atualizar_presenca
AFTER INSERT OR UPDATE ON presencas
FOR EACH ROW
EXECUTE FUNCTION atualizar_percentual_presenca();

-- Função: Verificar aptidão para certificado
CREATE OR REPLACE FUNCTION verificar_apto_certificado()
RETURNS TRIGGER AS $$
BEGIN
    -- Aluno está apto se: status = 'concluido' E presença >= 75%
    NEW.apto_certificado := (NEW.status = 'concluido' AND NEW.percentual_presenca >= 75.00);
    
    IF NEW.apto_certificado AND NEW.data_conclusao IS NULL THEN
        NEW.data_conclusao := NOW();
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_verificar_apto_certificado
BEFORE UPDATE ON inscricoes
FOR EACH ROW
WHEN (NEW.status IS DISTINCT FROM OLD.status OR NEW.percentual_presenca IS DISTINCT FROM OLD.percentual_presenca)
EXECUTE FUNCTION verificar_apto_certificado();

-- Função: Atualizar contador de inscritos na oficina
CREATE OR REPLACE FUNCTION atualizar_total_inscritos()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE oficinas
        SET total_inscritos = total_inscritos + 1
        WHERE id = NEW.oficina_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE oficinas
        SET total_inscritos = total_inscritos - 1
        WHERE id = OLD.oficina_id;
    END IF;
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_atualizar_total_inscritos
AFTER INSERT OR DELETE ON inscricoes
FOR EACH ROW
EXECUTE FUNCTION atualizar_total_inscritos();

-- Função: Atualizar contador de concluintes na oficina
CREATE OR REPLACE FUNCTION atualizar_total_concluintes()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'concluido' AND (OLD.status IS NULL OR OLD.status != 'concluido') THEN
        UPDATE oficinas
        SET total_concluintes = total_concluintes + 1
        WHERE id = NEW.oficina_id;
    ELSIF OLD.status = 'concluido' AND NEW.status != 'concluido' THEN
        UPDATE oficinas
        SET total_concluintes = total_concluintes - 1
        WHERE id = NEW.oficina_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_atualizar_total_concluintes
AFTER UPDATE ON inscricoes
FOR EACH ROW
WHEN (NEW.status IS DISTINCT FROM OLD.status)
EXECUTE FUNCTION atualizar_total_concluintes();

-- Função: Atualizar carga horária do tutor
CREATE OR REPLACE FUNCTION atualizar_carga_horaria_tutor()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE tutores
        SET carga_horaria_atual = (
            SELECT COALESCE(SUM(carga_horaria_oficina), 0)
            FROM oficina_tutores
            WHERE tutor_id = NEW.tutor_id
        )
        WHERE id = NEW.tutor_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE tutores
        SET carga_horaria_atual = (
            SELECT COALESCE(SUM(carga_horaria_oficina), 0)
            FROM oficina_tutores
            WHERE tutor_id = OLD.tutor_id
        )
        WHERE id = OLD.tutor_id;
    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE tutores
        SET carga_horaria_atual = (
            SELECT COALESCE(SUM(carga_horaria_oficina), 0)
            FROM oficina_tutores
            WHERE tutor_id = NEW.tutor_id
        )
        WHERE id = NEW.tutor_id;
    END IF;
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_atualizar_carga_tutor
AFTER INSERT OR UPDATE OR DELETE ON oficina_tutores
FOR EACH ROW
EXECUTE FUNCTION atualizar_carga_horaria_tutor();

-- ========== DADOS INICIAIS (SEED) ==========

-- Admin padrão (senha: admin123 - TROCAR EM PRODUÇÃO)
INSERT INTO users (email, senha_hash, role) 
VALUES ('admin@ellp.utfpr.edu.br', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIVInVket2', 'admin');

INSERT INTO pessoas (user_id, nome_completo, telefone)
VALUES (
    (SELECT id FROM users WHERE email = 'admin@ellp.utfpr.edu.br'),
    'Administrador ELLP',
    '43999999999'
);

-- Temas iniciais
INSERT INTO temas (nome, descricao, cor_hex, icone) VALUES
('Scratch Básico', 'Introdução à programação com Scratch', '#FF6B35', 'blocks'),
('Scratch Avançado', 'Projetos complexos com Scratch', '#FF8C42', 'puzzle'),
('Python para Crianças', 'Primeiros passos com Python', '#3A86FF', 'code'),
('Robótica Educacional', 'Construção e programação de robôs', '#8338EC', 'bot'),
('Lógica de Programação', 'Fundamentos de lógica e algoritmos', '#06FFA5', 'brain'),
('Desenvolvimento de Jogos', 'Criação de jogos digitais', '#FB5607', 'gamepad-2');
