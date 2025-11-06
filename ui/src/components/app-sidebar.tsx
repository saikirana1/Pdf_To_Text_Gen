import { Link } from "react-router-dom";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { useTheme } from "next-themes";
import { Sun, Moon, MessageSquare, FileText } from "lucide-react";
import { useNavigate } from "react-router-dom";
import logo from "@/assets/logo.png";

export function AppSidebar() {
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();
  const items = [
    {
      title: "Chat",
      url: "/chat",
      icon: MessageSquare,
    },
    {
      title: "Uploaded Files",
      url: "/get_files",
      icon: FileText,
    },
    {
      title: "Selected Files",
      url: "/selected_files",
      icon: FileText,
    },
  ];
  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarHeader className="flex  items-center justify-center">
            <div className="flex  flex-col items-center space-x-2 space-y-0.5">
              <h1 className=" text-center">Powered By</h1>

              <img
                src={logo}
                alt="Company Logo"
                className="w-40 h-30  object-cover mt-2 "
              />
            </div>
          </SidebarHeader>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton
                    className="flex items-center gap-2 px-3 py-2 rounded-md 
           hover:bg-gray-200 dark:hover:bg-gray-800 
           hover:text-gray-500 hover:scale-105 
           transition-all duration-200"
                    asChild
                  >
                    <Link to={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="p-2">
        <div className="flex flex-row items-center justify-between gap-4 p-2">
          {/* Theme Toggle Button */}
          <button
            onClick={() => {
              setTheme(theme === "dark" ? "light" : "dark");
            }}
            className="flex items-center justify-center w-10 h-10 border rounded-full bg-black text-white hover:bg-gray-500 dark:hover:bg-gray-800 transition"
          >
            {theme === "dark" ? (
              <Sun className="w-5 h-5" />
            ) : (
              <Moon className="w-5 h-5" />
            )}
          </button>

          {/* Logout Button */}
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-zinc-400 text-white rounded-lg hover:bg-gray-600 transition"
          >
            LogOut
          </button>
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}
