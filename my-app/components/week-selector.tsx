import { ChevronLeft, ChevronRight } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { motion, AnimatePresence } from "framer-motion"

type WeekSelectorProps = {
  currentWeek: number
  onWeekChange: (week: number) => void
  getWeekDates: (weekOffset: number) => { start: Date; end: Date }
}

export function WeekSelector({ currentWeek, onWeekChange, getWeekDates }: WeekSelectorProps) {
  const handlePreviousWeek = () => {
    onWeekChange(currentWeek - 1)
  }

  const handleNextWeek = () => {
    onWeekChange(currentWeek + 1)
  }

  const { start, end } = getWeekDates(currentWeek)
  const formatDate = (date: Date) => date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })

  return (
    <div className="flex items-center justify-center space-x-2 sm:space-x-4 bg-white p-2 rounded-lg shadow-md">
      <Button
        variant="outline"
        size="icon"
        onClick={handlePreviousWeek}
        aria-label="Previous week"
        className="h-8 w-8 sm:h-10 sm:w-10"
      >
        <ChevronLeft className="h-4 w-4 sm:h-5 sm:w-5" />
      </Button>
      <AnimatePresence mode="wait">
        <motion.h2
          key={currentWeek}
          initial={{ y: 10, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -10, opacity: 0 }}
          transition={{ duration: 0.2 }}
          className="text-sm sm:text-xl font-semibold text-gray-800 w-32 sm:w-48 text-center"
        >
          {formatDate(start)} - {formatDate(end)}
        </motion.h2>
      </AnimatePresence>
      <Button
        variant="outline"
        size="icon"
        onClick={handleNextWeek}
        aria-label="Next week"
        className="h-8 w-8 sm:h-10 sm:w-10"
      >
        <ChevronRight className="h-4 w-4 sm:h-5 sm:w-5" />
      </Button>
    </div>
  )
}

