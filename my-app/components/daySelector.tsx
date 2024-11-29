import { Button } from '@/components/ui/button';

type DaySelectorProps = {
  days: string[];
  selectedDay: string;
  onDayChange: (day: string) => void;
};

export function DaySelector({ days, selectedDay, onDayChange }: DaySelectorProps) {
  return (
    <div className="relative mb-6">
      <div className="flex gap-2 overflow-x-auto scrollbar-hide">
        {days.map(day => (
          <Button
            key={day}
            variant={selectedDay === day ? "default" : "outline"}
            onClick={() => onDayChange(day)}
            className="font-medium text-sm flex-shrink-0"
          >
            {day.length > 3 ? day.slice(0, 3) : day}
          </Button>
        ))}
      </div>
      <div className="absolute top-0 left-0 h-full w-8 bg-gradient-to-r from-gray-100 to-transparent pointer-events-none"></div>
      <div className="absolute top-0 right-0 h-full w-8 bg-gradient-to-l from-gray-100 to-transparent pointer-events-none"></div>
    </div>
  );
}