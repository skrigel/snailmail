import { useState } from 'react';
import { syncGmail, calculateStats } from '@/lib/api';

type SyncStatus = 'idle' | 'syncing' | 'calculating' | 'complete' | 'error';

export function useMailSync() {
  const [status, setStatus] = useState<SyncStatus>('idle');
  const [error, setError] = useState<string | null>(null);

  const triggerSync = async (days = 30) => {
    try {
      setStatus('syncing');
      setError(null);
      await syncGmail(days);

      setStatus('calculating');
      await calculateStats(days);

      setStatus('complete');
    } catch (err) {
      setStatus('error');
      setError(err instanceof Error ? err.message : 'Sync failed');
    }
  };

  return { status, error, triggerSync };
}
