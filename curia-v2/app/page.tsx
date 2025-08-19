"use client"
import { CuriaLogo } from "@/components/curia-logo"
import { useState, useEffect } from "react"
import { KanbanCalendar } from "@/components/kanban-calendar"
import { ProductList } from "@/components/product-list"
import { OrdersList } from "@/components/orders-list"
import { MessagesList } from "@/components/messages-list"
import { Button } from "@/components/ui/button"
import { Moon, Sun, Calendar, Package, ShoppingCart, MessageCircle, ChevronDown, Upload } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
  DropdownMenuCheckboxItem,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"

// Sample product data
const sampleProducts = [
  {
    id: "1",
    name: "Email Campaign Launch",
    category: "Marketing",
    color: "bg-purple-100 text-purple-800 border-purple-200",
  },
  { id: "2", name: "Website Redesign", category: "Design", color: "bg-yellow-100 text-yellow-800 border-yellow-200" },
  { id: "3", name: "API Development", category: "Development", color: "bg-blue-100 text-blue-800 border-blue-200" },
  { id: "4", name: "Blog Post Writing", category: "Content", color: "bg-green-100 text-green-800 border-green-200" },
  {
    id: "5",
    name: "User Analytics Review",
    category: "Analytics",
    color: "bg-orange-100 text-orange-800 border-orange-200",
  },
  { id: "6", name: "Client Presentation", category: "Sales", color: "bg-red-100 text-red-800 border-red-200" },
  {
    id: "7",
    name: "Social Media Strategy",
    category: "Marketing",
    color: "bg-purple-100 text-purple-800 border-purple-200",
  },
  {
    id: "8",
    name: "Database Optimization",
    category: "Development",
    color: "bg-blue-100 text-blue-800 border-blue-200",
  },
]

const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

export default function Home() {
  const [products, setProducts] = useState(sampleProducts)
  const [scheduledProducts, setScheduledProducts] = useState<Record<string, typeof sampleProducts>>({
    Monday: [],
    Tuesday: [sampleProducts[0]],
    Wednesday: [],
    Thursday: [sampleProducts[1], sampleProducts[2]],
    Friday: [],
    Saturday: [sampleProducts[3]],
    Sunday: [],
  })

  const [isDarkMode, setIsDarkMode] = useState(false)
  const [startWeekOnMonday, setStartWeekOnMonday] = useState(true)
  const [currentView, setCurrentView] = useState<"calendar" | "library" | "orders" | "messages">("calendar")
  const [repeatedProducts, setRepeatedProducts] = useState<
    Record<string, { originalDay: string; repeatedDays: string[] }>
  >({})
  const [avatarUploadDialog, setAvatarUploadDialog] = useState(false)
  const [userAvatar, setUserAvatar] = useState<string | null>(null)
  const [businessSearchOpen, setBusinessSearchOpen] = useState(false)
  const [businessSearchQuery, setBusinessSearchQuery] = useState("")

  useEffect(() => {
    const savedDarkMode = localStorage.getItem("kanban-dark-mode")
    const savedWeekStart = localStorage.getItem("kanban-week-start")

    if (savedDarkMode !== null) {
      setIsDarkMode(JSON.parse(savedDarkMode))
    }
    if (savedWeekStart !== null) {
      setStartWeekOnMonday(JSON.parse(savedWeekStart))
    }
  }, [])

  useEffect(() => {
    localStorage.setItem("kanban-dark-mode", JSON.stringify(isDarkMode))
    document.documentElement.classList.toggle("dark", isDarkMode)
  }, [isDarkMode])

  useEffect(() => {
    localStorage.setItem("kanban-week-start", JSON.stringify(startWeekOnMonday))
  }, [startWeekOnMonday])

  const handleAddProduct = (day: string, product: (typeof sampleProducts)[0]) => {
    setScheduledProducts((prev) => ({
      ...prev,
      [day]: [...(prev[day] || []), product],
    }))
  }

  const handleRemoveProduct = (day: string, productId: string) => {
    setScheduledProducts((prev) => ({
      ...prev,
      [day]: (prev[day] || []).filter((p) => p.id !== productId),
    }))
  }

  const handleMoveProduct = (fromDay: string, toDay: string, product: (typeof sampleProducts)[0]) => {
    setScheduledProducts((prev) => ({
      ...prev,
      [fromDay]: (prev[fromDay] || []).filter((p) => p.id !== product.id),
      [toDay]: [...(prev[toDay] || []), product],
    }))
  }

  const handleCreateProduct = (productData: Omit<(typeof sampleProducts)[0], "id">) => {
    const newProduct = {
      ...productData,
      id: Date.now().toString(),
    }
    setProducts((prev) => [...prev, newProduct])
  }

  const handleDeleteProduct = (productId: string) => {
    setProducts((prev) => prev.filter((p) => p.id !== productId))
    setScheduledProducts((prev) => {
      const updated = { ...prev }
      Object.keys(updated).forEach((day) => {
        updated[day] = updated[day].filter((p) => p.id !== productId)
      })
      return updated
    })
    setRepeatedProducts((prev) => {
      const updated = { ...prev }
      delete updated[productId]
      return updated
    })
  }

  const handleRepeatProduct = (productId: string, currentDay: string) => {
    const product = products.find((p) => p.id === productId)
    if (!product) return

    const targetDays = daysOfWeek.filter((day) => day !== currentDay)

    setScheduledProducts((prev) => {
      const updated = { ...prev }
      targetDays.forEach((day) => {
        if (!updated[day].some((p) => p.id === productId)) {
          updated[day] = [...updated[day], product]
        }
      })
      return updated
    })

    setRepeatedProducts((prev) => ({
      ...prev,
      [productId]: {
        originalDay: currentDay,
        repeatedDays: targetDays,
      },
    }))
  }

  const handleUnrepeatProduct = (productId: string, currentDay: string) => {
    const repeatInfo = repeatedProducts[productId]
    if (!repeatInfo) return

    // Remove from repeated days only, keep original day
    setScheduledProducts((prev) => {
      const updated = { ...prev }
      repeatInfo.repeatedDays.forEach((day) => {
        if (day !== repeatInfo.originalDay) {
          updated[day] = updated[day].filter((p) => p.id !== productId)
        }
      })
      return updated
    })

    setRepeatedProducts((prev) => {
      const updated = { ...prev }
      delete updated[productId]
      return updated
    })
  }

  const handleOrderClick = () => {
    setCurrentView("orders")
  }

  const handleAvatarUpload = (file: File) => {
    const imageUrl = URL.createObjectURL(file)
    setUserAvatar(imageUrl)
    setAvatarUploadDialog(false)
  }

  const mockBusinesses = [
    { id: "1", name: "Artisan Bakery Co.", initials: "AB", current: true },
    { id: "2", name: "Corner Cafe", initials: "CF", current: false },
    { id: "3", name: "Fresh Treats", initials: "FT", current: false },
    { id: "4", name: "Sweet Delights", initials: "SD", current: false },
    { id: "5", name: "Urban Eats", initials: "UE", current: false },
  ]

  const filteredBusinesses = mockBusinesses.filter((business) =>
    business.name.toLowerCase().includes(businessSearchQuery.toLowerCase()),
  )

  return (
    <div className={`min-h-screen bg-background ${isDarkMode ? "dark" : ""}`}>
      <div className="border-b border-border bg-background">
        <div className="flex items-center justify-between p-6">
          <div className="flex items-center gap-4">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <div className="w-8 h-8 rounded-full bg-blue-200 flex items-center justify-center text-sm font-medium text-gray-700 cursor-pointer hover:scale-105 transition-transform overflow-hidden">
                  {userAvatar ? (
                    <img
                      src={userAvatar || "/placeholder.svg"}
                      alt="User Avatar"
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    "CU"
                  )}
                </div>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="start" className="w-56">
                <DropdownMenuItem onClick={() => setAvatarUploadDialog(true)}>
                  <Upload className="h-4 w-4 mr-2" />
                  Change Avatar
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => setIsDarkMode(!isDarkMode)}>
                  {isDarkMode ? <Sun className="h-4 w-4 mr-2" /> : <Moon className="h-4 w-4 mr-2" />}
                  {isDarkMode ? "Light Mode" : "Dark Mode"}
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuCheckboxItem checked={startWeekOnMonday} onCheckedChange={setStartWeekOnMonday}>
                  Start week on Monday
                </DropdownMenuCheckboxItem>
              </DropdownMenuContent>
            </DropdownMenu>

            <div className="flex flex-col">
            <CuriaLogo className="text-foreground" />
              <DropdownMenu open={businessSearchOpen} onOpenChange={setBusinessSearchOpen}>
                <DropdownMenuTrigger asChild>
                  <div className="flex items-center gap-2 cursor-pointer hover:bg-accent/50 rounded px-2 py-1 -mx-2 -my-1 transition-colors">
                    <p className="text-base font-medium text-foreground">Artisan Bakery Co.</p>
                    <ChevronDown className="h-3 w-3 text-muted-foreground" />
                  </div>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="start" className="w-64 p-0">
                  <div className="p-2 border-b">
                    <Input
                      placeholder="Search businesses..."
                      value={businessSearchQuery}
                      onChange={(e) => setBusinessSearchQuery(e.target.value)}
                      className="h-8"
                      autoFocus
                    />
                  </div>
                  <div className="max-h-48 overflow-y-auto">
                    {filteredBusinesses.length > 0 ? (
                      filteredBusinesses.map((business) => (
                        <DropdownMenuItem key={business.id} className="cursor-pointer p-3">
                          <div className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded bg-blue-100 flex items-center justify-center text-xs font-medium">
                              {business.initials}
                            </div>
                            <div>
                              <p className="font-medium">{business.name}</p>
                              <p className="text-xs text-muted-foreground">
                                {business.current ? "Current business" : "Switch to this business"}
                              </p>
                            </div>
                          </div>
                        </DropdownMenuItem>
                      ))
                    ) : (
                      <div className="p-3 text-sm text-muted-foreground text-center">No businesses found</div>
                    )}
                  </div>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
            <div className="flex items-center gap-3">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="sm"
                className="gap-2 text-muted-foreground hover:text-foreground text-lg"
              >
                {currentView === "calendar" ? (
                <Calendar className="h-5 w-5" />
                ) : currentView === "library" ? (
                <Package className="h-5 w-5" />
                ) : currentView === "orders" ? (
                <ShoppingCart className="h-5 w-5" />
                ) : (
                <MessageCircle className="h-5 w-5" />
                )}
                {currentView === "calendar"
                ? "Calendar"
                : currentView === "library"
                  ? "Products"
                  : currentView === "orders"
                  ? "Orders"
                  : "Messages"}
                <ChevronDown className="h-5 w-5" />
              </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuItem
                onClick={() => setCurrentView("calendar")}
                className={`${currentView === "calendar" ? "bg-accent" : ""} text-base`}
              >
                <Calendar className="h-4 w-4 mr-2" />
                Calendar
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => setCurrentView("library")}
                className={`${currentView === "library" ? "bg-accent" : ""} text-base`}
              >
                <Package className="h-4 w-4 mr-2" />
                Products
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => setCurrentView("orders")}
                className={`${currentView === "orders" ? "bg-accent" : ""} text-base`}
              >
                <ShoppingCart className="h-4 w-4 mr-2" />
                Orders
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => setCurrentView("messages")}
                className={`${currentView === "messages" ? "bg-accent" : ""} text-base`}
              >
                <MessageCircle className="h-4 w-4 mr-2" />
                Messages
              </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
            </div>
        </div>
      </div>

      <div className="flex-1">
        {currentView === "calendar" ? (
          <KanbanCalendar
            scheduledProducts={scheduledProducts}
            onAddProduct={handleAddProduct}
            onRemoveProduct={handleRemoveProduct}
            onMoveProduct={handleMoveProduct}
            availableProducts={products}
            onRepeatProduct={handleRepeatProduct}
            onUnrepeatProduct={handleUnrepeatProduct}
            repeatedProducts={repeatedProducts}
            onOrderClick={handleOrderClick}
          />
        ) : currentView === "library" ? (
          <div className="p-6 max-w-6xl mx-auto">
            <ProductList
              products={products}
              scheduledProducts={scheduledProducts}
              onAddProduct={handleAddProduct}
              onCreateProduct={handleCreateProduct}
              onDeleteProduct={handleDeleteProduct}
            />
          </div>
        ) : currentView === "orders" ? (
          <div className="p-6 max-w-6xl mx-auto">
            <OrdersList />
          </div>
        ) : (
          <div className="p-6 max-w-6xl mx-auto">
            <MessagesList />
          </div>
        )}
      </div>

      <Dialog open={avatarUploadDialog} onOpenChange={setAvatarUploadDialog}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Update Avatar</DialogTitle>
            <DialogDescription>Choose an image file to use as your profile avatar.</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="border-2 border-dashed border-border rounded-lg p-6 text-center">
              <Upload className="h-8 w-8 mx-auto text-muted-foreground mb-2" />
              <p className="text-sm text-muted-foreground mb-2">Drag and drop or click to select</p>
              <Input
                type="file"
                accept="image/*"
                onChange={(e) => {
                  const file = e.target.files?.[0]
                  if (file) {
                    handleAvatarUpload(file)
                  }
                }}
                className="cursor-pointer"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setAvatarUploadDialog(false)}>
              Cancel
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
