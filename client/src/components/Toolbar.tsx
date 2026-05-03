"use client";

import React, { useState } from "react";
import { CATEGORIES } from "@/lib/catalog";
import { useCatalogue } from "@/lib/api";
import { TriangleAlert } from "lucide-react";

export default function Toolbar() {
  const [activeCategory, setActiveCategory] = useState<string>("walls");
  const { items, loading, error } = useCatalogue();

  const filtered = items.filter((item) => item.category === activeCategory);

  const handleDragStart = (e: React.DragEvent, itemId: string) => {
    e.dataTransfer.setData("catalogId", itemId);
    e.dataTransfer.effectAllowed = "copy";
  };

  return (
    <aside className="toolbar">
      <nav className="category-nav">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.id}
            className={`cat-btn ${activeCategory === cat.id ? "active" : ""}`}
            onClick={() => setActiveCategory(cat.id)}
          >
            {cat.label}
          </button>
        ))}
      </nav>

      <div className="item-grid">
        {loading && (
          <div className="catalogue-state">
            <span className="state-spinner" />
            <span>Loading…</span>
          </div>
        )}
        {error && !loading && (
          <div className="catalogue-state">
            <span className="catalogue-error">
              <TriangleAlert size={16} /> Backend offline
            </span>
          </div>
        )}
        {!loading && !error && filtered.length === 0 && (
          <div className="catalogue-state">
            <span>No items</span>
          </div>
        )}
        {!loading &&
          !error &&
          filtered.map((item) => (
            <div
              key={item.id}
              className="item-card"
              draggable
              onDragStart={(e) => handleDragStart(e, item.id)}
              title={item.label}
            >
              <div
                className="item-preview"
                dangerouslySetInnerHTML={{ __html: item.svg }}
              />
              <span className="item-label">{item.label}</span>
            </div>
          ))}
      </div>
    </aside>
  );
}
