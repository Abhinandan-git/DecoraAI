"use client";

import { useEffect, useState } from "react";
import { CatalogItem } from "./catalog";

interface UseCatalogueResult {
  items: CatalogItem[];
  loading: boolean;
  error: string | null;
}

export function useCatalogue(): UseCatalogueResult {
  const [items, setItems] = useState<CatalogItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetch("/api/catalogue")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data: CatalogItem[]) => {
        if (!cancelled) {
          setItems(data);
          setError(null);
        }
      })
      .catch((err: Error) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return { items, loading, error };
}
