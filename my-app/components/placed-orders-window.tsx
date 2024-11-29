import { useState } from 'react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogClose,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { ScrollArea } from "@/components/ui/scroll-area"

// ... (previous type definitions remain unchanged)

export function PlacedOrdersWindow({ isOpen, onClose, orders, setOrders, selectedDay, isAdmin }: PlacedOrdersWindowProps) {
  const [filter, setFilter] = useState<'all' | 'validated' | 'delivered'>('all')

  const filteredOrders = orders.filter(order => {
    if (order.day !== selectedDay) return false
    if (filter === 'validated') return order.isValidated
    if (filter === 'delivered') return order.isDelivered
    return true
  })

  const toggleOrderStatus = (orderId: string, status: 'isValidated' | 'isDelivered') => {
    if (!isAdmin) return
    // TODO: Implement API call to update order status
    setOrders(prevOrders =>
      prevOrders.map(order =>
        order.id === orderId
          ? { ...order, [status]: !order[status] }
          : order
      )
    )
  }

  const formatDate = (date: Date) => date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl w-full h-[calc(100vh-4rem)] max-h-[800px] flex flex-col bg-white bg-opacity-90 backdrop-blur-lg border border-gray-200">
        <DialogHeader className="flex-shrink-0">
          <DialogTitle className="text-2xl font-bold text-gray-800">Placed Orders for {selectedDay}</DialogTitle>
          <DialogDescription className="text-gray-600">View and manage your placed orders</DialogDescription>
        </DialogHeader>
        <div className="flex-shrink-0 mt-4">
          <div className="flex gap-4 mb-4">
            <Button
              variant={filter === 'all' ? 'default' : 'outline'}
              onClick={() => setFilter('all')}
              className={filter === 'all' ? "bg-gray-800 hover:bg-gray-900 text-white" : "text-gray-600 border-gray-300 hover:bg-gray-100"}
            >
              All Orders
            </Button>
            <Button
              variant={filter === 'validated' ? 'default' : 'outline'}
              onClick={() => setFilter('validated')}
              className={filter === 'validated' ? "bg-gray-800 hover:bg-gray-900 text-white" : "text-gray-600 border-gray-300 hover:bg-gray-100"}
            >
              Validated Orders
            </Button>
            <Button
              variant={filter === 'delivered' ? 'default' : 'outline'}
              onClick={() => setFilter('delivered')}
              className={filter === 'delivered' ? "bg-gray-800 hover:bg-gray-900 text-white" : "text-gray-600 border-gray-300 hover:bg-gray-100"}
            >
              Delivered Orders
            </Button>
          </div>
        </div>
        <ScrollArea className="flex-grow">
          <div className="space-y-4 p-4">
            {filteredOrders.map(order => (
              <div key={order.id} className="border border-gray-200 p-4 rounded-lg bg-white">
                <h3 className="font-semibold text-gray-800">
                  Order for {formatDate(order.date)}
                </h3>
                <p className="text-gray-600">Total: ${order.total.toFixed(2)}</p>
                <div className="mt-2 space-x-4">
                  <Label className="inline-flex items-center space-x-2">
                    <Checkbox
                      checked={order.isValidated}
                      onCheckedChange={() => toggleOrderStatus(order.id, 'isValidated')}
                      disabled={!isAdmin}
                    />
                    <span className="text-gray-700">Validated</span>
                  </Label>
                  <Label className="inline-flex items-center space-x-2">
                    <Checkbox
                      checked={order.isDelivered}
                      onCheckedChange={() => toggleOrderStatus(order.id, 'isDelivered')}
                      disabled={!isAdmin}
                    />
                    <span className="text-gray-700">Delivered</span>
                  </Label>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
        <DialogClose asChild>
          <Button className="mt-4 bg-gray-800 hover:bg-gray-900 text-white">Close</Button>
        </DialogClose>
      </DialogContent>
    </Dialog>
  )
}

