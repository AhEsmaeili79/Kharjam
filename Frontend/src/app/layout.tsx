"use_client"
import './globals.css'
import { Button } from "@/components/ui/button"
import Home from './home/page';


export default function RootLayout() {
  return (
    <html lang="en">
      <body  className="bg-gray-500 size-full">
      <h1 className="text-green-600">
        the layout
        </h1>

        <div>
      <Button variant="default">shadcn button</Button>
    </div>
    <Home/>
        
      </body>
    </html>
  );
}
