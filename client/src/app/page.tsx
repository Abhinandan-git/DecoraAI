"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import Toolbar from "@/components/Toolbar";
import Canvas from "@/components/Canvas";
import ChatPanel from "@/components/ChatPanel";
import AppHeader from "@/components/AppHeader";

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [chatOpen] = useState(true);

  useEffect(() => {
    if (!loading && !user) router.replace("/login");
  }, [user, loading, router]);

  // Show nothing while checking auth (middleware handles the redirect, this is a safety net)
  if (loading || !user) {
    return (
      <div className="auth-loading">
        <span className="auth-loading-spinner" />
      </div>
    );
  }

  return (
    <div className="app-shell">
      <AppHeader />
      <div className="app-layout">
        <Toolbar />
        <Canvas />
        <ChatPanel isOpen={chatOpen} />
      </div>
    </div>
  );
}
