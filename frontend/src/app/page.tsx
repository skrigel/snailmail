"use client";

import { useState, useMemo, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from '@/components/ui/carousel';
import type { DailyAnalytics } from '@/lib/types';
import Snail from '@/components/snail';
import AnalyticsDialog from '@/components/analytics-dialog';
import SnailMailIcon from '@/components/icons/snail-mail-icon';
import { CalendarDays, Mail, Reply, Clock, LogIn, LogOut, RefreshCw } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useGetStats } from '@/hooks/useGetStats';
import { useMailSync } from '@/hooks/useMailSync';
import { convertStatToAnalytics, getMockAnalytics } from '@/lib/utils/analytics';
  
export default function Home() {
  const { isAuthenticated, user, loading, login, logout } = useAuth();
  const { stats, loading: statsLoading, refetch } = useGetStats();
  const { status: syncStatus, error: syncError, triggerSync } = useMailSync();

  const [selectedSnail, setSelectedSnail] = useState<DailyAnalytics | null>(null);

  // Use real data if authenticated and available, otherwise use mock data
  const allData = useMemo(() => {
    if (isAuthenticated && stats.length > 0) {
      return stats.map((stat, index) => convertStatToAnalytics(stat, index));
    }
    return getMockAnalytics();
  }, [isAuthenticated, stats]);

  // Split into today's race (last 2 days) and historical (rest)
  const dailyData = allData.slice(0, 7);
  const historicalData = allData.slice(2);

  const handleSync = async () => {
    await triggerSync(30);
  };

  // Refetch stats when sync completes
  useEffect(() => {
    if (syncStatus === 'complete') {
      // Wait a moment for backend to finish processing
      setTimeout(() => {
        refetch();
      }, 2000);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [syncStatus]);

  return (
    <div className={"flex flex-col min-h-screen bg-background"}>
      <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 py-4">
        <div className={"container flex items-center justify-between"}>
          <div className="flex items-center space-x-4">
            <SnailMailIcon className={"h-8 w-8"} />
            <h1 className={"text-2xl font-bold font-headline tracking-tighter"}>Snail Mail Analytics</h1>
          </div>

          <div className="flex items-center gap-4">
            {loading ? (
              <span className="text-sm text-muted-foreground">Loading...</span>
            ) : isAuthenticated && user ? (
              <>
                <span className="text-sm">
                  Welcome, <strong>{user.username}</strong>
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleSync}
                  disabled={syncStatus === 'syncing' || syncStatus === 'calculating'}
                >
                  <RefreshCw className={`w-4 h-4 mr-2 ${syncStatus === 'syncing' || syncStatus === 'calculating' ? 'animate-spin' : ''}`} />
                  {syncStatus === 'syncing' ? 'Syncing...' : syncStatus === 'calculating' ? 'Calculating...' : 'Sync Gmail'}
                </Button>
                <Button variant="outline" size="sm" onClick={logout}>
                  <LogOut className="w-4 h-4 mr-2" />
                  Logout
                </Button>
              </>
            ) : (
              <Button onClick={login}>
                <LogIn className="w-4 h-4 mr-2" />
                Login with Google
              </Button>
            )}
          </div>
        </div>
      </header>
      
      <main className={"flex-1 container mx-auto p-4 md:p-8 space-y-12"}>
        {syncError && (
          <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded">
            <strong>Sync Error:</strong> {syncError}
          </div>
        )}

        {!isAuthenticated && (
          <div className="bg-muted/50 border border-border px-4 py-3 rounded text-center">
            <p className="text-sm text-muted-foreground">
              You're viewing demo data. <button onClick={login} className="underline font-medium">Login with Google</button> to see your real email analytics!
            </p>
          </div>
        )}

        <section>
          <Card className={"overflow-hidden"}>
            <CardHeader>
              <CardTitle className="font-headline text-3xl tracking-tighter">Today's Snail Race</CardTitle>
              <CardDescription>
                {isAuthenticated ? 'Your inbox activity over the last few days.' : 'A visual comparison of your inbox activity (demo data).'}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="relative space-y-4 pr-12 md:pr-24">
                {dailyData.map((data) => (
                  <div key={data.id} className="w-full h-20 bg-secondary/50 rounded-lg border p-2 flex items-center group">
                     <div 
                      className="transition-transform duration-1000 ease-out" 
                      style={{ transform: `translateX(calc(${data.progress * 0.9}%))` }}
                    >
                      <Snail 
                        analytics={data} 
                        onClick={() => setSelectedSnail(data)} 
                      />
                    </div>
                    <span className="absolute left-3 font-mono text-sm text-muted-foreground">{data.dayOfWeek.slice(0,3)}</span>
                  </div>
                ))}
                <div className="absolute top-0 right-4 h-full border-r-4 border-dashed border-primary-foreground/50 flex flex-col justify-between py-2">
                   <SnailMailIcon className="h-6 w-6 text-primary -translate-x-1/2 -translate-y-2"/>
                   <span className="font-mono text-xs -rotate-90 text-muted-foreground whitespace-nowrap">Finish Line</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>

        <section>
          <h2 className="text-3xl font-bold font-headline tracking-tighter mb-4">Historical Timeline</h2>
          <Carousel opts={{ align: "start" }} className="w-full">
            <CarouselContent>
              {historicalData.map((data) => (
                <CarouselItem key={data.id} className="md:basis-1/2 lg:basis-1/3">
                  <div className="p-1">
                    <Card>
                      <CardHeader>
                        <div className="flex justify-between items-start">
                           <div>
                            <CardTitle className="font-headline flex items-center gap-2"><CalendarDays className="w-5 h-5 text-muted-foreground" /> {data.date}</CardTitle>
                            <CardDescription>{data.dayOfWeek}</CardDescription>
                           </div>
                           <div className="w-12 h-12">
                            <Snail analytics={data} isStatic={true} />
                           </div>
                        </div>
                      </CardHeader>
                      <CardContent className="grid grid-cols-3 gap-2 text-sm">
                        <div className="flex items-center gap-2">
                          <Mail className="w-4 h-4 text-muted-foreground" />
                          {/* <span>{data.emailsReceived}</span> */}
                        </div>
                        <div className="flex items-center gap-2">
                          <Reply className="w-4 h-4 text-muted-foreground" />
                          {/* <span>{data.emailsReplied}</span> */}
                        </div>
                        <div className="flex items-center gap-2">
                          <Clock className="w-4 h-4 text-muted-foreground" />
                          {/* <span>{data.responseTime}m</span> */}
                        </div>
                      </CardContent>
                      <CardFooter>
                        <Button className="w-full" onClick={() => setSelectedSnail(data)}>View Details</Button>
                      </CardFooter>
                    </Card>
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </section>
      </main>

      {selectedSnail && (
        <AnalyticsDialog
          analytics={selectedSnail}
          open={!!selectedSnail}
          onOpenChange={(isOpen) => !isOpen && setSelectedSnail(null)}
        />
      )}
    </div>
  );
}
