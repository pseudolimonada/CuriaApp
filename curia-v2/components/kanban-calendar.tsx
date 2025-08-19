"use client"

import type React from "react"

import { useState, useRef, useCallback } from "react"
import { Card, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Plus, X, Calendar, ChevronLeft, ChevronRight, Repeat, Edit3, Eye, Check, ShoppingCart } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { cn } from "@/lib/utils"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface Product {
  id: string
  name: string
  category: string
  color: string
  price: number // Added
}

interface Order {
  id: string
  customerName: string
  productId: string
  quantity: number
  unitPrice: number // Added
  status: "pending" | "accepted" | "removed"
  date: string
}

interface KanbanCalendarProps {
  scheduledProducts: Record<string, Product[]>
  onAddProduct: (day: string, product: Product) => void
  onRemoveProduct: (day: string, productId: string) => void
  onMoveProduct: (fromDay: string, toDay: string, product: Product) => void
  availableProducts: Product[]
  onRepeatProduct: (productId: string, currentDay: string) => void
  onUnrepeatProduct: (productId: string, currentDay: string) => void
  repeatedProducts: Record<string, { originalDay: string; repeatedDays: string[] }>
  onOrderClick?: (order: Order) => void
}

const mockOrders: Order[] = [
  { id: "1", customerName: "John Smith", productId: "1", quantity: 2, unitPrice: 120, status: "pending", date: "Monday" },
  { id: "2", customerName: "Sarah Johnson", productId: "1", quantity: 1, unitPrice: 120, status: "pending", date: "Monday" },
  { id: "3", customerName: "Mike Wilson", productId: "2", quantity: 3, unitPrice: 950, status: "pending", date: "Thursday" },
  { id: "4", customerName: "Emma Davis", productId: "2", quantity: 1, unitPrice: 950, status: "accepted", date: "Thursday" },
  { id: "5", customerName: "Alex Brown", productId: "3", quantity: 2, unitPrice: 600, status: "pending", date: "Thursday" },
  { id: "6", customerName: "Lisa Garcia", productId: "4", quantity: 1, unitPrice: 80, status: "pending", date: "Saturday" },
]

const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
const daysOfWeekSunStart = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

const getWeekRange = (weekOffset = 0) => {
  const today = new Date()
  const currentDay = today.getDay()
  const mondayOffset = currentDay === 0 ? -6 : 1 - currentDay

  const monday = new Date(today)
  monday.setDate(today.getDate() + mondayOffset + weekOffset * 7)

  const sunday = new Date(monday)
  sunday.setDate(monday.getDate() + 6)

  const formatDate = (date: Date) => {
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric" })
  }

  return `${formatDate(monday)} - ${formatDate(sunday)}`
}

const getDateForDay = (dayName: string, weekOffset = 0) => {
  const today = new Date()
  const currentDay = today.getDay()
  const mondayOffset = currentDay === 0 ? -6 : 1 - currentDay

  const monday = new Date(today)
  monday.setDate(today.getDate() + mondayOffset + weekOffset * 7)

  const dayIndex = daysOfWeek.indexOf(dayName)
  const targetDate = new Date(monday)
  targetDate.setDate(monday.getDate() + dayIndex)

  return targetDate.toLocaleDateString("en-US", { month: "numeric", day: "numeric" })
}

export function KanbanCalendar({
  scheduledProducts,
  onAddProduct,
  onRemoveProduct,
  onMoveProduct,
  availableProducts,
  onRepeatProduct,
  onUnrepeatProduct,
  repeatedProducts,
  onOrderClick,
}: KanbanCalendarProps) {
  const [draggedProducts, setDraggedProducts] = useState<{ products: { product: Product; fromDay: string }[] } | null>(
    null,
  )
  const [selectedProducts, setSelectedProducts] = useState<Set<string>>(new Set())
  const [isSelecting, setIsSelecting] = useState(false)
  const [isDragging, setIsDragging] = useState(false)
  const [selectionBox, setSelectionBox] = useState<{
    startX: number
    startY: number
    endX: number
    endY: number
  } | null>(null)
  const [weekOffset, setWeekOffset] = useState(0)
  const [isTransitioning, setIsTransitioning] = useState(false)
  const [visibleDayStart, setVisibleDayStart] = useState(0)
  const containerRef = useRef<HTMLDivElement>(null)
  const scrollContainerRef = useRef<HTMLDivElement>(null)
  const [removeRepeatDialog, setRemoveRepeatDialog] = useState<{
    product: Product
    day: string
  } | null>(null)

  const [isManagementMode, setIsManagementMode] = useState(true) // Default to management mode
  const [selectedDay, setSelectedDay] = useState<string | null>(null)
  const [dayOrders, setDayOrders] = useState<Order[]>(mockOrders)
  const [productQuantities, setProductQuantities] = useState<Record<string, { set: number; sold: number }>>({
    "1": { set: 50, sold: 23 },
    "2": { set: 30, sold: 12 },
    "3": { set: 25, sold: 8 },
    "4": { set: 40, sold: 15 },
  })

  const formatCurrency = (v: number) =>
    new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 2 }).format(
      Number.isFinite(v) ? v : 0,
    )

  const getCurrentWeekDays = () => {
    return daysOfWeek
  }

  const currentDays = getCurrentWeekDays()
  const visibleDays = currentDays.slice(visibleDayStart, visibleDayStart + 4)

  const handleDragStart = (product: Product, fromDay: string, e: React.DragEvent) => {
    if (selectedProducts.has(product.id)) {
      // Collect all selected products from all days
      const allSelectedProducts: { product: Product; fromDay: string }[] = []

      Object.entries(scheduledProducts).forEach(([day, products]) => {
        products.forEach((p) => {
          if (selectedProducts.has(p.id)) {
            allSelectedProducts.push({ product: p, fromDay: day })
          }
        })
      })

      setDraggedProducts({ products: allSelectedProducts })
    } else {
      setDraggedProducts({ products: [{ product, fromDay }] })
    }
    setIsDragging(true)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleDrop = (e: React.DragEvent, toDay: string) => {
    e.preventDefault()
    if (draggedProducts) {
      draggedProducts.products.forEach(({ product, fromDay }) => {
        if (fromDay !== toDay) {
          onMoveProduct(fromDay, toDay, product)
        }
      })
    }
    setDraggedProducts(null)
    setIsDragging(false)
    setSelectedProducts(new Set()) // Clear selection after drag
  }

  const handleMouseDown = useCallback(
    (e: React.MouseEvent) => {
      if (isDragging || (e.target as HTMLElement).closest("button, [role='menuitem'], [data-product-id]")) {
        return
      }

      if (e.target === e.currentTarget || (e.target as HTMLElement).closest(".day-column")) {
        const rect = containerRef.current?.getBoundingClientRect()
        if (rect) {
          setIsSelecting(true)
          setSelectionBox({
            startX: e.clientX - rect.left,
            startY: e.clientY - rect.top,
            endX: e.clientX - rect.left,
            endY: e.clientY - rect.top,
          })
        }
      }
    },
    [isDragging],
  )

  const handleMouseMove = useCallback(
    (e: React.MouseEvent) => {
      if (isSelecting && selectionBox && containerRef.current && !isDragging) {
        const rect = containerRef.current.getBoundingClientRect()
        setSelectionBox((prev) =>
          prev
            ? {
                ...prev,
                endX: e.clientX - rect.left,
                endY: e.clientY - rect.top,
              }
            : null,
        )
      }
    },
    [isSelecting, selectionBox, isDragging],
  )

  const handleMouseUp = useCallback(() => {
    if (isSelecting && selectionBox && !isDragging) {
      // Calculate which products are within the selection box
      const newSelected = new Set<string>()

      // Get all product elements and check if they intersect with selection box
      const productElements = containerRef.current?.querySelectorAll("[data-product-id]")
      productElements?.forEach((element) => {
        const rect = element.getBoundingClientRect()
        const containerRect = containerRef.current?.getBoundingClientRect()
        if (containerRect) {
          const elementX = rect.left - containerRect.left
          const elementY = rect.top - containerRect.top
          const elementRight = elementX + rect.width
          const elementBottom = elementY + rect.height

          const selectionLeft = Math.min(selectionBox.startX, selectionBox.endX)
          const selectionTop = Math.min(selectionBox.startY, selectionBox.endY)
          const selectionRight = Math.max(selectionBox.startX, selectionBox.endX)
          const selectionBottom = Math.max(selectionBox.startY, selectionBox.endY)

          if (
            elementX < selectionRight &&
            elementRight > selectionLeft &&
            elementY < selectionBottom &&
            elementBottom > selectionTop
          ) {
            const productId = element.getAttribute("data-product-id")
            if (productId) newSelected.add(productId)
          }
        }
      })

      setSelectedProducts(newSelected)
    }
    setIsSelecting(false)
    setSelectionBox(null)
  }, [isSelecting, selectionBox, isDragging])

  const handleWeekChange = (direction: "prev" | "next") => {
    if (isTransitioning) return

    setIsTransitioning(true)
    setWeekOffset(direction === "next" ? weekOffset + 1 : weekOffset - 1)
    setTimeout(() => setIsTransitioning(false), 300)
  }

  const getAvailableProductsForDay = (day: string) => {
    const scheduledIds = scheduledProducts[day]?.map((p) => p.id) || []
    return availableProducts.filter((p) => !scheduledIds.includes(p.id))
  }

  const handleRepeatProduct = (product: Product, day: string, type: "weekly" | "daily") => {
    if (type === "weekly") {
      onRepeatProduct(product.id, day)
    } else if (type === "daily") {
      const allDays = daysOfWeek.filter((d) => d !== day)
      allDays.forEach((targetDay) => {
        onAddProduct(targetDay, product)
      })
      onRepeatProduct(product.id, day)
    }
  }

  const handleUnrepeatProduct = (product: Product, day: string) => {
    setRemoveRepeatDialog({ product, day })
  }

  const handleRemoveRepeatConfirm = (option: "all" | "following" | "current") => {
    if (!removeRepeatDialog) return

    const { product, day } = removeRepeatDialog
    const repeatInfo = repeatedProducts[product.id]

    if (repeatInfo && repeatInfo.originalDay === day) {
      if (option === "all") {
        onUnrepeatProduct(product.id, day)
      } else if (option === "current") {
        onRemoveProduct(day, product.id)
      } else if (option === "following") {
        const currentDayIndex = daysOfWeek.indexOf(day)
        const futureDays = daysOfWeek.slice(currentDayIndex + 1)
        futureDays.forEach((futureDay) => {
          if (scheduledProducts[futureDay]?.some((p) => p.id === product.id)) {
            onRemoveProduct(futureDay, product.id)
          }
        })
      }
    }

    setRemoveRepeatDialog(null)
  }

  const isRepeated = (productId: string, day: string) => {
    const repeatInfo = repeatedProducts[productId]
    return repeatInfo && repeatInfo.originalDay === day
  }

  const getPendingOrdersForDay = (day: string) => {
    return dayOrders.filter((order) => order.date === day && order.status === "pending").length
  }

  const getOrdersForDay = (day: string) => {
    return dayOrders.filter((order) => order.date === day)
  }

  const handleOrderAction = (orderId: string, action: "accept" | "remove") => {
    setDayOrders((prev) =>
      prev.map((order) =>
        order.id === orderId ? { ...order, status: action === "accept" ? "accepted" : "removed" } : order,
      ),
    )
  }

  const handleQuantityChange = (productId: string, field: "set" | "sold", value: number) => {
    setProductQuantities((prev) => ({
      ...prev,
      [productId]: {
        ...prev[productId],
        [field]: value,
      },
    }))
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div
        ref={scrollContainerRef}
        className="overflow-x-auto overflow-y-hidden"
        style={{ scrollbarWidth: "none", msOverflowStyle: "none" }}
      >
        <div
          ref={containerRef}
          className="relative flex gap-6 p-6 min-w-max transition-transform duration-300 ease-in-out"
          onMouseDown={!isManagementMode ? handleMouseDown : undefined}
          onMouseMove={!isManagementMode ? handleMouseMove : undefined}
          onMouseUp={!isManagementMode ? handleMouseUp : undefined}
          style={{ userSelect: "none", transform: isTransitioning ? "translateX(-20px)" : "translateX(0)" }}
        >
          {!isManagementMode && isSelecting && selectionBox && !isDragging && (
            <div
              className="absolute bg-primary/20 border-2 border-primary pointer-events-none z-50"
              style={{
                left: Math.min(selectionBox.startX, selectionBox.endX),
                top: Math.min(selectionBox.startY, selectionBox.endY),
                width: Math.abs(selectionBox.endX - selectionBox.startX),
                height: Math.abs(selectionBox.endY - selectionBox.startY),
              }}
            />
          )}

          {currentDays.map((day) => (
            <Card
              key={day}
              className="day-column flex flex-col w-80 h-[calc(100vh-200px)] border-2 border-border hover:border-primary/50 transition-colors duration-200 overflow-hidden bg-card flex-shrink-0 p-0"
              onDragOver={!isManagementMode ? handleDragOver : undefined}
              onDrop={!isManagementMode ? (e) => handleDrop(e, day) : undefined}
            >
              <div className="px-6 pt-6 pb-4 border-b border-border/50">
                <CardTitle className="flex items-center justify-between text-lg font-serif">
                  <div className="flex items-center gap-3 min-w-0 flex-1">
                    <Calendar className="h-5 w-5 text-primary flex-shrink-0" />
                    <div className="flex flex-col min-w-0">
                      <span className="truncate font-semibold">{day}</span>
                      <span className="text-xs text-muted-foreground">{getDateForDay(day, weekOffset)}</span>
                    </div>
                  </div>

                  {isManagementMode ? (
                    <div className="flex items-center gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-8 w-8 p-0 relative hover:bg-primary/10 hover:text-primary"
                        onClick={() => setSelectedDay(day)}
                      >
                        <ShoppingCart className="h-4 w-4" />
                        {getPendingOrdersForDay(day) > 0 && (
                          <div className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                            {getPendingOrdersForDay(day)}
                          </div>
                        )}
                      </Button>
                    </div>
                  ) : (
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-accent flex-shrink-0 ml-2">
                          <Plus className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end" className="w-64">
                        {getAvailableProductsForDay(day).length > 0 ? (
                          getAvailableProductsForDay(day).map((product) => (
                            <DropdownMenuItem
                              key={product.id}
                              onClick={() => onAddProduct(day, product)}
                              className="cursor-pointer"
                            >
                              <div className="flex items-center gap-3">
                                <div
                                  className={cn("w-3 h-3 rounded-full flex-shrink-0", product.color.split(" ")[0])}
                                />
                                <span className="font-medium truncate">{product.name}</span>
                              </div>
                            </DropdownMenuItem>
                          ))
                        ) : (
                          <DropdownMenuItem disabled>All products scheduled</DropdownMenuItem>
                        )}
                      </DropdownMenuContent>
                    </DropdownMenu>
                  )}
                </CardTitle>
                <div className="text-sm text-muted-foreground">
                  {isManagementMode
                    ? `${getOrdersForDay(day).length} orders`
                    : `${(scheduledProducts[day] || []).length} product${(scheduledProducts[day] || []).length !== 1 ? "s" : ""}`}
                </div>
              </div>

              <div className="flex-1 p-6 overflow-y-auto space-y-1 py-2">
                {(scheduledProducts[day] || []).map((product) => (
                  <div
                    key={product.id}
                    data-product-id={product.id}
                    draggable={!isManagementMode}
                    onDragStart={!isManagementMode ? (e) => handleDragStart(product, day, e) : undefined}
                    onDragEnd={
                      !isManagementMode
                        ? () => {
                            setIsDragging(false)
                            setDraggedProducts(null)
                          }
                        : undefined
                    }
                    className={cn(
                      "group relative p-3 rounded-xl border border-border bg-card transition-all duration-200",
                      !isManagementMode &&
                        "hover:bg-yellow-50/80 dark:hover:bg-yellow-900/20 cursor-move hover:shadow-lg hover:scale-[1.02]",
                      !isManagementMode &&
                        selectedProducts.has(product.id) &&
                        "ring-2 ring-primary bg-primary/10 shadow-lg",
                    )}
                    onClick={
                      !isManagementMode
                        ? (e) => {
                            e.stopPropagation()
                            const newSelected = new Set(selectedProducts)
                            if (e.ctrlKey || e.metaKey) {
                              if (newSelected.has(product.id)) {
                                newSelected.delete(product.id)
                              } else {
                                newSelected.add(product.id)
                              }
                            } else {
                              newSelected.clear()
                              newSelected.add(product.id)
                            }
                            setSelectedProducts(newSelected)
                          }
                        : undefined
                    }
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex-1 min-w-0">
                        <h4 className="font-semibold text-card-foreground text-sm mb-2 leading-tight">
                          {product.name}
                        </h4>
                        <Badge variant="secondary" className={cn("text-xs", product.color)}>
                          {product.category}
                        </Badge>
                        <div className="text-[11px] font-medium mt-1 text-muted-foreground">
                          {formatCurrency(product.price)}
                        </div>
                      </div>

                      {!isManagementMode && (
                        <div className="flex gap-1 flex-shrink-0">
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button
                                variant="ghost"
                                size="sm"
                                className={cn(
                                  "opacity-0 group-hover:opacity-100 transition-opacity h-7 w-7 p-0",
                                  isRepeated(product.id, day) && "opacity-100 bg-primary/20 text-primary",
                                )}
                                onClick={(e) => e.stopPropagation()}
                              >
                                <Repeat className="h-3 w-3" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              {isRepeated(product.id, day) ? (
                                <DropdownMenuItem
                                  onClick={(e) => {
                                    e.stopPropagation()
                                    handleUnrepeatProduct(product, day)
                                  }}
                                >
                                  Remove repeat
                                </DropdownMenuItem>
                              ) : (
                                <>
                                  <DropdownMenuItem
                                    onClick={(e) => {
                                      e.stopPropagation()
                                      handleRepeatProduct(product, day, "weekly")
                                    }}
                                  >
                                    Repeat weekly
                                  </DropdownMenuItem>
                                  <DropdownMenuItem
                                    onClick={(e) => {
                                      e.stopPropagation()
                                      handleRepeatProduct(product, day, "daily")
                                    }}
                                  >
                                    Repeat daily this week
                                  </DropdownMenuItem>
                                </>
                              )}
                            </DropdownMenuContent>
                          </DropdownMenu>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation()
                              onRemoveProduct(day, product.id)
                            }}
                            className="opacity-0 group-hover:opacity-100 transition-opacity h-7 w-7 p-0 hover:bg-destructive hover:text-destructive-foreground"
                          >
                            <X className="h-3 w-3" />
                          </Button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                {(scheduledProducts[day] || []).length === 0 && (
                  <div className="text-center py-12 text-muted-foreground">
                    <Calendar className="h-8 w-8 mx-auto mb-3 opacity-50" />
                    <p className="text-sm font-medium">
                      {isManagementMode ? "No products scheduled" : "No products scheduled"}
                    </p>
                    <p className="text-xs mt-1">
                      {isManagementMode ? "Switch to editing mode to add products" : "Click + to add products"}
                    </p>
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      </div>

      <Dialog open={!!selectedDay} onOpenChange={() => setSelectedDay(null)}>
        <DialogContent
          className="w-[95vw] sm:max-w-2xl max-h-[90vh] p-0 flex flex-col"
        >
          <div className="p-6 pb-4 border-b">
            <DialogHeader>
              <DialogTitle className="text-base sm:text-lg">Orders for {selectedDay}</DialogTitle>
              <DialogDescription className="text-xs sm:text-sm">
                Manage product quantities and process orders for this day
              </DialogDescription>
            </DialogHeader>
          </div>

          <div className="flex-1 overflow-y-auto px-6 py-4 space-y-8">
            {/* Product quantities section */}
            <div className="space-y-4">
              <h3 className="font-semibold text-sm sm:text-base">Product Quantities</h3>
              {selectedDay &&
                (scheduledProducts[selectedDay] || []).map((product) => (
                  <div
                    key={product.id}
                    className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 border rounded-lg bg-card/50"
                  >
                    <div className="flex items-start sm:items-center gap-3 min-w-0">
                      <div className={cn("w-3 h-3 rounded-full mt-1 sm:mt-0 flex-shrink-0", product.color.split(" ")[0])} />
                      <div className="min-w-0">
                        <span className="font-medium block text-sm sm:text-base truncate">
                          {product.name}
                        </span>
                        <span className="text-xs text-muted-foreground">
                          {formatCurrency(product.price)}
                        </span>
                      </div>
                    </div>
                    <div className="flex flex-wrap items-center gap-x-6 gap-y-3">
                      <div className="flex items-center gap-2">
                        <span className="text-xs sm:text-sm text-muted-foreground">Set:</span>
                        <Input
                          type="number"
                          value={productQuantities[product.id]?.set || 0}
                          onChange={(e) =>
                            handleQuantityChange(
                              product.id,
                              "set",
                              Number.isFinite(Number.parseInt(e.target.value))
                                ? Number.parseInt(e.target.value)
                                : 0,
                            )
                          }
                          className="w-20 h-8 text-sm"
                        />
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs sm:text-sm text-muted-foreground">Sold:</span>
                        <span className="font-medium text-sm">
                          {productQuantities[product.id]?.sold || 0}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs sm:text-sm text-muted-foreground">Revenue:</span>
                        <span className="font-semibold text-sm">
                          {formatCurrency((productQuantities[product.id]?.sold || 0) * product.price)}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
            </div>

            {/* Orders section */}
            <div className="space-y-4">
              <h3 className="font-semibold text-sm sm:text-base">
                Orders ({getOrdersForDay(selectedDay || "").length})
              </h3>
              <div className="space-y-2">
                {getOrdersForDay(selectedDay || "").map((order) => {
                  const product = availableProducts.find((p) => p.id === order.productId)
                  return (
                    <div
                      key={order.id}
                      className={cn(
                        "flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 border rounded-lg cursor-pointer hover:bg-accent/50 transition-colors",
                        order.status === "removed" && "opacity-50 bg-muted",
                      )}
                      onClick={() => onOrderClick?.(order)}
                    >
                      <div className="flex items-start sm:items-center gap-3 min-w-0">
                        <div className={cn("w-3 h-3 rounded-full mt-1 sm:mt-0 flex-shrink-0", product?.color.split(" ")[0])} />
                        <div className="min-w-0">
                          <span className="font-medium block text-sm truncate">{order.customerName}</span>
                          <div className="text-xs sm:text-sm text-muted-foreground truncate">
                            {product?.name} × {order.quantity} @ {formatCurrency(order.unitPrice)}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-3 flex-wrap">
                        <Badge
                          variant={
                            order.status === "accepted"
                              ? "default"
                              : order.status === "removed"
                                ? "secondary"
                                : "outline"
                          }
                          className="text-xs"
                        >
                          {order.status}
                        </Badge>
                        {order.status === "pending" && (
                          <div className="flex gap-1">
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={(e) => {
                                e.stopPropagation()
                                handleOrderAction(order.id, "accept")
                              }}
                              className="h-7 w-7 p-0"
                            >
                              <Check className="h-3 w-3" />
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={(e) => {
                                e.stopPropagation()
                                handleOrderAction(order.id, "remove")
                              }}
                              className="h-7 w-7 p-0"
                            >
                              <X className="h-3 w-3" />
                            </Button>
                          </div>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Week selection control at bottom */}
      <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2 flex items-center gap-2 bg-card border border-border rounded-lg p-2 shadow-lg">
        <Button
          variant="outline"
          size="sm"
          onClick={() => handleWeekChange("prev")}
          disabled={isTransitioning}
          className="h-8 w-8 p-0"
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>
        <span className="text-sm font-medium px-3 text-muted-foreground">{getWeekRange(weekOffset)}</span>
        <Button
          variant="outline"
          size="sm"
          onClick={() => handleWeekChange("next")}
          disabled={isTransitioning}
          className="h-8 w-8 p-0"
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>

      {/* Mode toggle button at bottom right */}
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              onClick={() => setIsManagementMode(!isManagementMode)}
              variant="default"
              size="icon"
              className="fixed bottom-6 right-6 h-12 w-12 rounded-full shadow-lg"
            >
              {isManagementMode ? <Edit3 className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
            </Button>
          </TooltipTrigger>
          <TooltipContent side="left">
            <p>Switch to {isManagementMode ? "Editing" : "Management"} Mode</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </div>
  )
}
