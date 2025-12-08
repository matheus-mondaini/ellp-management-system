export default function NotFound() {
  return (
    <div className="space-y-4 text-center text-white">
      <p className="text-sm uppercase tracking-[0.4em] text-rose-300">Hash não encontrado</p>
      <p className="text-lg font-semibold">Nenhum certificado corresponde a esse identificador</p>
      <p className="text-sm text-slate-300">Verifique os caracteres e tente novamente.</p>
    </div>
  );
}
