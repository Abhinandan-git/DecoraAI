"use client";

import { useAuth } from "@/lib/authContext";
import {Birdhouse} from "lucide-react";

export default function AppHeader() {
  const { user, logout } = useAuth();

  if (!user) return null;

  // Get initials for avatar
  const initials = user.name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  return (
    <header className="app-header">
      <div className="app-header-brand">
        <span className="app-header-logo"><Birdhouse /></span>
        <span className="app-header-title">DecoraAI</span>
      </div>

      <div className="app-header-user">
        <span className="app-header-email">{user.email}</span>
        <div className="app-header-avatar" title={user.name}>
          {initials}
        </div>
        <button className="app-header-logout" onClick={logout} title="Sign out">
          ↪ Sign out
        </button>
      </div>
    </header>
  );
}
