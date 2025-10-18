import { Route, Routes } from 'react-router-dom'
import "./app/globals.css"
import './App.css'
import Chat from './pages/Chat'
import Login from './pages/Login'
import UploadDocument from './pages/UploadDocument'
import { Toaster } from 'react-hot-toast';
import { SidebarProvider, SidebarTrigger } from './components/ui/sidebar'
import { AppSidebar } from './components/app-sidebar'
import { ThemeProvider } from './components/theme-provider'
import FileSelector from './pages/FileSelector'


function App() {

  return (
    <>
       <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
     <SidebarProvider>
      <AppSidebar/>
          <main className="flex-1 p-4 ">
            <h1>welcome</h1>
        <SidebarTrigger />
             <Routes>
              <Route path="/" element={<Chat />} />
               <Route path="/get_files" element={<FileSelector />} />
              {/* <Route path="/calendar" element={<CalendarPage />} />
              <Route path="/search" element={<SearchPage />} />
              <Route path="/settings" element={<SettingsPage />} /> */}
            </Routes>
      </main>
        </SidebarProvider>
        </ThemeProvider>
    </>
  )
}

export default App


