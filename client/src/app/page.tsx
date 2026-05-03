"use client";

import { useState } from "react";
import Toolbar from "@/components/Toolbar";
import Canvas from "@/components/Canvas";
import ChatPanel from "@/components/ChatPanel";

export default function Home() {
  const [chatOpen, setChatOpen] = useState(true);

  return (
    <div className="app-layout">
      <Toolbar />
      <Canvas />
      <ChatPanel isOpen={chatOpen} onToggle={() => setChatOpen((v) => !v)} />
    </div>
  );
}
