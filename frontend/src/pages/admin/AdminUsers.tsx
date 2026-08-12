import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { ArrowLeft, UserCheck, UserX, Shield, ShieldAlert, Search, UserPlus, Trash2 } from 'lucide-react';

interface AdminUsersProps {
  onBack: () => void;
}

export const AdminUsers: React.FC<AdminUsersProps> = ({ onBack }) => {
  const [users, setUsers] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  const loadUsers = async () => {
    try {
      const data = await api.getAdminUsers();
      setUsers(data);
    } catch (e) {
      console.error("Failed loading users", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleToggleStatus = async (uid: string, currentStatus: boolean) => {
    try {
      await api.toggleUserStatus(uid, !currentStatus);
      loadUsers();
    } catch (e: any) {
      alert(e.message || "Action failed");
    }
  };

  const handleUpdateRole = async (uid: string, currentRole: string) => {
    const newRole = currentRole === 'ADMIN' ? 'USER' : 'ADMIN';
    const confirmText = newRole === 'ADMIN' 
      ? "Promote this student to Platform Administrator?" 
      : "Demote this Admin to standard Student role?";
      
    if (window.confirm(confirmText)) {
      try {
        await api.updateUserRole(uid, newRole);
        loadUsers();
      } catch (e: any) {
        alert(e.message || "Role change failed");
      }
    }
  };

  const handleDeleteUser = async (uid: string, email: string) => {
    if (window.confirm(`Are you sure you want to PERMANENTLY DELETE the account for ${email}? This action cannot be undone.`)) {
      try {
        await api.deleteUser(uid);
        loadUsers();
      } catch (e: any) {
        alert(e.message || "Delete user failed");
      }
    }
  };

  const filteredUsers = users.filter(u => 
    u.email.toLowerCase().includes(searchTerm.toLowerCase()) || 
    u.display_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      <button onClick={onBack} className="flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white">
        <ArrowLeft className="w-4 h-4" /> Back to Admin Overview
      </button>

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white">User Management &amp; Admin Privileges</h1>
          <p className="text-xs text-slate-400">Manage user accounts, monitor progress, promote admins, or delete accounts.</p>
        </div>

        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search email or name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-sm text-slate-200"
          />
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : (
        <div className="glass-panel rounded-2xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-900/80 text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">User</th>
                  <th className="py-3 px-4">Role</th>
                  <th className="py-3 px-4">Attempted</th>
                  <th className="py-3 px-4">Avg Score</th>
                  <th className="py-3 px-4">Account Status</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {filteredUsers.map((u) => (
                  <tr key={u.uid} className="hover:bg-slate-900/40">
                    <td className="py-3.5 px-4">
                      <p className="font-bold text-white text-sm">{u.display_name}</p>
                      <p className="text-xs text-slate-400">{u.email}</p>
                    </td>
                    <td className="py-3.5 px-4">
                      {u.role === 'ADMIN' ? (
                        <span className="px-2.5 py-0.5 rounded text-xs font-bold bg-purple-500/10 text-purple-400 border border-purple-500/20 inline-flex items-center gap-1">
                          <Shield className="w-3 h-3" /> ADMIN
                        </span>
                      ) : (
                        <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-slate-800 text-slate-300">
                          STUDENT
                        </span>
                      )}
                    </td>
                    <td className="py-3.5 px-4 text-xs font-semibold text-slate-300">
                      {u.metrics?.total_attempted || 0}
                    </td>
                    <td className="py-3.5 px-4 font-bold text-emerald-400">
                      {u.metrics?.average_score || 0}%
                    </td>
                    <td className="py-3.5 px-4">
                      {u.is_disabled ? (
                        <span className="px-2 py-0.5 rounded text-xs font-bold bg-rose-500/10 text-rose-400">Disabled</span>
                      ) : (
                        <span className="px-2 py-0.5 rounded text-xs font-bold bg-emerald-500/10 text-emerald-400">Active</span>
                      )}
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        {/* Promote / Demote Role Button */}
                        <button
                          onClick={() => handleUpdateRole(u.uid, u.role)}
                          className={`px-2.5 py-1 rounded-lg text-xs font-bold flex items-center gap-1 transition-all ${
                            u.role === 'ADMIN'
                              ? 'bg-purple-950/40 text-purple-300 border border-purple-500/30 hover:bg-purple-900/40'
                              : 'bg-blue-600/20 text-blue-300 border border-blue-500/30 hover:bg-blue-600/30'
                          }`}
                        >
                          {u.role === 'ADMIN' ? (
                            <><ShieldAlert className="w-3.5 h-3.5 text-purple-400" /> Demote</>
                          ) : (
                            <><UserPlus className="w-3.5 h-3.5 text-blue-400" /> Make Admin</>
                          )}
                        </button>

                        {/* Enable / Disable Status Button */}
                        {u.role !== 'ADMIN' && (
                          <button
                            onClick={() => handleToggleStatus(u.uid, u.is_disabled)}
                            className={`px-2 py-1 rounded-lg text-xs font-bold flex items-center gap-1 ${
                              u.is_disabled
                                ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-600/30'
                                : 'bg-amber-600/20 text-amber-400 border border-amber-500/30 hover:bg-amber-600/30'
                            }`}
                          >
                            {u.is_disabled ? (
                              <><UserCheck className="w-3.5 h-3.5" /> Enable</>
                            ) : (
                              <><UserX className="w-3.5 h-3.5" /> Disable</>
                            )}
                          </button>
                        )}

                        {/* Delete Account Button */}
                        {u.role !== 'ADMIN' && (
                          <button
                            onClick={() => handleDeleteUser(u.uid, u.email)}
                            className="px-2.5 py-1 bg-rose-600/20 text-rose-400 border border-rose-500/30 hover:bg-rose-600/30 rounded-lg text-xs font-bold flex items-center gap-1 transition-all"
                            title="Permanently Delete Account"
                          >
                            <Trash2 className="w-3.5 h-3.5" /> Delete
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

    </div>
  );
};
