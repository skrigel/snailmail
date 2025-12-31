"use client";

import { useState } from 'react';
import Image from 'next/image';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from '@/components/ui/carousel';
import type { DailyAnalytics } from '@/lib/types';
import Snail from '@/components/snail';
import AnalyticsDialog from '@/components/analytics-dialog';
import SnailMailIcon from '@/components/icons/snail-mail-icon';
import { CalendarDays, Mail, Reply, Clock, LogIn, LogOut } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

export default function Home() {
  const dailyData: DailyAnalytics[] = [
    {
      id: 1,
      dayOfWeek: 'Monday',
      date: '2024-10-20',
      inbox_count: 20,
      sent_count: 5,
      work: 10,
      personal: 8,
      promotions: 2,
      emailsReceived: 20,
      emailsReplied: 5,
      responseTime: 120,
      progress: 25,
      hourlyActivity: []
    },
    {
      id: 2,
      dayOfWeek: 'Tuesday',
      date: '2024-10-21',
      inbox_count: 15,
      sent_count: 7,
      work: 8,
      personal: 5,
      promotions: 2,
      emailsReceived: 15,
      emailsReplied: 7,
      responseTime: 90,
      progress: 40,
      hourlyActivity: []
    }
  ];

  const historicalData: DailyAnalytics[] = [
    {
      id: 3,
      dayOfWeek: 'Wednesday',
      date: '2024-10-22',
      inbox_count: 30,
      sent_count: 10,
      work: 15,
      personal: 12,
      promotions: 3,
      emailsReceived: 30,
      emailsReplied: 10,
      responseTime: 80,
      progress: 60,
      hourlyActivity: []
    },
    {
      id: 4,
      dayOfWeek: 'Thursday',
      date: '2024-10-23',
      inbox_count: 25,
      sent_count: 12,
      work: 12,
      personal: 10,
      promotions: 3,
      emailsReceived: 25,
      emailsReplied: 12,
      responseTime: 70,
      progress: 75,
      hourlyActivity: []
    },
    {
      id: 5,
      dayOfWeek: 'Friday',
      date: '2024-10-24',
      inbox_count: 40,
      sent_count: 20,
      work: 20,
      personal: 15,
      promotions: 5,
      emailsReceived: 40,
      emailsReplied: 20,
      responseTime: 60,
      progress: 90,
      hourlyActivity: []
    },
  ];
  const [selectedSnail, setSelectedSnail] = useState<DailyAnalytics | null>(null);
  const { isAuthenticated, user, loading, login, logout } = useAuth();

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
        <section>
          <Card className={"overflow-hidden"}>
            <CardHeader>
              <CardTitle className="font-headline text-3xl tracking-tighter">Today's Snail Race</CardTitle>
              <CardDescription>A visual comparison of your inbox activity over the last few days.</CardDescription>
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
