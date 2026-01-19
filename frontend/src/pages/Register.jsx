import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/client';
import { User, Mail, Lock, UserPlus } from 'lucide-react';

export default function Register() {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        full_name: '',
        username: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            await api.post('/users/', {
                email: formData.email,
                password: formData.password,
                full_name: formData.full_name,
                username: formData.username
            });
            navigate('/login', { state: { message: '¡Cuenta creada con éxito! Ahora puedes iniciar sesión.' } });
        } catch (err) {
            setError(err.response?.data?.detail || 'Error al crear la cuenta. Por favor intenta de nuevo.');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <div className="min-h-screen bg-[#0f172a] relative overflow-hidden flex items-center justify-center p-4">
            {/* Background Decorations */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-600/20 rounded-full blur-[120px] animate-pulse"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-cyan-500/10 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: '2s' }}></div>

            <div className="glass-card p-10 rounded-[2rem] w-full max-w-md relative z-10 animate-in">
                <div className="text-center mb-8">
                    <div className="inline-flex p-3 rounded-2xl bg-indigo-500/10 mb-4">
                        <UserPlus className="h-8 w-8 text-indigo-400" />
                    </div>
                    <h1 className="text-4xl font-bold text-white tracking-tight mb-3">Crear Cuenta</h1>
                    <p className="text-slate-400 font-light">Únete a nuestra plataforma académica</p>
                </div>

                {error && (
                    <div className="bg-red-500/10 border border-red-500/20 text-red-300 p-4 rounded-xl mb-6 text-sm animate-in">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-5">
                    <div className="space-y-2">
                        <label className="block text-slate-300 text-sm font-medium ml-1">Nombre Completo</label>
                        <div className="relative group">
                            <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-indigo-400 transition-colors w-5 h-5" />
                            <input
                                name="full_name"
                                type="text"
                                value={formData.full_name}
                                onChange={handleChange}
                                className="glass-input w-full pl-12 h-12"
                                placeholder="Juan Pérez"
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="block text-slate-300 text-sm font-medium ml-1">Nombre de Usuario</label>
                        <div className="relative group">
                            <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-indigo-400 transition-colors w-5 h-5" />
                            <input
                                name="username"
                                type="text"
                                value={formData.username}
                                onChange={handleChange}
                                className="glass-input w-full pl-12 h-12"
                                placeholder="juanito123"
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="block text-slate-300 text-sm font-medium ml-1">Email</label>
                        <div className="relative group">
                            <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-indigo-400 transition-colors w-5 h-5" />
                            <input
                                name="email"
                                type="email"
                                value={formData.email}
                                onChange={handleChange}
                                className="glass-input w-full pl-12 h-12"
                                placeholder="tu@email.com"
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="block text-slate-300 text-sm font-medium ml-1">Contraseña</label>
                        <div className="relative group">
                            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-indigo-400 transition-colors w-5 h-5" />
                            <input
                                name="password"
                                type="password"
                                value={formData.password}
                                onChange={handleChange}
                                className="glass-input w-full pl-12 h-12"
                                placeholder="••••••••"
                                required
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="btn-premium w-full h-14 text-lg active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed mt-4"
                    >
                        {loading ? 'Creando cuenta...' : 'Registrarse'}
                    </button>
                </form>

                <footer className="mt-8 text-center border-t border-white/5 pt-6">
                    <p className="text-slate-500 text-sm">
                        ¿Ya tienes cuenta? <Link to="/login" className="text-indigo-400 hover:text-indigo-300 font-semibold transition-colors">Inicia sesión</Link>
                    </p>
                </footer>
            </div>
        </div>
    );
}
