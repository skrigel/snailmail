"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ChartContainer, ChartTooltip, ChartTooltipContent, BarChart, Bar } from '@/components/ui/chart';
import { XAxis, YAxis, CartesianGrid } from 'recharts';
import type { DailyAnalytics } from '@/lib/types';
import { Mail, Reply, Clock } from 'lucide-react';
import type { ChartConfig } from '@/components/ui/chart';

type AnalyticsDialogProps = {
  analytics: DailyAnalytics;
  open: boolean;
  onOpenChange: (open: boolean) => void;
};

const chartConfig = {
  received: {
    label: 'Received',
    color: 'hsl(var(--accent))',
  },
  replied: {
    label: 'Replied',
    color: 'hsl(var(--primary))',
  },
} satisfies ChartConfig;

const AnalyticsDialog = ({ analytics, open, onOpenChange }: AnalyticsDialogProps) => {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-2xl bg-card">
        <DialogHeader>
          <DialogTitle className="font-headline text-2xl">Analytics for {analytics.date}</DialogTitle>
          <DialogDescription>{analytics.dayOfWeek}</DialogDescription>
        </DialogHeader>
        <div className="grid gap-6 py-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Emails Received</CardTitle>
                <Mail className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics.emailsReceived}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Emails Replied</CardTitle>
                <Reply className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics.emailsReplied}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Avg. Response Time</CardTitle>
                <Clock className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics.responseTime}<span className="text-sm text-muted-foreground">m</span></div>
              </CardContent>
            </Card>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-2 font-headline">Hourly Activity</h3>
            <ChartContainer config={chartConfig} className="h-64 w-full">
              <BarChart accessibilityLayer data={analytics.hourlyActivity}>
                <CartesianGrid vertical={false} />
                <XAxis
                  dataKey="hour"
                  tickLine={false}
                  tickMargin={10}
                  axisLine={false}
                  tickFormatter={(value: string) => value.slice(0, 2)}
                />
                <YAxis />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Bar dataKey="received" fill="var(--color-received)" radius={4} />
                <Bar dataKey="replied" fill="var(--color-replied)" radius={4} />
              </BarChart>
            </ChartContainer>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default AnalyticsDialog;
