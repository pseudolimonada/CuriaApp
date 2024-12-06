import { useState } from 'react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogClose,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ScrollArea } from "@/components/ui/scroll-area"

// ... (previous type definitions remain unchanged)

export function CatalogManagementPopup({ isOpen, onClose, catalog, setCatalog }: CatalogManagementPopupProps) {
  const [newItem, setNewItem] = useState<Omit<BakeryItem, 'id'>>({ name: '', price: 0, image: '' })

  const handleAddItem = () => {
    const id = Math.max(0, ...catalog.map(item => item.id)) + 1
    setCatalog(prev => [...prev, { ...newItem, id }])
    setNewItem({ name: '', price: 0, image: '' })
  }

  const handleRemoveItem = (id: number) => {
    setCatalog(prev => prev.filter(item => item.id !== id))
  }

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setNewItem(prev => ({ ...prev, image: reader.result as string }))
      }
      reader.readAsDataURL(file)
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl w-full h-[calc(100vh-4rem)] max-h-[800px] flex flex-col bg-white bg-opacity-90 backdrop-blur-lg border border-gray-200">
        <DialogHeader className="flex-shrink-0">
          <DialogTitle className="text-2xl font-bold text-gray-800">Manage Catalog</DialogTitle>
        </DialogHeader>
        <ScrollArea className="flex-grow">
          <div className="space-y-4 p-4">
            {catalog.map(item => (
              <div key={item.id} className="flex items-center justify-between border-b pb-2">
                <div>
                  <p className="font-semibold">{item.name}</p>
                  <p>${item.price.toFixed(2)}</p>
                </div>
                <Button onClick={() => handleRemoveItem(item.id)} variant="destructive">Remove</Button>
              </div>
            ))}
          </div>
        </ScrollArea>
        <div className="mt-4 space-y-4 flex-shrink-0">
          <h3 className="text-lg font-semibold">Add New Item</h3>
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              value={newItem.name}
              onChange={e => setNewItem(prev => ({ ...prev, name: e.target.value }))}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="price">Price</Label>
            <Input
              id="price"
              type="number"
              value={newItem.price}
              onChange={e => setNewItem(prev => ({ ...prev, price: parseFloat(e.target.value) }))}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="image">Image</Label>
            <Input
              id="image"
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
            />
          </div>
          <Button onClick={handleAddItem}>Add Item</Button>
        </div>
        <DialogClose asChild>
          <Button className="mt-4 bg-gray-800 hover:bg-gray-900 text-white">Close</Button>
        </DialogClose>
      </DialogContent>
    </Dialog>
  )
}

