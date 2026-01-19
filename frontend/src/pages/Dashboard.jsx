import { useEffect, useState } from 'react';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';
import { BookOpen, Calendar, GraduationCap, LogOut } from 'lucide-react';

export default function Dashboard() {
    const { user, logout } = useAuth();
    const [subjects, setSubjects] = useState([]);
    const [grades, setGrades] = useState([]);
    const [schedule, setSchedule] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [subjectsRes, gradesRes, scheduleRes] = await Promise.all([
                    api.get('/academic/subjects'),
                    api.get('/academic/grades'),
                    api.get('/academic/schedule')
                ]);
                setSubjects(subjectsRes.data);
                setGrades(gradesRes.data);
                setSchedule(scheduleRes.data);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-900 flex items-center justify-center">
                <div className="animate-pulse flex flex-col items-center">
                    <div className="h-12 w-12 bg-blue-500 rounded-full mb-4"></div>
                    <p className="text-slate-400">Cargando información académica...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0f172a] text-slate-100 font-sans selection:bg-indigo-500/30">
            {/* Navbar */}
            <nav className="glass-card !bg-slate-900/60 backdrop-blur-xl border-x-0 border-t-0 sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-6 lg:px-8">
                    <div className="flex items-center justify-between h-20">
                        <div className="flex items-center gap-4">
                            <div className="bg-gradient-to-tr from-indigo-600 to-cyan-400 p-2.5 rounded-xl shadow-lg shadow-indigo-500/20">
                                <GraduationCap className="h-6 w-6 text-white" />
                            </div>
                            <div>
                                <h2 className="font-bold text-xl tracking-tight text-white leading-none">MiPortal</h2>
                                <p className="text-[10px] uppercase tracking-widest text-indigo-400 font-bold mt-1">Academic Suite</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-6">
                            <div className="hidden sm:flex flex-col items-end mr-2">
                                <span className="text-sm font-medium text-white">{user?.username || 'Usuario'}</span>
                                <span className="text-[10px] text-slate-500 uppercase tracking-wider">Estudiante Regular</span>
                            </div>
                            <button
                                onClick={logout}
                                className="group flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium text-slate-300 hover:text-white bg-white/5 hover:bg-red-500/10 border border-white/5 hover:border-red-500/20 transition-all"
                            >
                                <LogOut className="h-4 w-4 group-hover:translate-x-0.5 transition-transform" />
                                <span>Salir</span>
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            <main className="max-w-7xl mx-auto px-6 lg:px-8 py-12">
                <header className="mb-12 animate-in">
                    <h1 className="text-5xl font-bold text-white mb-3 tracking-tight">Resumen Académico</h1>
                    <p className="text-slate-400 text-lg font-light">Bienvenido de vuelta. Aquí está tu progreso y próximas actividades.</p>
                </header>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Main Content Area */}
                    <div className="lg:col-span-2 space-y-8">
                        {/* Subjects Card */}
                        <section className="glass-card p-8 rounded-[2rem] animate-in" style={{ animationDelay: '0.1s' }}>
                            <div className="flex items-center justify-between mb-8">
                                <div className="flex items-center gap-4">
                                    <div className="p-3 bg-indigo-500/10 rounded-2xl text-indigo-400">
                                        <BookOpen className="h-6 w-6" />
                                    </div>
                                    <div>
                                        <h2 className="text-xl font-bold text-white">Asignaturas</h2>
                                        <p className="text-sm text-slate-500">Cursos inscritos este semestre</p>
                                    </div>
                                </div>
                                <span className="bg-indigo-500/10 text-indigo-400 text-xs font-bold px-3 py-1 rounded-full border border-indigo-500/20">
                                    {subjects.length} Total
                                </span>
                            </div>

                            <div className="grid gap-5 sm:grid-cols-2">
                                {subjects.map((sub, idx) => (
                                    <div key={idx} className="group relative bg-[#1e293b]/40 p-6 rounded-2xl border border-white/5 hover:border-indigo-500/30 transition-all hover:shadow-2xl hover:shadow-indigo-500/5 hover:-translate-y-1">
                                        <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <div className="h-2 w-2 rounded-full bg-indigo-500 blur-[2px]"></div>
                                        </div>
                                        <h3 className="font-semibold text-lg text-white mb-1 group-hover:text-indigo-300 transition-colors uppercase tracking-tight">{sub.name}</h3>
                                        <p className="text-xs font-mono text-slate-500 tracking-wider uppercase">{sub.code}</p>
                                    </div>
                                ))}
                                {subjects.length === 0 && (
                                    <div className="col-span-full py-12 text-center bg-slate-800/20 rounded-2xl border border-dashed border-slate-700">
                                        <p className="text-slate-500 italic">No hay asignaturas inscritas en tu currículo.</p>
                                    </div>
                                )}
                            </div>
                        </section>

                        {/* Schedule Card */}
                        <section className="glass-card p-8 rounded-[2rem] animate-in" style={{ animationDelay: '0.2s' }}>
                            <div className="flex items-center gap-4 mb-8">
                                <div className="p-3 bg-cyan-500/10 rounded-2xl text-cyan-400">
                                    <Calendar className="h-6 w-6" />
                                </div>
                                <div>
                                    <h2 className="text-xl font-bold text-white">Agenda Semanal</h2>
                                    <p className="text-sm text-slate-500">Próximos bloques de clases</p>
                                </div>
                            </div>

                            <div className="grid gap-3">
                                {schedule.map((item, idx) => (
                                    <div key={idx} className="flex items-center justify-between p-5 rounded-2xl bg-white/5 border border-white/5 hover:bg-white/[0.08] transition-colors group">
                                        <div className="flex items-center gap-6">
                                            <div className="flex flex-col items-center justify-center w-14 h-14 rounded-xl bg-slate-900 border border-white/5 group-hover:border-cyan-500/30 transition-colors">
                                                <span className="text-[10px] font-bold text-slate-500 uppercase leading-none">{item.day.substring(0, 3)}</span>
                                            </div>
                                            <div>
                                                <span className="text-white font-medium block mb-1">{item.subject_name}</span>
                                                <div className="flex items-center gap-2">
                                                    <div className="h-1.5 w-1.5 rounded-full bg-cyan-500"></div>
                                                    <span className="text-xs text-slate-500 font-mono">{item.start_time} - {item.end_time}</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                                {schedule.length === 0 && (
                                    <div className="py-10 text-center text-slate-500 italic">Tu agenda está despejada por ahora.</div>
                                )}
                            </div>
                        </section>
                    </div>

                    {/* Sidebar: Performance */}
                    <aside className="lg:col-span-1">
                        <div className="glass-card p-8 rounded-[2rem] h-full animate-in" style={{ animationDelay: '0.3s' }}>
                            <div className="flex items-center gap-4 mb-10">
                                <div className="p-3 bg-emerald-500/10 rounded-2xl text-emerald-400">
                                    <GraduationCap className="h-6 w-6" />
                                </div>
                                <div>
                                    <h2 className="text-xl font-bold text-white">Rendimiento</h2>
                                    <p className="text-sm text-slate-500">Promedio y calificaciones</p>
                                </div>
                            </div>

                            <div className="space-y-8">
                                {grades.map((grade, idx) => (
                                    <div key={idx} className="relative group">
                                        <div className="flex justify-between items-end mb-3">
                                            <span className="text-sm font-semibold text-slate-400 group-hover:text-white transition-colors uppercase tracking-tight">{grade.subject_name}</span>
                                            <span className={`text-2xl font-black italic tracking-tighter ${grade.value >= 4.0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                                                {grade.value.toFixed(1)}
                                            </span>
                                        </div>
                                        <div className="w-full bg-slate-800/80 h-2.5 rounded-full overflow-hidden border border-white/5 p-[1px]">
                                            <div
                                                className={`h-full rounded-full transition-all duration-1000 ease-out shadow-[0_0_12px_rgba(16,185,129,0.3)] ${grade.value >= 4.0 ? 'bg-gradient-to-r from-emerald-600 to-teal-400' : 'bg-gradient-to-r from-rose-600 to-pink-400'}`}
                                                style={{ width: `${(grade.value / 7.0) * 100}%` }}
                                            ></div>
                                        </div>
                                    </div>
                                ))}
                                {grades.length === 0 && (
                                    <div className="py-12 text-center text-slate-500 italic">Aún no hay registros de evaluación.</div>
                                )}
                            </div>

                            <div className="mt-12 pt-8 border-t border-white/5 text-center">
                                <div className="inline-block p-6 rounded-3xl bg-indigo-500/5 border border-indigo-500/10">
                                    <p className="text-[10px] text-indigo-400 font-bold uppercase tracking-[0.2em] mb-1">Carga Académica</p>
                                    <p className="text-3xl font-black text-white italic">NORMAL</p>
                                </div>
                            </div>
                        </div>
                    </aside>
                </div>
            </main>
        </div>
    );
}
