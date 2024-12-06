import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import Image from "next/image"

type BakeryItem = {
  id: number
  name: string
  price: number
  image: string
}

type BakeryItemCardProps = {
  item: BakeryItem
  count: number
  onAdd: () => void
  onRemove: () => void
}

export function BakeryItemCard({ item, count, onAdd, onRemove }: BakeryItemCardProps) {
  return (
    <Card className="w-full overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300">
      <div className="relative h-40 sm:h-48 w-full">
        <Image
          src={item.image}
          alt={item.name}
          fill
          style={{ objectFit: 'cover' }}
          className="transition-transform duration-300 hover:scale-105"
        />
      </div>
      <CardContent className="p-3 sm:p-4">
        <h3 className="text-lg sm:text-xl font-semibold mb-1 sm:mb-2 text-gray-800">{item.name}</h3>
        <p className="text-base sm:text-lg font-medium text-gray-600">${item.price.toFixed(2)}</p>
      </CardContent>
      <CardFooter className="flex justify-between p-3 sm:p-4 bg-gray-50">
        <Button variant="outline" onClick={onRemove} disabled={count === 0} className="text-sm sm:text-base">-</Button>
        <span className="text-base sm:text-lg font-semibold text-gray-800">{count}</span>
        <Button variant="outline" onClick={onAdd} className="text-sm sm:text-base">+</Button>
      </CardFooter>
    </Card>
  )
}

