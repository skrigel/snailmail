import { useState, useEffect } from 'react';
import { getDailyStats } from '@/lib/api';

export interface DailyStat {
  id: number;
  date: string;
  inbox_count: number;
  sent_count: number;
  work: number;
  personal: number;
  promotions: number;
}

export function useGetStats() {
  const [stats, setStats] = useState<DailyStat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const data = await getDailyStats();
      setStats(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch stats');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return {
    stats,
    loading,
    error,
    refetch: fetchStats,
  };
}