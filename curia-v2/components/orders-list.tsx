"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Package, User, Calendar, Plus, MessageCircle, Check, X, ChevronDown, ArrowUpDown, Filter } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"

interface Order {
  id: string
  customerName: string
  productId: string
  productName: string
  quantity: number
  unitPrice: number // Added
  status: "pending" | "accepted" | "removed"
  date: string
  actualDate: string
  category: string
  color: string
  avatarColor: string
}

const mockOrdersData: Order[] = [
  {
    id: "1",
    customerName: "John Smith",
    productId: "1",
    productName: "Email Campaign Launch",
    quantity: 2,
    unitPrice: 120,
    status: "pending",
    date: "Monday",
    actualDate: "24/01",
    category: "Marketing",
    color: "bg-purple-100 text-purple-800 border-purple-200",
    avatarColor: "bg-rose-200",
  },
  {
    id: "2",
    customerName: "Sarah Johnson",
    productId: "1",
    productName: "Email Campaign Launch",
    quantity: 1,
    unitPrice: 120,
    status: "accepted",
    date: "Monday",
    actualDate: "24/01",
    category: "Marketing",
    color: "bg-purple-100 text-purple-800 border-purple-200",
    avatarColor: "bg-blue-200",
  },
  {
    id: "3",
    customerName: "Mike Wilson",
    productId: "2",
    productName: "Website Redesign",
    quantity: 3,
    unitPrice: 950,
    status: "pending",
    date: "Thursday",
    actualDate: "27/01",
    category: "Design",
    color: "bg-yellow-100 text-yellow-800 border-yellow-200",
    avatarColor: "bg-green-200",
  },
  {
    id: "4",
    customerName: "Emma Davis",
    productId: "2",
    productName: "Website Redesign",
    quantity: 1,
    unitPrice: 950,
    status: "accepted",
    date: "Thursday",
    actualDate: "27/01",
    category: "Design",
    color: "bg-yellow-100 text-yellow-800 border-yellow-200",
    avatarColor: "bg-purple-200",
  },
  {
    id: "5",
    customerName: "Alex Brown",
    productId: "3",
    productName: "API Development",
    quantity: 2,
    unitPrice: 600,
    status: "pending",
    date: "Thursday",
    actualDate: "27/01",
    category: "Development",
    color: "bg-blue-100 text-blue-800 border-blue-200",
    avatarColor: "bg-orange-200",
  },
  {
    id: "6",
    customerName: "Lisa Garcia",
    productId: "4",
    productName: "Blog Post Writing",
    quantity: 1,
    unitPrice: 80,
    status: "removed",
    date: "Saturday",
    actualDate: "29/01",
    category: "Content",
    color: "bg-green-100 text-green-800 border-green-200",
    avatarColor: "bg-pink-200",
  },
]

const mockProducts = [
  { id: "1", name: "Email Campaign Launch", price: 120 },
  { id: "2", name: "Website Redesign", price: 950 },
  { id: "3", name: "API Development", price: 600 },
  { id: "4", name: "Blog Post Writing", price: 80 },
]

export function OrdersList() {
  const [orders, setOrders] = useState<Order[]>(mockOrdersData)
  const [selectedProducts, setSelectedProducts] = useState<string[]>([])
  const [selectedStatuses, setSelectedStatuses] = useState<string[]>([])
  const [sortBy, setSortBy] = useState<"date" | "customer" | "product" | "quantity">("date")

  const [showCreateForm, setShowCreateForm] = useState(false)
  const [editingOrder, setEditingOrder] = useState<string | null>(null)
  const [editingValues, setEditingValues] = useState<{ quantity: number }>({ quantity: 1 })
  const [newOrder, setNewOrder] = useState({
    customerName: "Current User", // Default to current user
    productId: "",
    quantity: 1,
  })

  const uniqueProducts = Array.from(new Set(orders.map((order) => order.productName)))
  const uniqueStatuses = Array.from(new Set(orders.map((order) => order.status)))

  const filteredOrders = orders.filter((order) => {
    const matchesProduct = selectedProducts.length === 0 || selectedProducts.includes(order.productName)
    const matchesStatus = selectedStatuses.length === 0 || selectedStatuses.includes(order.status)

    return matchesProduct && matchesStatus
  })

  const handleCreateOrder = () => {
    const selectedProduct = mockProducts.find((p) => p.id === newOrder.productId)
    if (!selectedProduct) return

    const avatarColors = ["bg-rose-200", "bg-blue-200", "bg-green-200", "bg-purple-200", "bg-orange-200", "bg-pink-200"]
    const newOrderData: Order = {
      id: Date.now().toString(),
      customerName: newOrder.customerName,
      productId: newOrder.productId,
      productName: selectedProduct.name,
      quantity: newOrder.quantity,
      unitPrice: selectedProduct.price, // Added
      status: "pending",
      date: "Today",
      actualDate: new Date().toLocaleDateString().split("/").reverse().join("/"), // Format as DD/MM
      category: "Manual",
      color: "bg-gray-100 text-gray-800 border-gray-200",
      avatarColor: avatarColors[Math.floor(Math.random() * avatarColors.length)],
    }

    setOrders([newOrderData, ...orders])
    setNewOrder({ customerName: "Current User", productId: "", quantity: 1 })
    setShowCreateForm(false)
  }

  const handleAcceptOrder = (orderId: string) => {
    setOrders(orders.map((order) => (order.id === orderId ? { ...order, status: "accepted" as const } : order)))
  }

  const handleRemoveOrder = (orderId: string) => {
    setOrders(orders.map((order) => (order.id === orderId ? { ...order, status: "removed" as const } : order)))
  }

  const getUserInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2)
  }

  const formatCurrency = (v: number) =>
    new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 2 }).format(v)

  const totals = filteredOrders.reduce(
    (acc, o) => {
      const amount = o.unitPrice * o.quantity
      acc.all += amount
      if (o.status === "pending") acc.pending += amount
      if (o.status === "accepted") acc.accepted += amount
      return acc
    },
    { all: 0, pending: 0, accepted: 0 },
  )

  const safeNumber = (v: string, fallback = 0) => {
    const n = Number.parseFloat(v)
    return Number.isFinite(n) && n >= 0 ? n : fallback
  }

  return (
    <TooltipProvider>
      <div className="space-y-6 px-6">
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Package className="h-6 w-6 text-primary" />
              <h2 className="text-2xl font-bold font-serif">Orders</h2>
              <Badge variant="secondary" className="ml-2">
                {filteredOrders.length} orders
              </Badge>
            </div>
            <Button
              onClick={() => setShowCreateForm(!showCreateForm)}
              variant="outline"
              className="gap-2 border-primary/20 text-primary hover:bg-primary/10 px-4 bg-transparent"
            >
              <Plus className="h-4 w-4" />
              Add Order
            </Button>
          </div>

          <div className="flex items-center gap-3 py-2 border-b border-border/50">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm" className="gap-2 text-muted-foreground hover:text-foreground">
                  <ArrowUpDown className="h-4 w-4" />
                  Sort
                  <ChevronDown className="h-3 w-3" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="start">
                <DropdownMenuItem onClick={() => setSortBy("date")}>
                  <Calendar className="h-4 w-4 mr-2" />
                  Date
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSortBy("customer")}>
                  <User className="h-4 w-4 mr-2" />
                  Customer
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSortBy("product")}>
                  <Package className="h-4 w-4 mr-2" />
                  Product
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSortBy("quantity")}>Quantity</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm" className="gap-2 text-muted-foreground hover:text-foreground">
                  <Filter className="h-4 w-4" />
                  Filter
                  <ChevronDown className="h-3 w-3" />
                  {selectedProducts.length + selectedStatuses.length > 0 && (
                    <Badge variant="secondary" className="ml-1">
                      {selectedProducts.length + selectedStatuses.length}
                    </Badge>
                  )}
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="start" className="w-48">
                {[
                  { value: "marketing", label: "Marketing" },
                  { value: "development", label: "Development" },
                  { value: "design", label: "Design" },
                  { value: "content", label: "Content" },
                  { value: "analytics", label: "Analytics" },
                  { value: "sales", label: "Sales" },
                ].map((option) => (
                  <DropdownMenuItem key={option.value} className="cursor-pointer">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded border border-border" />
                      {option.label}
                    </div>
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>

        {showCreateForm && (
          <div className="animate-in slide-in-from-top-4 fade-in-0 duration-500">
            <Card className="border-2 border-primary/20 bg-primary/5">
              <CardContent className="p-4">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-serif text-lg font-semibold">Create Manual Order</h3>
                  <Button variant="ghost" size="sm" onClick={() => setShowCreateForm(false)}>
                    <X className="h-4 w-4" />
                  </Button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="customer">Customer Name</Label>
                    <Input
                      id="customer"
                      value={newOrder.customerName}
                      onChange={(e) => setNewOrder({ ...newOrder, customerName: e.target.value })}
                      placeholder="Enter customer name"
                      className="border-border/50 focus:border-primary focus:ring-1 focus:ring-primary/20"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="product">Product</Label>
                    <Select
                      value={newOrder.productId}
                      onValueChange={(value) => setNewOrder({ ...newOrder, productId: value })}
                    >
                      <SelectTrigger className="border-border/50 focus:border-primary focus:ring-1 focus:ring-primary/20">
                        <SelectValue placeholder="Select product" />
                      </SelectTrigger>
                      <SelectContent>
                        {mockProducts.map((product) => (
                          <SelectItem key={product.id} value={product.id}>
                            {product.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="quantity">Quantity</Label>
                    <Input
                      id="quantity"
                      type="number"
                      min="1"
                      value={newOrder.quantity}
                      onChange={(e) => setNewOrder({ ...newOrder, quantity: Math.max(1, Math.trunc(safeNumber(e.target.value, 1))) })}
                      className="border-border/50 focus:border-primary focus:ring-1 focus:ring-primary/20"
                    />
                  </div>
                </div>
                <div className="flex gap-2 mt-4">
                  <Button
                    onClick={handleCreateOrder}
                    disabled={!newOrder.productId || !newOrder.customerName}
                    variant="outline"
                    className="border-primary/20 text-primary hover:bg-primary/10 bg-transparent"
                  >
                    Create Order
                  </Button>
                  <Button variant="ghost" onClick={() => setShowCreateForm(false)}>
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filteredOrders.map((order) => {
            const isEditing = editingOrder === order.id
            return (
              <Card
                key={order.id}
                className={cn(
                  "hover:shadow-md transition-all duration-300 cursor-pointer p-0", // Added p-0 to remove default card padding
                  order.status === "removed" && "opacity-60",
                  isEditing && "ring-2 ring-primary shadow-lg",
                )}
                onClick={() => {
                  if (isEditing) {
                    setEditingOrder(null)
                  } else {
                    setEditingOrder(order.id)
                    setEditingValues({ quantity: order.quantity })
                  }
                }}
              >
                <div className="p-3">
                  {" "}
                  {/* Added padding container for content */}
                  <div className="text-xs text-muted-foreground font-medium mb-2">
                    {order.date} {order.actualDate}
                  </div>
                  <div className="flex items-center gap-2 mb-3">
                    <div className={cn("w-2 h-2 rounded-full flex-shrink-0", order.color.split(" ")[0])} />
                    <span className="font-medium text-sm truncate flex-1">{order.productName}</span>
                    {isEditing ? (
                      <Input
                        value={editingValues.quantity}
                        onChange={(e) => setEditingValues({ quantity: Math.max(1, Math.trunc(safeNumber(e.target.value, editingValues.quantity))) })}
                        className="w-12 h-6 text-xs text-center border-border/50 focus:border-primary focus:ring-1 focus:ring-primary/20"
                        onClick={(e) => e.stopPropagation()}
                        type="number"
                        min="1"
                      />
                    ) : (
                      <span className="text-xs text-muted-foreground/70 bg-muted/30 px-1.5 py-0.5 rounded text-[10px] font-medium">
                        x{order.quantity}
                      </span>
                    )}
                    {/* Added order amount */}
                    <span className="text-[10px] ml-2 text-muted-foreground font-medium">
                      {formatCurrency(order.unitPrice * order.quantity)}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <button
                                className={cn(
                                  "w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium text-gray-700 hover:scale-105 transition-transform cursor-pointer",
                                  order.avatarColor,
                                )}
                                onClick={(e) => e.stopPropagation()}
                              >
                                {getUserInitials(order.customerName)}
                              </button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="start">
                              <div className="px-2 py-1.5 text-sm font-medium border-b border-border">
                                {order.customerName}
                              </div>
                              <DropdownMenuItem className="gap-2">
                                <MessageCircle className="h-4 w-4" />
                                Send Message
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>{order.customerName}</p>
                        </TooltipContent>
                      </Tooltip>

                      {order.status === "pending" && (
                        <div className="flex gap-1">
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button
                                size="sm"
                                variant="ghost"
                                className="h-6 w-6 p-0 hover:bg-green-100 hover:text-green-700"
                                onClick={(e) => e.stopPropagation()}
                              >
                                <Check className="h-3 w-3" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="start">
                              <DropdownMenuItem onClick={() => handleAcceptOrder(order.id)}>
                                Accept Order
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>

                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button
                                size="sm"
                                variant="ghost"
                                className="h-6 w-6 p-0 hover:bg-red-100 hover:text-red-700"
                                onClick={(e) => e.stopPropagation()}
                              >
                                <X className="h-3 w-3" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="start">
                              <DropdownMenuItem onClick={() => handleRemoveOrder(order.id)}>
                                Remove Order
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </div>
                      )}

                      {order.status === "accepted" && (
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button
                              size="sm"
                              variant="ghost"
                              className="h-6 w-6 p-0 hover:bg-orange-100 hover:text-orange-700"
                              onClick={(e) => e.stopPropagation()}
                            >
                              <X className="h-3 w-3" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="start">
                            <DropdownMenuItem
                              onClick={() =>
                                setOrders(
                                  orders.map((o) => (o.id === order.id ? { ...o, status: "pending" as const } : o)),
                                )
                              }
                            >
                              Cancel Order
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      )}
                    </div>

                    <Badge
                      variant={
                        order.status === "accepted" ? "default" : order.status === "removed" ? "secondary" : "outline"
                      }
                      className="text-xs"
                    >
                      {order.status}
                    </Badge>
                  </div>
                </div>
              </Card>
            )
          })}
        </div>

        <div className="flex items-center justify-between pt-4">
          <div className="text-sm text-muted-foreground">
            Showing 1-{Math.min(12, filteredOrders.length)} of {filteredOrders.length} orders
          </div>
          <div className="flex items-center gap-4">
            <div className="text-xs text-muted-foreground hidden md:block">
              Pending: {formatCurrency(totals.pending)} | Accepted: {formatCurrency(totals.accepted)}
            </div>
            <Button variant="outline" size="sm" disabled>
              Previous
            </Button>
            <Button variant="outline" size="sm" className="bg-primary text-primary-foreground">
              1
            </Button>
            <Button variant="outline" size="sm" disabled>
              Next
            </Button>
          </div>
        </div>

        {filteredOrders.length === 0 && (
          <div className="text-center py-12 text-muted-foreground">
            <Package className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p className="text-lg font-medium">No orders found</p>
            <p className="text-sm mt-1">Try adjusting your filters</p>
          </div>
        )}
      </div>
    </TooltipProvider>
  )
}
