import { Route, Routes, useLocation } from "react-router-dom";
import "./app/globals.css";
import "./App.css";
import Chat from "./pages/Chat";
import Login from "./pages/Login";
import FileSelector from "./pages/FileSelector";
import SelectedFiles from "./pages/SelectedFiles";
import { Toaster } from "react-hot-toast";
import { ThemeProvider } from "./components/theme-provider";
import MainLayout from "./layouts/MainLayout";

function App() {
  const location = useLocation();

  const noSidebarRoutes = ["/"];

  const isNoSidebar = noSidebarRoutes.includes(location.pathname);

  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="light"
      enableSystem
      storageKey="vite-ui-theme"
    >
      <Toaster position="top-center" reverseOrder={false} />
      {isNoSidebar ? (
        <Routes>
          <Route path="/" element={<Login />} />
        </Routes>
      ) : (
        <MainLayout>
          <Routes>
            <Route path="/chat" element={<Chat />} />
            <Route path="/get_files" element={<FileSelector />} />
            <Route path="/selected_files" element={<SelectedFiles />} />
          </Routes>
        </MainLayout>
      )}
    </ThemeProvider>
  );
}

export default App;
