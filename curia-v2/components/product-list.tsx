"use client"

import type React from "react"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Plus, Package, X, Filter, ArrowUpDown, ChevronDown, Upload, Camera, Calendar } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { cn } from "@/lib/utils"

interface Product {
  id: string
  name: string
  category: string
  color: string
  image?: string
  price: number // Added
}

interface ProductListProps {
  products: Product[]
  scheduledProducts: Record<string, Product[]>
  onAddProduct: (day: string, product: Product) => void
  onCreateProduct: (product: Omit<Product, "id">) => void
  onDeleteProduct: (productId: string) => void
}

const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

const categoryColors = {
  Marketing: "bg-purple-100 text-purple-800 border-purple-200",
  Development: "bg-blue-100 text-blue-800 border-blue-200",
  Design: "bg-yellow-100 text-yellow-800 border-yellow-200",
  Content: "bg-green-100 text-green-800 border-green-200",
  Analytics: "bg-orange-100 text-orange-800 border-orange-200",
  Sales: "bg-red-100 text-red-800 border-red-200",
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

  return targetDate.toLocaleDateString("en-US", { weekday: "short", month: "numeric", day: "numeric" })
}

const getCurrentDayIndex = () => {
  const today = new Date().getDay()
  return today === 0 ? 6 : today - 1 // Convert Sunday (0) to 6, Monday (1) to 0, etc.
}

const getOrderedDaysFromToday = () => {
  const currentIndex = getCurrentDayIndex()
  return [...daysOfWeek.slice(currentIndex), ...daysOfWeek.slice(0, currentIndex)]
}

export function ProductList({
  products,
  scheduledProducts,
  onAddProduct,
  onCreateProduct,
  onDeleteProduct,
}: ProductListProps) {
  const [showForm, setShowForm] = useState(false)
  const [editingProduct, setEditingProduct] = useState<string | null>(null)
  const [deleteDialog, setDeleteDialog] = useState<string | null>(null)
  const [editingValues, setEditingValues] = useState<{ name: string; category: string; image?: string; price: number }>({
    name: "",
    category: "",
    price: 0,
  })
  const [newProduct, setNewProduct] = useState({
    name: "",
    category: "",
    color: "",
    image: "",
    price: 0, // Added
  })
  const [imageUploadDialog, setImageUploadDialog] = useState<string | null>(null)

  const getScheduledDays = (productId: string) => {
    return daysOfWeek.filter((day) => scheduledProducts[day]?.some((p) => p.id === productId))
  }

  const getAvailableDays = (productId: string) => {
    return daysOfWeek.filter((day) => !scheduledProducts[day]?.some((p) => p.id === productId))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (newProduct.name && newProduct.category && newProduct.color && Number.isFinite(newProduct.price) && newProduct.price > 0) {
      onCreateProduct(newProduct)
      setNewProduct({ name: "", category: "", color: "", image: "", price: 0 })
      setShowForm(false)
    }
  }

  const handleImageUpload = (file: File, productId?: string) => {
    const imageUrl = URL.createObjectURL(file)
    if (productId) {
      setEditingValues((prev) => ({ ...prev, image: imageUrl }))
    } else {
      setNewProduct((prev) => ({ ...prev, image: imageUrl }))
    }
    setImageUploadDialog(null)
  }

  const formatCurrency = (v: number) =>
    new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 2 }).format(
      Number.isFinite(v) ? v : 0,
    )

  const safeNumber = (v: string, fallback = 0) => {
    const n = Number.parseFloat(v)
    return Number.isFinite(n) && n >= 0 ? n : fallback
  }

  return (
    <div className="space-y-6 px-6">
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Package className="h-6 w-6 text-primary" />
            <h2 className="text-2xl font-bold font-serif">Products</h2>
            <Badge variant="secondary" className="ml-2">
              {products.length} products
            </Badge>
          </div>

          <Button
            onClick={() => setShowForm(!showForm)}
            variant="outline"
            className="gap-2 border-primary/20 text-primary hover:bg-primary/10 px-4 bg-transparent"
          >
            <Plus className="h-4 w-4" />
            Add Product
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
              {[
                { value: "name", label: "Name A-Z" },
                { value: "name-desc", label: "Name Z-A" },
                { value: "category", label: "Category" },
                { value: "created", label: "Date Created" },
              ].map((option) => (
                <DropdownMenuItem key={option.value} className="cursor-pointer">
                  {option.label}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm" className="gap-2 text-muted-foreground hover:text-foreground">
                <Filter className="h-4 w-4" />
                Filter
                <ChevronDown className="h-3 w-3" />
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
      {showForm && (
        <div className="animate-in slide-in-from-top-4 fade-in-0 duration-500">
          <Card className="border-2 border-primary/20 bg-primary/5 p-0">
            {" "}
            {/* Added p-0 to remove default card padding */}
            <div className="p-4">
              {" "}
              {/* Added padding container for form content */}
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-serif text-lg font-semibold">Create New Product</h3>
                <Button variant="ghost" size="sm" onClick={() => setShowForm(false)}>
                  <X className="h-4 w-4" />
                </Button>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div className="space-y-2">
                    <Label>Product Image</Label>
                    <div
                      className="h-24 rounded-md border-2 border-dashed border-border/50 flex items-center justify-center cursor-pointer hover:border-primary/50 transition-colors"
                      onClick={() => setImageUploadDialog("new")}
                    >
                      {newProduct.image ? (
                        <img
                          src={newProduct.image || "/placeholder.svg"}
                          alt="Product"
                          className="w-full h-full object-cover rounded-md"
                        />
                      ) : (
                        <div className="text-center">
                          <Upload className="h-6 w-6 mx-auto text-muted-foreground mb-1" />
                          <p className="text-xs text-muted-foreground">Upload Image</p>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="name">Product Name</Label>
                    <Input
                      id="name"
                      value={newProduct.name}
                      onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
                      placeholder="Enter product name"
                      className="border-border/50 focus:border-primary focus:ring-1 focus:ring-primary/20"
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="category">Category</Label>
                    <Select
                      value={newProduct.category}
                      onValueChange={(value) => {
                        setNewProduct({
                          ...newProduct,
                          category: value,
                          color: categoryColors[value as keyof typeof categoryColors] || "",
                        })
                      }}
                      required
                    >
                      <SelectTrigger className="border-border/50 focus:border-primary focus:ring-1 focus:ring-primary/20">
                        <SelectValue placeholder="Select category" />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.keys(categoryColors).map((category) => (
                          <SelectItem key={category} value={category}>
                            {category}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Color Preview</Label>
                    <div className="h-10 rounded-md border border-border/50 flex items-center justify-center">
                      {newProduct.color && <Badge className={newProduct.color}>{newProduct.category}</Badge>}
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="price">Price</Label>
                    <Input
                      id="price"
                      type="number"
                      min="0"
                      step="0.01"
                      value={newProduct.price}
                      onChange={(e) => setNewProduct({ ...newProduct, price: safeNumber(e.target.value, 0) })}
                      placeholder="0.00"
                      className="border-border/50 focus:border-primary focus:ring-1 focus:ring-primary/20"
                      required
                    />
                  </div>
                </div>

                <div className="flex gap-2 mt-4">
                  <Button
                    type="submit"
                    disabled={
                      !newProduct.name ||
                      !newProduct.category ||
                      !Number.isFinite(newProduct.price) ||
                      newProduct.price <= 0
                    }
                    variant="outline"
                    className="border-primary/20 text-primary hover:bg-primary/10 bg-transparent"
                  >
                    Create Product
                  </Button>
                  <Button type="button" variant="ghost" onClick={() => setShowForm(false)}>
                    Cancel
                  </Button>
                </div>
              </form>
            </div>
          </Card>
        </div>
      )}
      <div className="grid gap-4 grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        {products.map((product) => {
          const scheduledDays = getScheduledDays(product.id)
          const availableDays = getAvailableDays(product.id)
          const isEditing = editingProduct === product.id

          return (
            <Card
              key={product.id}
              className={cn(
                "hover:shadow-md transition-all duration-300 group cursor-pointer overflow-hidden p-0", // Added p-0 to remove default card padding
                isEditing && "ring-2 ring-primary shadow-lg",
              )}
              onClick={() => {
                if (isEditing) {
                  setEditingProduct(null)
                } else {
                  setEditingProduct(product.id)
                  setEditingValues({
                    name: product.name,
                    category: product.category,
                    image: product.image,
                    price: Number.isFinite(product.price) ? product.price : 0,
                  })
                }
              }}
            >
              <div className="relative">
                <div className="relative">
                  <div className="w-full h-32 rounded-t-lg overflow-hidden bg-gradient-to-br from-primary/20 to-primary/10">
                    {" "}
                    {/* Image takes full width with no padding */}
                    {product.image ? (
                      <img
                        src={product.image || "/placeholder.svg"}
                        alt={product.name}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        <Package className="h-12 w-12 text-primary" />
                      </div>
                    )}
                  </div>

                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        variant="ghost"
                        size="sm"
                        disabled={availableDays.length === 0}
                        className="absolute top-2 right-10 h-6 w-6 p-0 hover:bg-primary/10 hover:text-primary rounded-md bg-white/90 shadow-sm"
                        onClick={(e) => e.stopPropagation()}
                      >
                        <Calendar className="h-3 w-3" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      {availableDays.map((day) => (
                        <DropdownMenuItem
                          key={day}
                          onClick={() => onAddProduct(day, product)}
                          className="cursor-pointer"
                        >
                          {day} ({getDateForDay(day)})
                        </DropdownMenuItem>
                      ))}
                      {availableDays.length === 0 && (
                        <DropdownMenuItem disabled>All days scheduled</DropdownMenuItem>
                      )}
                    </DropdownMenuContent>
                  </DropdownMenu>

                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="absolute top-2 right-2 h-6 w-6 p-0 hover:bg-red-100 hover:text-red-700 rounded-md bg-white/90 shadow-sm"
                        onClick={(e) => e.stopPropagation()}
                      >
                        <X className="h-3 w-3" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem
                        onClick={() => {
                          onDeleteProduct(product.id)
                        }}
                        className="cursor-pointer text-destructive focus:text-destructive"
                      >
                        Delete Product
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>

                  {isEditing && (
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation()
                        setImageUploadDialog(product.id)
                      }}
                      className="absolute top-2 left-2 h-5 w-5 p-0 bg-white/90 hover:bg-white shadow-sm rounded-md"
                    >
                      <Camera className="h-3 w-3" />
                    </Button>
                  )}
                </div>

                <div className="p-3">
                  {" "}
                  {/* Content area with proper padding */}
                  {isEditing ? (
                    <div className="space-y-2">
                      <Input
                        value={editingValues.name}
                        onChange={(e) => setEditingValues({ ...editingValues, name: e.target.value })}
                        className="font-medium text-sm border-border/50 focus:border-primary focus:ring-1 focus:ring-primary/20 h-8 py-4.5"
                        onClick={(e) => e.stopPropagation()}
                      />
                      <Select
                        value={editingValues.category}
                        onValueChange={(value) => setEditingValues({ ...editingValues, category: value })}
                      >
                        <SelectTrigger
                          className="font-medium text-sm border-border/50 focus:border-primary focus:ring-1 focus:ring-primary/20 h-7"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {Object.keys(categoryColors).map((category) => (
                            <SelectItem key={category} value={category}>
                              {category}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <Input
                        type="number"
                        min="0"
                        step="0.01"
                        value={editingValues.price}
                        onChange={(e) => setEditingValues({ ...editingValues, price: safeNumber(e.target.value, editingValues.price) })}
                        className="font-medium text-sm border-border/50 focus:border-primary focus:ring-1 focus:ring-primary/20 h-8"
                        onClick={(e) => e.stopPropagation()}
                        placeholder="Price"
                      />
                    </div>
                  ) : (
                    <>
                      <h3 className="font-medium text-sm mb-1 leading-tight truncate">{product.name}</h3>
                      <div className="flex items-center justify-between mb-1">
                        <Badge className={cn("text-xs", product.color)}>{product.category}</Badge>
                        <span className="text-[11px] font-medium text-muted-foreground">
                          {formatCurrency(Number.isFinite(product.price) ? product.price : 0)}
                        </span>
                      </div>
                    </>
                  )}
                  {scheduledDays.length > 0 ? (
                    <div className="mt-3 pt-2 border-t border-border/30">
                      <p className="text-xs font-medium text-muted-foreground mb-1">Scheduled:</p>
                      <div className="flex flex-wrap gap-1">
                        {scheduledDays.slice(0, 2).map((day) => (
                          <Badge key={day} variant="outline" className="text-xs">
                            {day.slice(0, 3)} {getDateForDay(day).split(" ").slice(1).join("/")}
                          </Badge>
                        ))}
                        {scheduledDays.length > 2 && (
                          <Badge variant="outline" className="text-xs">
                            +{scheduledDays.length - 2}
                          </Badge>
                        )}
                      </div>
                    </div>
                  ) : (
                    <p className="text-xs text-muted-foreground mt-3 pt-2 border-t border-border/30">Not scheduled</p>
                  )}
                </div>
              </div>
            </Card>
          )
        })}
      </div>
      <div className="flex items-center justify-between pt-4">
        <div className="text-sm text-muted-foreground">
          Showing 1-{Math.min(12, products.length)} of {products.length} products
        </div>
        <div className="flex items-center gap-4">
          <div className="text-xs text-muted-foreground hidden md:block">
            Total value:{" "}
            <span className="font-medium">
              {formatCurrency(
                products.reduce(
                  (s, p) => s + (Number.isFinite(p.price) && p.price >= 0 ? p.price : 0),
                  0,
                ),
              )}
            </span>
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
      <Dialog open={!!deleteDialog} onOpenChange={() => setDeleteDialog(null)}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Delete Product</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete this product? This action cannot be undone and will remove it from all
              scheduled days.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteDialog(null)}>
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={() => {
                if (deleteDialog) {
                  onDeleteProduct(deleteDialog)
                  setDeleteDialog(null)
                }
              }}
            >
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      <Dialog open={!!imageUploadDialog} onOpenChange={() => setImageUploadDialog(null)}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Upload Product Image</DialogTitle>
            <DialogDescription>Choose an image file to upload for this product.</DialogDescription>
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
                    handleImageUpload(file, imageUploadDialog === "new" ? undefined : imageUploadDialog)
                  }
                }}
                className="cursor-pointer"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setImageUploadDialog(null)}>
              Cancel
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
