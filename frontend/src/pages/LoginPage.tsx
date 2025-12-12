import { FormEvent, useState } from "react";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export default function LoginPage() {
  const { setTokens } = useAuth();
  const [email, setEmail] = useState("demo@hospital.test");
  const [password, setPassword] = useState("P@ssw0rd!");
  const [code, setCode] = useState("");
  const [backupCode, setBackupCode] = useState("");
  const [message, setMessage] = useState("");
  const [provisioningUri, setProvisioningUri] = useState<string | null>(null);
  const [totpSecret, setTotpSecret] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMessage("");
    try {
      const payload = { email, password, code: code || undefined, backup_code: backupCode || undefined };
      const response = await api.post<LoginResponse | { detail: string; provisioning_uri?: string }>("/auth/login", payload, {
        validateStatus: () => true
      });

      if (response.status === 206) {
        const data = response.data as { detail: string; provisioning_uri?: string };
        setMessage(data.detail);
        if (data.provisioning_uri) setProvisioningUri(data.provisioning_uri);
        const headerSecret = response.headers["x-totp-secret"] as string | undefined;
        if (headerSecret) setTotpSecret(headerSecret);
        return;
      }

      if (response.status !== 200) {
        setMessage("Login o 2FA inválido");
        return;
      }

      const data = response.data as LoginResponse;
      setTokens(data.access_token, data.refresh_token, email);
      setMessage("Autenticado");
    } catch (err) {
      console.error(err);
      setMessage("Error inesperado");
    }
  };

  return (
    <section className="bg-gray-900 p-6 rounded-lg shadow-lg max-w-xl w-full">
      <h2 className="text-xl font-semibold mb-4">Login + 2FA</h2>
      <form className="flex flex-col gap-3" onSubmit={handleSubmit}>
        <input className="p-2 rounded bg-gray-800 border border-gray-700" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input className="p-2 rounded bg-gray-800 border border-gray-700" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
        <input className="p-2 rounded bg-gray-800 border border-gray-700" value={code} onChange={(e) => setCode(e.target.value)} placeholder="TOTP code" />
        <input className="p-2 rounded bg-gray-800 border border-gray-700" value={backupCode} onChange={(e) => setBackupCode(e.target.value)} placeholder="Backup code (opcional)" />
        <button className="bg-blue-500 hover:bg-blue-600 transition text-white font-semibold py-2 rounded" type="submit">
          Entrar
        </button>
      </form>
      {message && <p className="mt-3 text-sm text-gray-200">{message}</p>}
      {provisioningUri && (
        <div className="mt-3 text-xs text-gray-300 break-all">
          <p>Escanea el QR en tu app TOTP usando esta URI:</p>
          <p>{provisioningUri}</p>
        </div>
      )}
      {totpSecret && <p className="mt-2 text-xs text-gray-400">Secreto TOTP: {totpSecret}</p>}
    </section>
  );
}
