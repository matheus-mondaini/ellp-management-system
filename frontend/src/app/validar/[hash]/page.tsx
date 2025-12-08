type Params = {
  params: {
    hash: string;
  };
};

export default function CertificateValidationPage({ params }: Params) {
  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold text-slate-900">Validação de Certificado</h1>
      <p className="text-sm text-slate-600">
        Hash consultado: <span className="font-mono text-slate-900">{params.hash}</span>
      </p>
      <p className="text-sm text-slate-600">
        Esta página consumirá o endpoint público{' '}
        <code className="font-mono text-slate-900">GET /certificados/validar/&lt;hash&gt;</code>.
      </p>
    </section>
  );
}
