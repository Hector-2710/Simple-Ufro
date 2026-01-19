import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { Lock, User } from 'lucide-react';

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const successMsg = location.state?.message;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await login(username, password);
            navigate('/');
        } catch (err) {
            setError('Credenciales inválidas');
        }
    };

    return (
        <div className="min-h-screen bg-[#0f172a] relative overflow-hidden flex items-center justify-center p-4">
            {/* Background Decorations */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-600/20 rounded-full blur-[120px] animate-pulse"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-cyan-500/10 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: '2s' }}></div>

            <div className="glass-card p-10 rounded-[2rem] w-full max-w-md relative z-10 animate-in">
                <div className="text-center mb-10">
                    <div className="inline-flex p-3 rounded-2xl bg-indigo-500/10 mb-4">
                        <User className="h-8 w-8 text-indigo-400" />
                    </div>
                    <h1 className="text-4xl font-bold text-white tracking-tight mb-3">Bienvenido</h1>
                    <p className="text-slate-400 font-light">Ingresa tus credenciales para continuar</p>
                </div>

                {successMsg && (
                    <div className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 p-4 rounded-xl mb-8 text-sm animate-in">
                        {successMsg}
                    </div>
                )}

                {error && (
                    <div className="bg-red-500/10 border border-red-500/20 text-red-300 p-4 rounded-xl mb-8 text-sm animate-in">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-8">
                    <div className="space-y-2">
                        <label className="block text-slate-300 text-sm font-medium ml-1">Usuario</label>
                        <div className="relative group">
                            <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-indigo-400 transition-colors w-5 h-5" />
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className="glass-input w-full pl-12 h-14"
                                placeholder="ej. usuario123"
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="block text-slate-300 text-sm font-medium ml-1">Contraseña</label>
                        <div className="relative group">
                            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-indigo-400 transition-colors w-5 h-5" />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="glass-input w-full pl-12 h-14"
                                placeholder="••••••••"
                                required
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="btn-premium w-full h-14 text-lg active:scale-95 transition-all"
                    >
                        Iniciar Sesión
                    </button>
                </form>

                <footer className="mt-10 text-center border-t border-white/5 pt-8">
                    <p className="text-slate-500 text-sm mb-2">
                        ¿No tienes una cuenta? <Link to="/register" className="text-indigo-400 hover:text-indigo-300 font-semibold transition-colors">Regístrate</Link>
                    </p>
                    <p className="text-slate-500 text-xs">
                        ¿Olvidaste tu contraseña? <span className="text-slate-400 hover:text-white cursor-pointer transition-colors">Recupérala</span>
                    </p>
                </footer>
            </div>
        </div>
    );
}
