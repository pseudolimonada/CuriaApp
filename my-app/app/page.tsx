"use client"

import { useState, useEffect } from 'react'
import { BakeryItemCard } from '@/components/bakery-item-card'
import { OrderSummaryPopup } from '@/components/order-summary-popup'
import { PlacedOrdersWindow } from '@/components/placed-orders-window'
import { WeekSelector } from '@/components/week-selector'
import { Button } from '@/components/ui/button'
import { ShoppingCart, Calendar, Edit, Menu } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { EditItemsPopup } from '@/components/edit-items-popup'
import { CatalogManagementPopup } from '@/components/catalog-management-popup'
import { motion, AnimatePresence } from 'framer-motion'
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"

type BakeryItem = {
  id: number
  name: string
  price: number
  image: string
}

type Order = {
  id: string
  week: number
  day: string
  items: Record<number, number>
  total: number
  isValidated: boolean
  isDelivered: boolean
  date: Date
}

type WeeklySchedule = Record<string, number[]>

const initialBakeryItems: BakeryItem[] = [
  { id: 1, name: 'Croissant', price: 2.5, image: '/placeholder.svg?height=200&width=200' },
  { id: 2, name: 'Baguette', price: 3.0, image: '/placeholder.svg?height=200&width=200' },
  { id: 3, name: 'Chocolate Chip Cookie', price: 1.5, image: '/placeholder.svg?height=200&width=200' },
  { id: 4, name: 'Blueberry Muffin', price: 2.0, image: '/placeholder.svg?height=200&width=200' },
]

const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

const getWeekDates = (weekOffset: number) => {
  const now = new Date()
  const start = new Date(now.getFullYear(), now.getMonth(), now.getDate() - now.getDay() + (weekOffset * 7))
  const end = new Date(start.getFullYear(), start.getMonth(), start.getDate() + 6)
  return { start, end }
}

export default function BakeryOrderPage() {
  const router = useRouter()
  const [currentWeek, setCurrentWeek] = useState(0)
  const [selectedDay, setSelectedDay] = useState<string>(days[0])
  const [order, setOrder] = useState<Record<number, number>>({})
  const [isPopupOpen, setIsPopupOpen] = useState(false)
  const [placedOrders, setPlacedOrders] = useState<Order[]>([])
  const [isPlacedOrdersOpen, setIsPlacedOrdersOpen] = useState(false)
  const [isAdmin, setIsAdmin] = useState(false)
  const [catalog, setCatalog] = useState<BakeryItem[]>(initialBakeryItems)
  const [weeklySchedule, setWeeklySchedule] = useState<Record<number, WeeklySchedule>>({})
  const [isEditItemsOpen, setIsEditItemsOpen] = useState(false)
  const [isCatalogManagementOpen, setIsCatalogManagementOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
    } else {
      setIsAdmin(token === 'admin-token')
      // TODO: Implement API call to fetch placed orders, catalog, and weekly schedules
      // For now, we'll use mock data
      const mockOrders: Order[] = [
        {
          id: '1',
          week: 0,
          day: 'Monday',
          items: { 1: 2, 2: 1 },
          total: 8,
          isValidated: true,
          isDelivered: false,
          date: new Date(2024, 10, 4) // November 4, 2024 (a Monday)
        },
        {
          id: '2',
          week: 0,
          day: 'Wednesday',
          items: { 3: 3, 4: 2 },
          total: 8.5,
          isValidated: true,
          isDelivered: true,
          date: new Date(2024, 10, 6) // November 6, 2024 (a Wednesday)
        }
      ]
      setPlacedOrders(mockOrders)

      // Initialize weekly schedule with all items for all days
      const initialSchedule: Record<number, WeeklySchedule> = {
        0: Object.fromEntries(days.map(day => [day, catalog.map(item => item.id)]))
      }
      setWeeklySchedule(initialSchedule)
    }
  }, [router, catalog])

  const addToOrder = (itemId: number) => {
    setOrder(prev => ({
      ...prev,
      [itemId]: (prev[itemId] || 0) + 1
    }))
  }

  const removeFromOrder = (itemId: number) => {
    setOrder(prev => {
      const newOrder = { ...prev }
      if (newOrder[itemId] > 1) {
        newOrder[itemId]--
      } else {
        delete newOrder[itemId]
      }
      return newOrder
    })
  }

  const totalItems = Object.values(order).reduce((sum, count) => sum + count, 0)

  const placeOrder = () => {
    const availableItems = weeklySchedule[currentWeek]?.[selectedDay] || []
    const total = catalog
      .filter(item => availableItems.includes(item.id))
      .reduce((sum, item) => sum + item.price * (order[item.id] || 0), 0)
    const newOrder: Order = {
      id: Date.now().toString(),
      week: currentWeek,
      day: selectedDay,
      items: { ...order },
      total,
      isValidated: false,
      isDelivered: false,
      date: getWeekDates(currentWeek).start
    }
    // TODO: Implement API call to place order
    setPlacedOrders(prev => [...prev, newOrder])
    setOrder({})
    setIsPopupOpen(false)
    alert("Order placed successfully!")
  }

  const handleWeekChange = (week: number) => {
    setIsLoading(true)
    setCurrentWeek(week)
    setOrder({})
    // Initialize the schedule for the new week if it doesn't exist
    if (!weeklySchedule[week]) {
      setWeeklySchedule(prev => ({
        ...prev,
        [week]: Object.fromEntries(days.map(day => [day, catalog.map(item => item.id)]))
      }))
    }
    // Simulate loading delay
    setTimeout(() => setIsLoading(false), 500)
  }

  const { start, end } = getWeekDates(currentWeek)

  const availableItems = weeklySchedule[currentWeek]?.[selectedDay] || []
  const displayedItems = catalog.filter(item => availableItems.includes(item.id))

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto p-4">
        <div className="flex flex-col sm:flex-row items-center justify-between mb-8 gap-4">
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-800">Artisanal Bakery</h1>
          <WeekSelector currentWeek={currentWeek} onWeekChange={handleWeekChange} getWeekDates={getWeekDates} />
        </div>
        <div className="bg-white rounded-lg shadow-lg p-4 sm:p-6">
          <div className="flex flex-wrap gap-2 mb-6 justify-center">
            {days.map(day => (
              <Button
                key={day}
                variant={selectedDay === day ? "default" : "outline"}
                onClick={() => setSelectedDay(day)}
                className="font-medium text-xs sm:text-sm"
              >
                {day.length > 3 ? day.slice(0, 3) : day}
              </Button>
            ))}
          </div>
          {isAdmin && (
            <div className="flex flex-wrap gap-2 mb-4 justify-center sm:justify-start">
              <Button onClick={() => setIsEditItemsOpen(true)} className="bg-gray-800 hover:bg-gray-900 text-white text-xs sm:text-sm">
                <Edit className="mr-2 h-3 w-3 sm:h-4 sm:w-4" />
                Edit Day's Items
              </Button>
              <Button onClick={() => setIsCatalogManagementOpen(true)} className="bg-gray-800 hover:bg-gray-900 text-white text-xs sm:text-sm">
                Manage Catalog
              </Button>
            </div>
          )}
          <AnimatePresence mode="wait">
            {isLoading ? (
              <motion.div
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex justify-center items-center h-64"
              >
                <div className="animate-spin rounded-full h-16 w-16 sm:h-32 sm:w-32 border-b-2 border-gray-900"></div>
              </motion.div>
            ) : (
              <motion.div
                key="content"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                {displayedItems.length > 0 ? (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 max-w-4xl mx-auto">
                    {displayedItems.map(item => (
                      <BakeryItemCard
                        key={item.id}
                        item={item}
                        count={order[item.id] || 0}
                        onAdd={() => addToOrder(item.id)}
                        onRemove={() => removeFromOrder(item.id)}
                      />
                    ))}
                  </div>
                ) : (
                  <div className="text-center text-gray-500 py-12">
                    <p className="text-xl sm:text-2xl font-semibold">No bread today! Sorry</p>
                    <p className="mt-2">Check back tomorrow for fresh bakes!</p>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
      <Sheet>
        <SheetTrigger asChild>
          <Button className="fixed bottom-4 left-4 z-10 rounded-full p-3 bg-gray-800 hover:bg-gray-900 text-white sm:hidden">
            <Menu className="h-6 w-6" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-[250px] sm:w-[300px]">
          <div className="flex flex-col gap-4 py-4">
            <Button onClick={() => setIsPlacedOrdersOpen(true)} className="bg-blue-600 hover:bg-blue-700 text-white justify-start">
              <Calendar className="mr-2 h-4 w-4" />
              View Placed Orders
            </Button>
            <Button onClick={() => setIsPopupOpen(true)} className="bg-gray-800 hover:bg-gray-900 text-white justify-start">
              <ShoppingCart className="mr-2 h-4 w-4" />
              View Order ({totalItems})
            </Button>
          </div>
        </SheetContent>
      </Sheet>
      <div className="fixed bottom-4 right-4 z-10 flex-col gap-2 hidden sm:flex">
        <Button onClick={() => setIsPlacedOrdersOpen(true)} className="bg-blue-600 hover:bg-blue-700 text-white">
          <Calendar className="mr-2 h-4 w-4" />
          View Placed Orders
        </Button>
        <Button onClick={() => setIsPopupOpen(true)} className="bg-gray-800 hover:bg-gray-900 text-white">
          <ShoppingCart className="mr-2 h-4 w-4" />
          View Order ({totalItems})
        </Button>
      </div>
      <OrderSummaryPopup
        isOpen={isPopupOpen}
        onClose={() => setIsPopupOpen(false)}
        order={order}
        bakeryItems={displayedItems}
        onPlaceOrder={placeOrder}
        selectedDay={selectedDay}
        weekStart={start}
        weekEnd={end}
      />
      <PlacedOrdersWindow
        isOpen={isPlacedOrdersOpen}
        onClose={() => setIsPlacedOrdersOpen(false)}
        orders={placedOrders}
        setOrders={setPlacedOrders}
        selectedDay={selectedDay}
        isAdmin={isAdmin}
      />
      <EditItemsPopup
        isOpen={isEditItemsOpen}
        onClose={() => setIsEditItemsOpen(false)}
        catalog={catalog}
        weeklySchedule={weeklySchedule}
        setWeeklySchedule={setWeeklySchedule}
        selectedDay={selectedDay}
        currentWeek={currentWeek}
      />
      <CatalogManagementPopup
        isOpen={isCatalogManagementOpen}
        onClose={() => setIsCatalogManagementOpen(false)}
        catalog={catalog}
        setCatalog={setCatalog}
      />
    </div>
  )
}

