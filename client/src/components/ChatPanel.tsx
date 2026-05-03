"use client";

import React, { useCallback, useEffect, useRef, useState } from "react";
import {
  Bot,
  BotMessageSquare,
  MoveDiagonal,
  SendHorizontal,
} from "lucide-react";

// ── Types ─────────────────────────────────────────────────────────────────────

type MessageRole = "user" | "assistant" | "system";

interface TextMessage {
  id: string;
  role: MessageRole;
  kind: "text";
  content: string;
}

interface ImageMessage {
  id: string;
  role: "assistant";
  kind: "image";
  dataUrl: string;
  prompt: string;
}

type ChatMessage = TextMessage | ImageMessage;

// ── Helpers ───────────────────────────────────────────────────────────────────

let msgCounter = 0;
function makeId() {
  return `msg-${++msgCounter}`;
}

const IMAGE_COMMAND = /^\/image\s+(.+)$/i;

// ── Draggable image bubble ────────────────────────────────────────────────────

interface ImageBubbleProps {
  message: ImageMessage;
}

function ImageBubble({ message }: ImageBubbleProps) {
  const handleDragStart = (e: React.DragEvent) => {
    e.dataTransfer.setData("chatImageDataUrl", message.dataUrl);
    e.dataTransfer.setData("chatImageLabel", message.prompt);
    e.dataTransfer.effectAllowed = "copy";
  };

  return (
    <div className="chat-image-bubble">
      <div className="chat-image-prompt">
        <span className="chat-image-prompt-icon">
          <BotMessageSquare />
        </span>
        <span>{message.prompt}</span>
      </div>
      <div
        className="chat-image-wrapper"
        draggable
        onDragStart={handleDragStart}
        title="Drag to canvas"
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={message.dataUrl}
          alt={message.prompt}
          className="chat-image"
        />
        <div className="chat-image-drag-hint">
          <span>
            <MoveDiagonal size={14} /> Drag to canvas
          </span>
        </div>
      </div>
    </div>
  );
}

// ── Main Chat component ───────────────────────────────────────────────────────

interface ChatPanelProps {
  isOpen: boolean;
}

export default function ChatPanel({ isOpen }: ChatPanelProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: makeId(),
      role: "assistant",
      kind: "text",
      content:
        "Hi! Ask me anything about your floor plan, or type **/image <description>** to generate a reference image you can drag onto the canvas.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const pushMessage = useCallback((msg: ChatMessage) => {
    setMessages((prev) => [...prev, msg]);
  }, []);

  // ── Send handler ────────────────────────────────────────────────────────────

  const handleSend = useCallback(async () => {
    const text = input.trim();
    if (!text || loading) return;
    setInput("");

    // Push user message
    pushMessage({ id: makeId(), role: "user", kind: "text", content: text });
    setLoading(true);

    try {
      const imageMatch = text.match(IMAGE_COMMAND);

      if (imageMatch) {
        // ── /image command ────────────────────────────────────────────────────
        const prompt = imageMatch[1].trim();

        const res = await fetch(
          `/api/background-image?prompt=${encodeURIComponent(prompt)}`,
          { cache: "no-store" },
        );
        if (!res.ok) throw new Error(`Server error ${res.status}`);
        const data = await res.json();

        if (data.error) throw new Error(data.error);

        pushMessage({
          id: makeId(),
          role: "assistant",
          kind: "image",
          dataUrl: data.dataUrl,
          prompt,
        });
      } else {
        // ── regular chat ──────────────────────────────────────────────────────
        const res = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text }),
        });
        if (!res.ok) throw new Error(`Server error ${res.status}`);
        const data = await res.json();

        if (data.error) throw new Error(data.error);

        pushMessage({
          id: makeId(),
          role: "assistant",
          kind: "text",
          content: data.reply ?? "…",
        });
      }
    } catch (err) {
      pushMessage({
        id: makeId(),
        role: "assistant",
        kind: "text",
        content: `⚠ ${err instanceof Error ? err.message : "Something went wrong"}`,
      });
    } finally {
      setLoading(false);
    }
  }, [input, loading, pushMessage]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Auto-resize textarea
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    const ta = e.target;
    ta.style.height = "auto";
    ta.style.height = `${Math.min(ta.scrollHeight, 120)}px`;
  };

  return (
    <div
      className={`chat-panel ${isOpen ? "chat-panel--open" : "chat-panel--closed"}`}
    >
      {isOpen && (
        <>
          {/* Header */}
          <div className="chat-header">
            <span className="chat-header-icon">
              <Bot />
            </span>
            <span className="chat-header-title">Assistant</span>
            <span className="chat-header-hint">
              Try <code>/image kitchen plan</code>
            </span>
          </div>

          {/* Messages */}
          <div className="chat-messages">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`chat-bubble chat-bubble--${msg.role}`}
              >
                {msg.kind === "image" ? (
                  <ImageBubble message={msg} />
                ) : (
                  <p className="chat-text">{msg.content}</p>
                )}
              </div>
            ))}

            {loading && (
              <div className="chat-bubble chat-bubble--assistant">
                <div className="chat-typing">
                  <span />
                  <span />
                  <span />
                </div>
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="chat-input-area">
            <textarea
              ref={inputRef}
              className="chat-input"
              value={input}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              placeholder="Ask something… or /image <prompt>"
              rows={1}
              disabled={loading}
            />
            <button
              className="chat-send"
              onClick={handleSend}
              disabled={loading || !input.trim()}
              aria-label="Send"
            >
              <SendHorizontal />
            </button>
          </div>
        </>
      )}
    </div>
  );
}
