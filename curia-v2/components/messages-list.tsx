"use client"

import type React from "react"
import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { MessageCircle, Send, Paperclip, ImageIcon } from "lucide-react"
import { cn } from "@/lib/utils"

interface Message {
  id: string
  sender: string
  content: string
  timestamp: string
  isCurrentUser: boolean
  avatarColor: string
  image?: string
}

interface Conversation {
  id: string
  name: string
  lastMessage: string
  timestamp: string
  avatarColor: string
  unread: number
}

const mockConversations: Conversation[] = [
  {
    id: "1",
    name: "John Smith",
    lastMessage: "I'm wondering about the timeline...",
    timestamp: "10:35 AM",
    avatarColor: "bg-rose-200",
    unread: 2,
  },
  {
    id: "2",
    name: "Sarah Johnson",
    lastMessage: "Hey! Just wanted to check on...",
    timestamp: "11:15 AM",
    avatarColor: "bg-green-200",
    unread: 1,
  },
  {
    id: "3",
    name: "Mike Wilson",
    lastMessage: "Thanks for the update!",
    timestamp: "Yesterday",
    avatarColor: "bg-blue-200",
    unread: 0,
  },
]

const mockMessages: Record<string, Message[]> = {
  "1": [
    {
      id: "1",
      sender: "John Smith",
      content: "Hi! I wanted to ask about the email campaign we discussed.",
      timestamp: "10:30 AM",
      isCurrentUser: false,
      avatarColor: "bg-rose-200",
    },
    {
      id: "2",
      sender: "Current User",
      content: "Of course! What specific details would you like to know?",
      timestamp: "10:32 AM",
      isCurrentUser: true,
      avatarColor: "bg-blue-200",
    },
    {
      id: "3",
      sender: "John Smith",
      content: "I'm wondering about the timeline and deliverables.",
      timestamp: "10:35 AM",
      isCurrentUser: false,
      avatarColor: "bg-rose-200",
    },
  ],
  "2": [
    {
      id: "4",
      sender: "Sarah Johnson",
      content: "Hey! Just wanted to check on the website redesign progress.",
      timestamp: "11:15 AM",
      isCurrentUser: false,
      avatarColor: "bg-green-200",
      image: "/placeholder.svg?height=200&width=300",
    },
    {
      id: "5",
      sender: "Current User",
      content: "Great timing! I was just about to send you an update.",
      timestamp: "11:18 AM",
      isCurrentUser: true,
      avatarColor: "bg-blue-200",
    },
  ],
}

export function MessagesList() {
  const [selectedConversation, setSelectedConversation] = useState<string>("1")
  const [messages, setMessages] = useState<Record<string, Message[]>>(mockMessages)
  const [newMessage, setNewMessage] = useState("")
  const [selectedImage, setSelectedImage] = useState<File | null>(null)

  const getUserInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2)
  }

  const handleSendMessage = () => {
    if (!newMessage.trim() && !selectedImage) return

    const message: Message = {
      id: Date.now().toString(),
      sender: "Current User",
      content: newMessage,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      isCurrentUser: true,
      avatarColor: "bg-blue-200",
      image: selectedImage ? URL.createObjectURL(selectedImage) : undefined,
    }

    setMessages((prev) => ({
      ...prev,
      [selectedConversation]: [...(prev[selectedConversation] || []), message],
    }))
    setNewMessage("")
    setSelectedImage(null)
  }

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedImage(file)
    }
  }

  const currentMessages = messages[selectedConversation] || []

  return (
    <div className="flex h-[calc(100vh-12rem)] gap-4">
      <div className="w-80 border-r border-border/50 pr-4">
        <div className="flex items-center gap-3 mb-4">
          <MessageCircle className="h-6 w-6 text-primary" />
          <h2 className="text-2xl font-bold font-serif">Messages</h2>
        </div>

        <div className="space-y-2">
          {mockConversations.map((conversation) => (
            <Card
              key={conversation.id}
              className={cn(
                "cursor-pointer transition-all duration-200 hover:shadow-sm p-0", // Added p-0 to remove default card padding
                selectedConversation === conversation.id && "ring-2 ring-primary bg-primary/5",
              )}
              onClick={() => setSelectedConversation(conversation.id)}
            >
              <div className="p-3">
                {" "}
                {/* Added padding container for content */}
                <div className="flex items-center gap-3">
                  <div
                    className={cn(
                      "w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium text-gray-700 flex-shrink-0",
                      conversation.avatarColor,
                    )}
                  >
                    {getUserInitials(conversation.name)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium text-sm truncate">{conversation.name}</span>
                      <span className="text-xs text-muted-foreground">{conversation.timestamp}</span>
                    </div>
                    <p className="text-xs text-muted-foreground truncate">{conversation.lastMessage}</p>
                  </div>
                  {conversation.unread > 0 && (
                    <Badge variant="default" className="h-5 w-5 p-0 flex items-center justify-center text-xs">
                      {conversation.unread}
                    </Badge>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>

      <div className="flex-1 flex flex-col">
        <div className="flex items-center gap-3 mb-4 pb-4 border-b border-border/50">
          <div
            className={cn(
              "w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium text-gray-700",
              mockConversations.find((c) => c.id === selectedConversation)?.avatarColor,
            )}
          >
            {getUserInitials(mockConversations.find((c) => c.id === selectedConversation)?.name || "")}
          </div>
          <h3 className="text-lg font-semibold">
            {mockConversations.find((c) => c.id === selectedConversation)?.name}
          </h3>
        </div>

        <div className="flex-1 space-y-2 overflow-y-auto mb-4">
          {currentMessages.map((message) => (
            <div key={message.id} className={cn("flex gap-3", message.isCurrentUser && "justify-end")}>
              {!message.isCurrentUser && (
                <div
                  className={cn(
                    "w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium text-gray-700 flex-shrink-0",
                    message.avatarColor,
                  )}
                >
                  {getUserInitials(message.sender)}
                </div>
              )}
              <div className={cn("max-w-[70%]", message.isCurrentUser && "text-right")}>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-sm font-medium">{message.sender}</span>
                  <span className="text-xs text-muted-foreground">{message.timestamp}</span>
                </div>
                <Card
                  className={cn(
                    "inline-block p-0", // Added p-0 to remove default card padding
                    message.isCurrentUser ? "bg-primary text-primary-foreground" : "bg-muted",
                  )}
                >
                  <div className="p-2">
                    {" "}
                    {/* Added padding container for message content */}
                    {message.image && (
                      <img
                        src={message.image || "/placeholder.svg"}
                        alt="Shared image"
                        className="rounded-md mb-2 max-w-full h-auto"
                      />
                    )}
                    <p className="text-sm">{message.content}</p>
                  </div>
                </Card>
              </div>
              {message.isCurrentUser && (
                <div
                  className={cn(
                    "w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium text-gray-700 flex-shrink-0",
                    message.avatarColor,
                  )}
                >
                  {getUserInitials(message.sender)}
                </div>
              )}
            </div>
          ))}
        </div>

        <Card className="border-2 border-primary/20 p-0">
          {" "}
          {/* Added p-0 to remove default card padding */}
          <div className="p-4">
            {" "}
            {/* Added padding container for input area */}
            {selectedImage && (
              <div className="mb-3 p-2 bg-muted rounded-md flex items-center gap-2">
                <ImageIcon className="h-4 w-4" />
                <span className="text-sm">{selectedImage.name}</span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedImage(null)}
                  className="ml-auto h-6 w-6 p-0"
                >
                  ×
                </Button>
              </div>
            )}
            <div className="flex gap-2">
              <Input
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 border-border/50 focus:border-primary focus:ring-1 focus:ring-primary/20"
                onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
              />
              <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" id="image-upload" />
              <Button
                variant="ghost"
                size="sm"
                onClick={() => document.getElementById("image-upload")?.click()}
                className="px-3"
              >
                <Paperclip className="h-4 w-4" />
              </Button>
              <Button
                onClick={handleSendMessage}
                disabled={!newMessage.trim() && !selectedImage}
                variant="outline"
                className="border-primary/20 text-primary hover:bg-primary/10 bg-transparent px-4"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}
