import { useState } from 'react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogClose,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { ScrollArea } from "@/components/ui/scroll-area"

type BakeryItem = {
  id: number
  name: string
  price: number
  image: string
}

type WeeklySchedule = Record<string, number[]>

type EditItemsPopupProps = {
  isOpen: boolean
  onClose: () => void
  catalog: BakeryItem[]
  weeklySchedule: Record<number, WeeklySchedule>
  setWeeklySchedule: React.Dispatch<React.SetStateAction<Record<number, WeeklySchedule>>>
  selectedDay: string
  currentWeek: number
}

export function EditItemsPopup({
  isOpen,
  onClose,
  catalog,
  weeklySchedule,
  setWeeklySchedule,
  selectedDay,
  currentWeek
}: EditItemsPopupProps) {
  const [selectedItems, setSelectedItems] = useState<number[]>(
    weeklySchedule[currentWeek]?.[selectedDay] || []
  )

  const handleItemToggle = (itemId: number) => {
    setSelectedItems(prev =>
      prev.includes(itemId)
        ? prev.filter(id => id !== itemId)
        : [...prev, itemId]
    )
  }

  const handleSave = () => {
    setWeeklySchedule(prev => ({
      ...prev,
      [currentWeek]: {
        ...prev[currentWeek],
        [selectedDay]: selectedItems
      }
    }))
    onClose()
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl bg-white bg-opacity-90 backdrop-blur-lg border border-gray-200">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold text-gray-800">Edit Items for {selectedDay}</DialogTitle>
        </DialogHeader>
        <ScrollArea className="h-[60vh] overflow-y-auto pr-4">
          <div className="space-y-4">
            {catalog.map(item => (
              <div key={item.id} className="flex items-center space-x-2">
                <Checkbox
                  id={`item-${item.id}`}
                  checked={selectedItems.includes(item.id)}
                  onCheckedChange={() => handleItemToggle(item.id)}
                />
                <label
                  htmlFor={`item-${item.id}`}
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  {item.name} - ${item.price.toFixed(2)}
                </label>
              </div>
            ))}
          </div>
        </ScrollArea>
        <div className="flex justify-end space-x-2 mt-4">
          <Button onClick={onClose} variant="outline">Cancel</Button>
          
<Button onClick={handleSave}>Save Changes</Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}

