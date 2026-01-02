import { createContext } from "react";

const MailContext = createContext({
    isAuthenticated: false,
    user: null,
    syncStatus: 'idle',
    checkAuth: async () => {},
    triggerSync: async (days = 30) => {
      // 1. Call sync endpoint
      // 2. Wait or poll for completion
      // 3. Call calculate endpoint
      // 4. Update syncStatus
    },
    logout: async () => {}
  });


//  State to manage:
//   - isAuthenticated: boolean
//   - user: { id, username, email } | null
//   - syncStatus: 'idle' | 'syncing' | 'calculating' | 'complete' | 'error'
//   - syncError: string | null