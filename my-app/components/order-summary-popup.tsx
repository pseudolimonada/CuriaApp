import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"

type BakeryItem = {
  id: number
  name: string
  price: number
  image: string
}

type OrderSummaryPopupProps = {
  isOpen: boolean
  onClose: () => void
  order: Record<number, number>
  bakeryItems: BakeryItem[]
  onPlaceOrder: () => void
  selectedDay: string
  weekStart: Date
  weekEnd: Date
}

export function OrderSummaryPopup({ isOpen, onClose, order, bakeryItems, onPlaceOrder, selectedDay, weekStart, weekEnd }: OrderSummaryPopupProps) {
  const orderItems = bakeryItems.filter(item => order[item.id] > 0)
  const total = orderItems.reduce((sum, item) => sum + item.price * order[item.id], 0)

  const formatDate = (date: Date) => date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-md bg-white bg-opacity-90 backdrop-blur-lg border border-gray-200">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold text-gray-800">Order Summary</DialogTitle>
          <DialogDescription className="text-gray-600">
            {formatDate(weekStart)} - {formatDate(weekEnd)}, {selectedDay}
          </DialogDescription>
        </DialogHeader>
        <ScrollArea className="h-[60vh] overflow-y-auto pr-4">
          <div className="space-y-4">
            {orderItems.map(item => (
              <div key={item.id} className="flex justify-between items-center mb-2 text-gray-800">
                <span className="font-medium">{item.name}</span>
                <span>
                  {order[item.id]} x ${item.price.toFixed(2)} = ${(order[item.id] * item.price).toFixed(2)}
                </span>
              </div>
            ))}
          </div>
        </ScrollArea>
        <div className="border-t border-gray-200 pt-2 mt-4">
          <div className="flex justify-between items-center font-semibold text-gray-800">
            <span className="text-xl">Total</span>
            <span>${total.toFixed(2)}</span>
          </div>
        </div>
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline" className="text-gray-600 border-gray-300 hover:bg-gray-100">Close</Button>
          </DialogClose>
          <Button onClick={onPlaceOrder} className="bg-gray-800 hover:bg-gray-900 text-white">Place Order</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

